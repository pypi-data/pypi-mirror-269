import copy
import json
from urllib.parse import urlparse

from azure.storage.blob import BlobServiceClient
from colorama import Fore

from btpy.configuration.config import get_env_data_storage_name
from .env_desc import EnvDesc
from .. import azure_utility
from ..file_utility import to_absolute_path

DEF_ACCOUNT_NAME = "stgbttfdata"
DEF_CONTAINER_NAME = "terraformoutput"
BLOB_ACCOUNT_URL = f"https://{DEF_ACCOUNT_NAME}.blob.core.windows.net"


async def list_envs():
    blob_names = await _load_env_file_blob_names()
    return _extract_envs_from_blob_names(blob_names)


async def load_env_desc(env_name: str):
    env_blob_data = await _load_env_blob_data(env_name)

    if env_blob_data is None:
        return None

    if "version" not in env_blob_data:
        print(f"{Fore.RED}{env_name} does not have version")
        return None

    desc_template = _load_versioned_desc_template(env_blob_data["version"])
    env_desc = _evaluate_desc_template(desc_template, env_blob_data)

    return env_desc


async def _load_env_file_blob_names():
    with _get_blob_container_client() as container_client:
        blob_names = []

        for blob in container_client.list_blobs():
            blob_names.append(blob.name)

        return blob_names


def _extract_envs_from_blob_names(blob_names):
    # Parse blob names and extract environments/stamps
    env_structure = {}

    for name in blob_names:
        name_parts = name.split("/")
        app_name = name_parts[0]
        env_name = name_parts[1]
        stamp_name = name_parts[2]

        if app_name not in env_structure:
            env_structure[app_name] = {}

        if env_name not in env_structure[app_name]:
            env_structure[app_name][env_name] = []

        if stamp_name not in env_structure[app_name][env_name]:
            env_structure[app_name][env_name].append(stamp_name)

    # Generate envs list
    envs = []

    for app_name in env_structure:
        for env_name in env_structure[app_name]:
            for stamp_name in env_structure[app_name][env_name]:
                envs.append(f"{app_name}.{env_name}.{stamp_name}")

    return envs


async def _load_env_blob_data(env_name: str):
    formatted_env_id = f"{env_name.replace('.', '/')}/@latest"

    with _get_blob_container_client() as container_client:
        tf_data = {}
        blob_names = []

        for blob in container_client.list_blobs(name_starts_with=formatted_env_id):
            blob_names.append(blob.name)

        if len(blob_names) == 0:
            return None

        for blob_name in blob_names:
            blob_client = container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob()
            blob_obj = json.loads(blob_data.readall())
            tf_data.update(blob_obj)
            blob_client.close()

        return tf_data


def _load_versioned_desc_template(version: str):
    template_version_filename = f"bt_{version.replace('.', '_')}.json"

    with open(to_absolute_path(f"envs/desc_templates/{template_version_filename}"), "r") as template_file:
        return template_file.read()


def _evaluate_desc_template(template: str, env_blob_data: dict):
    # Generate extra data
    env_data = copy.deepcopy(env_blob_data)
    evaluated_template = template

    # env_data["tenant_id"] = "needed?"
    env_data["sub_id"] = _get_sub_id(env_data)
    env_data["ingress_eh_url"] = _construct_ingress_eh_url(env_data)
    env_data["stamp_tag"] = _get_stamp_tag(env_data)
    env_data["env_tag"] = _get_env_tag(env_data)
    env_data["frontend_storage_name"] = _get_frontend_storage_name(env_data)

    # Substitute variables in template
    var_start = "${"
    var_end = "}"

    var_start_index = evaluated_template.find(var_start)

    while var_start_index != -1:
        var_end_index = evaluated_template.find(var_end, var_start_index)
        var_name = evaluated_template[var_start_index + len(var_start):var_end_index]
        var_value = env_data.get(var_name)

        if not var_value:
            raise Exception(f"Variable '{var_name}' not found in env data")

        # TODO: Consider doing it another way to avoid manually parsing while still using redundant `replace()`
        evaluated_template = evaluated_template.replace(f"{var_start}{var_name}{var_end}", var_value)
        var_start_index = evaluated_template.find(var_start, var_start_index)

    # Parse evaluated template
    return EnvDesc(json.loads(evaluated_template))


def _get_sub_id(env_data: dict):
    if "common_plan_id" not in env_data:
        raise Exception("'common_plan_id' not found in environment data")

    common_plan_id = env_data["common_plan_id"]
    return common_plan_id.split("/")[2]


def _construct_ingress_eh_url(env_data: dict):
    if "common_eventhub_namespace" not in env_data and "ingress_eventhub_name" not in env_data:
        raise Exception("'common_eventhub_namespace' or 'ingress_eventhub_name' not found in environment data")

    eh_namespace = env_data["common_eventhub_namespace"]
    ingress_eh_name = env_data["ingress_eventhub_name"]

    return f"https://{eh_namespace}.servicebus.windows.net/{ingress_eh_name}"


def _get_stamp_tag(env_data: dict):
    if "environment" not in env_data and "shloc" not in env_data and "stamp" not in env_data:
        raise Exception("'environment' or 'shloc' or 'stamp' not found in environment data")

    return f"{env_data['environment']}-{env_data['shloc']}-{env_data['stamp']}"


def _get_env_tag(env_data: dict):
    if "environment" not in env_data and "shloc" not in env_data and "stamp" not in env_data \
            and "suffix" not in env_data:
        raise Exception("'environment' or 'shloc' or 'stamp' or 'suffix' not found in environment data")

    return f"{env_data['environment']}-{env_data['shloc']}-{env_data['stamp']}{env_data['suffix']}"


def _get_frontend_storage_name(env_data: dict):
    if "frontend_url" not in env_data:
        raise Exception("'frontend_url' not found in environment data")

    url = env_data["frontend_url"]

    return urlparse(url).netloc.split(".")[0]


def _get_blob_container_client():
    credential = azure_utility.get_azure_credential()
    blob_account_url = f"https://{get_env_data_storage_name()}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(blob_account_url, credential=credential)
    return blob_service_client.get_container_client(DEF_CONTAINER_NAME)
