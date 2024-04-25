"""
Module holding AnuraSchema class
"""

import os
from typing import List, Dict, Tuple
import importlib.resources
import json
from cachetools import cached, LRUCache

# Hold supported schema versions, and maps to the directory in which they are stored
# Key: schema from model db
# Value: json folder
SUPPORTED_SCHEMAS = {"anura_2_7": "anura27", "anura_2_8": "anura28", "stable": "anura27", "preview": "anura28"}

LIBRARY_NAME = "cosmicfrog"


class AnuraSchema:
    """
    Static class for managing Anura schema versions
    """

    def __init__(self):
        raise RuntimeError("Do not instantiate directly - Static class")

    @staticmethod
    @cached(LRUCache(maxsize=len(SUPPORTED_SCHEMAS)))
    def get_anura_masterlist(anura_version: str) -> List:
        """
        Return the masterlist for the given Anura schema

        """
        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/anuraMasterTableList.json"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Fetch all table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            table_name = field["Table"]
            result.append(table_name)

        if lower_case:
            return [s.lower() for s in result]

        return result
    
    # get abreviated names
    def get_anura_abreviated_table_names(anura_version: str) -> Dict[str, str]:
        """
        Fetch all abbreviated table names and create a dictionary with table names
        """

        result = {}

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            table_name = field["Table"].lower()
            abbreviated_name = field["AbbreviatedName"].lower()

            result[abbreviated_name] = table_name

        return result

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_input_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Fetch input table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            if field["Category"].startswith("Output") is False:
                result.append(field["Table"])

        if lower_case:
            return [s.lower() for s in result]

        return result

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_output_table_names(anura_version: str, lower_case: bool = True) -> List[str]:
        """
        Return output  table names
        """

        result = []

        for field in AnuraSchema.get_anura_masterlist(anura_version):
            if field["Category"].startswith("Output"):
                result.append(field["Table"])

        if lower_case:
            return [s.lower() for s in result]

        return result

    @staticmethod
    def get_anura_keys(anura_version: str, table_name: str) -> List[str]:
        """
        Get table keys defined in Anura schema
        """

        anura_keys, _ = AnuraSchema._get_anura_key_and_column_dicts(anura_version)

        return anura_keys.get(table_name, [])

    @staticmethod
    def get_anura_columns(anura_version: str, table_name: str) -> List[str]:
        """
        Get table coluimns defined in Anura schema
        """
        _, anura_columns = AnuraSchema._get_anura_key_and_column_dicts(anura_version)

        return anura_columns.get(table_name, [])

    @staticmethod
    @cached(LRUCache(maxsize=2))
    def _get_anura_key_and_column_dicts(
        anura_version: str,
    ) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Extract keys and columns from json definitions
        """

        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/table_definitions"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:

            anura_keys = {}
            anura_cols = {}

            # Iterate over each file in the directory
            for filename in os.listdir(file_path):

                if not filename.endswith(".json"):
                    continue

                filepath = os.path.join(file_path, filename)

                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                table_name = data.get("TableName").lower()

                # Extract the column names where "PK" is "Yes"
                anura_cols[table_name] = [
                    field["Column Name"].lower() for field in data.get("fields", [])
                ]
                anura_keys[table_name] = [
                    field["Column Name"].lower()
                    for field in data.get("fields", [])
                    if field.get("PK") == "Yes"
                ]

            return anura_keys, anura_cols

    @staticmethod
    @cached(LRUCache(maxsize=2 * len(SUPPORTED_SCHEMAS)))
    def get_anura_master_table_mappings(anura_version: str):
        """
        Return the master table mappings for the given Anura schema
        """

        json_path = f"{SUPPORTED_SCHEMAS[anura_version]}/anuraMasterTablesMappings.json"

        with importlib.resources.as_file(
            importlib.resources.files(LIBRARY_NAME).joinpath(json_path)
        ) as file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                return json.load(file)
