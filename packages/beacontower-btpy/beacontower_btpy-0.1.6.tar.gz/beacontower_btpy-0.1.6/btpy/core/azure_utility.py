from azure.identity import AzureCliCredential, DefaultAzureCredential


def get_azure_credential():
    return AzureCliCredential()
    # return DefaultAzureCredential()


def to_azure_appsetting_format(setting_value: str) -> str:
    return setting_value.replace(":", "__")


def from_azure_appsetting_format(setting_value: str) -> str:
    return setting_value.replace("__", ":")
