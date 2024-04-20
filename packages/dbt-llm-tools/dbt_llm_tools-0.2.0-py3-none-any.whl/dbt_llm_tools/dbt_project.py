import glob
import json
import os
import re
from typing import Union

import yaml

from tinydb import TinyDB, Query

from dbt_llm_tools.types import DbtModelDirectoryEntry, DbtProjectDirectory

SOURCE_SEARCH_EXPRESSION = r"source\(['\"]*(.*?)['\"]*?\)"
REF_SEARCH_EXPRESSION = r"ref\(['\"]*(.*?)['\"]*\)"


class DbtProject:
    """
    A class representing a DBT project.
    """

    def __init__(
        self,
        dbt_project_root: str,
        database_path: str = ".local_storage/db.json",
    ) -> None:
        """
        Initializes a dbt project parser object.

        Args:
            dbt_project_root (str): Root of the dbt prject
            database_path (str, optional): Path to the directory file that stores the parsed dbt project.

        Methods:
            parse: Parse the dbt project and store details in a manifest file.
            get_single_model: Get a single model by name.
            get_models: Get a list of models based on the provided filters.
            update_model_directory: Update a model in the directory.
        """
        self.__project_root = dbt_project_root
        project_file = os.path.join(dbt_project_root, "dbt_project.yml")

        if not os.path.isfile(project_file):
            raise Exception("No dbt project found in the specified folder")

        self.__database_path = database_path
        os.makedirs(os.path.dirname(database_path), exist_ok=True)

        with open(project_file, encoding="utf-8") as f:
            project_config = yaml.safe_load(f)
            self.__model_paths = project_config.get("model-paths", ["models"])

        self.__sql_files = self.__get_all_files("sql")
        self.__yaml_files = self.__get_all_files("yml")

    def __get_all_files(self, file_extension: str):
        """
        Get all files of a certain type in the dbt project.

        Args:
            file_extension (str): The file extension to search for.

        Returns:
            list: A list of files with the specified extension.
        """
        files = []

        for path in self.__model_paths:
            files.extend(
                glob.glob(
                    os.path.join(
                        self.__project_root, path, "**", f"*.{file_extension}"
                    ),
                    recursive=True,
                )
            )

        return files

    def __find_upstream_references(
        self, file_path: str, recursive: bool = False, dependencies: list[str] = None
    ):
        """
        Find upstream references in a SQL file.

        Args:
            file_path (str): The path to the SQL file.
            recursive (bool, optional): Whether to recursively search for upstream references.
            dependencies (list, optional): A list of dependencies to add to.

        Returns:
            list: A list of upstream references.
        """
        if dependencies is None:
            dependencies = []

        with open(file_path, encoding="utf-8") as f:
            file_contents = f.read()

        search_results = re.findall(REF_SEARCH_EXPRESSION, file_contents)
        unique_results = list(set(search_results))

        if recursive:
            for result in unique_results:
                if result in dependencies or result in file_path:
                    continue

                sub_file_path = next(
                    (x for x in self.__sql_files if x.endswith(f"/{result}.sql")), None
                )
                if sub_file_path is not None:
                    dependencies = self.__find_upstream_references(
                        file_path=sub_file_path,
                        recursive=True,
                        dependencies=dependencies,
                    )

        return dependencies + unique_results

    def __parse_sql_file(self, sql_file: str):
        """
        Parse a SQL file and return a dictionary with the file metadata.

        Args:
            sql_file (str): The path to the SQL file.

        Returns:
            dict: A dictionary containing the parsed SQL file metadata.
        """
        with open(sql_file, encoding="utf-8") as f:
            sql_contents = f.read()

        sources = []
        source_search = re.findall(SOURCE_SEARCH_EXPRESSION, sql_contents)

        for raw_source in source_search:
            source = raw_source.replace("'", "").replace('"', "").split(",")
            if len(source) == 2:
                sources.append({"name": source[0], "table": source[1]})

        return {
            "type": "model",
            "absolute_path": sql_file,
            "relative_path": sql_file.replace(self.__project_root, ""),
            "name": os.path.basename(sql_file).replace(".sql", ""),
            "refs": self.__find_upstream_references(sql_file, False),
            "deps": self.__find_upstream_references(sql_file, True),
            "sources": sources,
            "sql_contents": sql_contents,
        }

    def __parse_yaml_files(self, yaml_files: list[str]):
        """
        Extract documentation from the parsed yaml files.

        Args:
            yaml_files (list): A list of yaml files to parse.

        Returns:
            dict: A dictionary containing the parsed models.
            dict: A dictionary containing the parsed sources.
        """
        models = {}
        sources = {}

        for yaml_path in yaml_files:
            with open(yaml_path, encoding="utf-8") as f:
                yaml_contents = yaml.safe_load(f)

            if yaml_contents is None:
                continue

            for model in yaml_contents.get("models", []):
                model["yaml_path"] = yaml_path
                models[model["name"]] = model

            for source in yaml_contents.get("sources", []):
                source["type"] = "source"
                source["yaml_path"] = yaml_path
                sources[source["name"]] = source

        return models, sources

    def __get_directory(self):
        """
        Get the parsed directory from the directory file.

        Returns:
            dict: The parsed directory.
        """
        with open(self.__database_path, encoding="utf-8") as f:
            return json.load(f)

    def __save_directory(self, directory):
        """
        Save the parsed directory to a file.

        Args:
            directory (dict): The directory to save.
        """
        db = TinyDB(self.__database_path, sort_keys=True, indent=4)
        Model = Query()  # pylint: disable=invalid-name
        Source = Query()  # pylint: disable=invalid-name

        for name, model in directory["models"].items():
            if "name" in model:
                db.upsert(model, Model.name == name)

        for name, source in directory["sources"].items():
            if "name" in source:
                db.upsert(source, Source.name == source["name"])

    def parse(self) -> DbtProjectDirectory:
        """
        Parse the dbt project and store details in a manifest file.

        Returns:
            dict: The parsed directory.
        """
        source_sql_models = {}

        for sql_file in self.__sql_files:
            parsed_model = self.__parse_sql_file(sql_file)
            source_sql_models[parsed_model["name"]] = parsed_model

        documented_models, documented_sources = self.__parse_yaml_files(
            self.__yaml_files
        )

        for model_name, model_dict in documented_models.items():
            yaml_path = model_dict.pop("yaml_path")

            if model_name in source_sql_models:
                source_sql_models[model_name]["yaml_path"] = yaml_path
                source_sql_models[model_name]["documentation"] = model_dict
            else:
                source_sql_models[model_name] = {
                    "yaml_path": yaml_path,
                    "documentation": model_dict,
                }

        directory = {
            "models": source_sql_models,
            "sources": documented_sources,
        }

        self.__save_directory(directory)

        return directory

    def get_single_model(self, model_name: str) -> Union[DbtModelDirectoryEntry, None]:
        """
        Get a single model by name.

        Args:
            model_name (str): The name of the model to get.

        Returns:
            dict: The model object.
        """
        if model_name is None:
            raise Exception("No model name provided")

        # directory = self.__get_directory()
        db = TinyDB(self.__database_path)
        Model = Query()  # pylint: disable=invalid-name

        return db.get(Model.name == model_name)

    def get_models(
        self,
        models: list[str] = None,
        included_folders: list[str] = None,
        excluded_folders: list[str] = None,
    ):
        """
        Get a list of models based on the provided filters.

        Args:
            models (list, optional): A list of model names to get.
            included_folders (list, optional): A list of folders to include in the search for sql or yaml files.
            excluded_folders (list, optional): A list of folders to exclude from the search for sql or yaml files.

        Returns:
            list: A list of DbtModel objects.
        """
        searched_models = []

        db = TinyDB(self.__database_path)
        Model = Query()  # pylint: disable=invalid-name
        File = Query()  # pylint: disable=invalid-name

        if models is None and included_folders is None:
            searched_models = db.search(File.type == "model")

        for model in models or []:
            if model := db.get(Model.name == model):
                searched_models.append(model)

        for included_folder in included_folders or []:
            for model in db.search(File.type == "model"):
                if included_folder in model.get(
                    "absolute_path", ""
                ) or included_folder in model.get("yaml_path", ""):
                    searched_models.append(model)

        for excluded_folder in excluded_folders or []:
            for model in searched_models.copy():
                if excluded_folder in model.get(
                    "absolute_path", ""
                ) or excluded_folder in model.get("yaml_path", ""):
                    searched_models.remove(model)

        return searched_models

    def update_model_directory(self, model: dict):
        """
        Update a model in the directory.

        Args:
            model (dict): The model to update.
        """
        directory = self.__get_directory()

        if model["name"] in directory["models"]:
            directory["models"][model["name"]] = model

        self.__save_directory(directory)
