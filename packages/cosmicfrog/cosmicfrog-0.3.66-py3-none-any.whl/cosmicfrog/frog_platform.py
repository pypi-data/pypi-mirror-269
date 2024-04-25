"""
Functions to facilitate interactions with Optilogic platform using 'optilogic' library
"""

import os
import json
import logging
import time
from typing import Tuple
import optilogic
import requests

class OptilogicClient:
    """
    Wrapper for optilogic module for consumption in Cosmic Frog services
    """

    def __init__(self, username=None, appkey=None, logger=logging.getLogger()):
        # Detect if being run in Andromeda
        job_app_key = os.environ.get("OPTILOGIC_JOB_APPKEY")

        if appkey and not username:
            # Use supplied key
            self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=appkey)
        elif appkey and username:
            # Use supplied key & name
            self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=appkey, un=username)
        elif job_app_key:
            # Running on Andromeda
            self.api = optilogic.pioneer.Api(auth_legacy=False)
        else:
            raise ValueError("OptilogicClient could not authenticate")

        self.logger = logger

    def model_exists(self, model_name: str) -> bool:
        """
        Returns True if a given model exists, False otherwise
        """
        try:
            return self.api.storagename_database_exists(model_name)
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error(f"Exception in cosmicfrog: {e}")
            return False

    def get_connection_string(self, model_name: str) -> Tuple[bool, str]:

        # TODO: There are two connection string fetch functions, see also frog_dbtools

        try:
            rv = {"message": "error getting connection string"}
            if not self.api.storagename_database_exists(model_name):
                return False, ""

            connection_info = self.api.sql_connection_info(model_name)

            return True, connection_info["connectionStrings"]["url"]

        except Exception as e:
            self.logger.error(f"Exception in cosmicfrog: {e}")
            return False, ""

    def create_model_synchronous(self, model_name: str, model_template: str):
        try:
            new_model = self.api.database_create(name=model_name, template=model_template)

            status = "success"
            rv = {}
            if "crash" in new_model:
                status = "error"
                rv["message"] = json.loads(new_model["response_body"])["message"]
                rv["httpStatus"] = new_model["resp"].status_code
            else:
                while not self.api.storagename_database_exists(model_name):
                    self.logger.info(f"creating {model_name}")
                    time.sleep(3.0)
                connections = self.api.sql_connection_info(model_name)
                rv["model"] = new_model
                rv["connection"] = connections

            return status, rv

        except Exception as e:
            return "exception", e

    def get_pk_custom_columns_from_platform(self, table_name: str, model_name: str, appkey: str, log):
        ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL")
        url = f'https://api.optilogic.app/v0/storage/{model_name}/custom-columns?tableName={table_name}'
        response = requests.get(url, headers={'X-App-Key': appkey})

        try:
            response_data = response.json()
            if response.status_code == 200 and response_data.get('result') == 'success':

                required_columns = [column['columnName'] for column in  response_data.get('customColumns', []) if column.get('isTableKeyColumn', True)]
                return required_columns
            else:
                log.error(f"Error: {response_data.get('message')}")
                for error in response_data.get('errorDetails', []):
                    print(f"Type: {error.get('type')}, Table Name: {error.get('tableName')}, Column Name: {error.get('columnName')}, Expected: {error.get('expected')}, Actual: {error.get('actual')}, Description: {error.get('description')}")
                return []
        except Exception as e:
            log.error(f"An error occurred fetching custom column PKs: {str(e)}")
            return []
        
    def get_custom_tables(self,  model_name: str, appkey: str, log):
        ATLAS_API_BASE_URL = os.getenv("ATLAS_API_BASE_URL")
        url = f'https://api.optilogic.app/v0/storage/{model_name}/custom-tables'
        response = requests.get(url, headers={'X-App-Key': appkey})

        try:
            response_data = response.json()
            if response.status_code == 200 and response_data.get('result') == 'success':
                return response_data.get('customTables', [])
            else:
                log.error(f"Error: {response_data.get('message')}")
                return []
        except Exception as e:
            log.error(f"An error occurred fetching custom tables: {str(e)}")
            return []
