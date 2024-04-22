# Import System libraries required for Pre-Check
from datetime import datetime
import json
import hashlib
from types import SimpleNamespace
import requests
import os
import sys

# Class BotUtiles contains common functions which is used in cloud/Device bots
class BotUtils:
    __json_response = None
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    __cwEndpoint = None
    __cwProductId_connectionId = None
    __cwTenantId = None

    @staticmethod
    def fetch_input_data() -> dict:
        with open("input.json", "r") as file:
            data = json.load(file)

            # Store sensitive inputs as class attributes
            BotUtils.__cwEndpoint = data.get('cwEndpoint')
            BotUtils.__cwProductId_connectionId = data.get('cwProductId_connectionId')
            BotUtils.__cwTenantId = data.get('cwTenantId')

            # Exclude sensitive inputs from being exposed
            filtered_data = {key: value for key, value in data.items() if key not in ['cwEndpoint', 'cwProductId_connectionId', 'cwTenantId']}
            return SimpleNamespace(**filtered_data)
    
    @staticmethod
    def __log_result_internal(
        msg: str = "",
        is_json_only: bool = False,
        msg_level: str = None,
        status: str = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Function to redirect output to Result.txt
        """

        if not is_json_only:
            try:
                with open("Output/Result.txt", "a+") as file:
                    file.seek(0)
                    (
                        file.write(
                            f"[{BotUtils.timestamp}][Result]\n------------------------------\n"
                        )
                        if not file.read()
                        else None
                    )
                    file.write(msg + "\n")
            except Exception:
                raise Exception("Error while redirecting output to Result.txt")
                exit()

        if msg_level:
            BotUtils.__log___json_response(msg=msg, msg_level=msg_level, status=status)

        if status:
            BotUtils.__log___json_response(status=status)

    @staticmethod
    def __log_error_internal(
        msg: str = "",
        is_json_only: bool = False,
        msg_level: str = None,
        status: str = None,
        *args,
        **kwargs,
    ) -> None:
        """
        Function to redirect error to Error.txt
        """

        if not is_json_only:
            try:
                with open("Output/Error.txt", "a+") as file:
                    file.seek(0)
                    (
                        file.write(
                            f"[{BotUtils.timestamp}][Error]\n----------------------------\n"
                        )
                        if not file.read()
                        else None
                    )
                    file.write(msg + "\n")
            except:
                raise Exception("Error while redirecting error to Error.txt")

        if msg_level:
            BotUtils.__log___json_response(msg=msg, msg_level=msg_level, status=status)

        if status:
            BotUtils.__log___json_response(status=status)

    @staticmethod
    def __log___json_response(msg_level=None, msg: str = None, status: str = None):
        if BotUtils.__json_response is None:
            BotUtils.__json_response = {"status": "", "messages": [], "data": []}

        if status is not None:
            BotUtils.__json_response["status"] = status

        if msg and msg_level:
            BotUtils.__json_response["messages"].append(
                {"level": msg_level, "message": msg}
            )
   
    @staticmethod
    def get_default_domain(access_token_for_graph):
        try:
            headers = {
                "Authorization": f"Bearer {access_token_for_graph}",
                "Content-Type": "application/json",
            }
            # Retrieve all domains
            domains_response = requests.get(
                url="https://graph.microsoft.com/v1.0/domains", headers=headers
            )
            domains_response.raise_for_status()
            domains_data = domains_response.json().get("value", [])

            # Find the default domain
            for domain in domains_data:
                if domain.get("isInitial"):
                    return domain.get("id")

            return None  # Return None if default domain not found
        except Exception as e:
            print(f"Error occurred while fetching default domain: {str(e)}")
            return None

    @staticmethod
    def __acquire_access_token_from_extensibility(
        cwEndpoint: str, cwProductId_connectionId: str, cwTenantId: str, Scopes: list
    ):
        try:
            # first refresh token
            refresh_token_URL = f"{cwEndpoint}/third-party-integration/v1/oauth/{cwProductId_connectionId}/token"
            res = requests.get(refresh_token_URL)
            res.raise_for_status()
            res_json = res.json()
            refresh_token = res_json["refresh_token"]
            # access tokens here
            access_token_URL = f"{cwEndpoint}/third-party-integration/v1/oauth/{cwProductId_connectionId}/customer/{cwTenantId}/authorize"
            req_json = {
                "grant_type": "refresh_token",
                "scope": "*",
                "resource_list": Scopes,
                "refresh_token": refresh_token,
            }
            res = requests.post(url=access_token_URL, json=req_json)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            raise Exception(f"Error while aquiring access token: {e}")

    @staticmethod
    def __extract_access_token(tokens, scope="https://graph.microsoft.com"):
        if "resource_tokens" not in tokens:
            return None

        for token in tokens["resource_tokens"]:
            if token["resource"] == scope:
                return token["access_token"]
        return None

    @staticmethod
    def log_result(msg):
        # BotUtils.__log_result_internal(f"{msg}")
        BotUtils.__log_result_internal(
            msg=msg,
            is_json_only=False,
            msg_level="success",
            status="Success",
        )
        BotUtils.__create_result_json_file()

    @staticmethod
    def log_error(msg):
        # BotUtils.__log_error_internal(f"{msg}")
        BotUtils.__log_error_internal(
            msg=msg,
            is_json_only=False,
            status="Failed",
            msg_level="error",
        )
        BotUtils.__create_result_json_file()

    @staticmethod
    def __create_result_json_file():
        has_error = any(
            message["level"] in "error"
            for message in BotUtils.__json_response["messages"]
        )
        BotUtils.__json_response["status"] = "Failed" if has_error else "Success"
        output_dir = os.path.join(os.getcwd(), "Output")
        result_json_path = os.path.join(output_dir, "result.json")
        with open(result_json_path, "w") as result_json_file:
            json.dump(BotUtils.__json_response, result_json_file, indent=4)

    @staticmethod
    def generate_access_token():
        try:
            if (
                not BotUtils.__cwEndpoint
                or not BotUtils.__cwProductId_connectionId
                or not BotUtils.__cwTenantId
            ):
                BotUtils.log_error(
                    "[Error : Unable to process the request kindly check Client ID, Client Secret and Tenant ID]"
                )
                return False

            scopes = ["https://graph.microsoft.com", "https://outlook.office365.com"]

            tokens: dict = BotUtils.__acquire_access_token_from_extensibility(
                cwEndpoint=BotUtils.__cwEndpoint,
                cwProductId_connectionId=BotUtils.__cwProductId_connectionId,
                cwTenantId=BotUtils.__cwTenantId,
                Scopes=scopes,
            )

            access_token_for_exchange_online = BotUtils.__extract_access_token(
                tokens=tokens, scope="https://outlook.office365.com"
            )
            access_token_for_graph = BotUtils.__extract_access_token(
                tokens=tokens, scope="https://graph.microsoft.com"
            )

            return SimpleNamespace(
                access_token_for_exchange_online=access_token_for_exchange_online,
                access_token_for_graph=access_token_for_graph,
            )
        except Exception as e:
            BotUtils.log_error(f"{e}")

# Executor and perform initial setups
class BotExecutor:
    
    @staticmethod
    def create_out_dir(output_dir="Output"):
        try:

            output_dir_path = os.path.abspath(output_dir)
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
            else:
                [
                    os.remove(os.path.join(output_dir_path, outputfiles))
                    for outputfiles in os.listdir(output_dir_path)
                    if os.path.isfile(os.path.join(output_dir_path, outputfiles))
                ]
        except Exception as e:
            if (
                "The process cannot access the file because it is being used by another process"
                in str(e)
            ):
                raise Exception(
                    "Output file is used by another process, please close the file and try again"
                )
            else:
                raise Exception(
                    "Error while creating Output folder/removing output files"
                )

    @staticmethod
    def initialize():
        BotExecutor.check_python_version()
        BotExecutor.create_out_dir()

    @staticmethod
    def check_python_version():
        if sys.version_info < (3, 10):
            raise Exception("Python version should be 3.6 or higher")
