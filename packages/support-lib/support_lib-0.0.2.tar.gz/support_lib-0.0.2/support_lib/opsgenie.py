import opsgenie_sdk
from opsgenie_sdk.rest import ApiException


class OpsGenie(object):

    def __init__(self, opsgenie_url, opsgenie_api_key):
        self.opsgenie_url = opsgenie_url
        self.opsgenie_api_key = opsgenie_api_key
        configuration = opsgenie_sdk.Configuration()
        configuration.host = self.opsgenie_url
        configuration.api_key['Authorization'] = self.opsgenie_api_key
        self.api_instance = opsgenie_sdk.AlertApi(opsgenie_sdk.ApiClient(configuration))

    def create_alert(self, payload):
        try:
            response = self.api_instance.create_alert(payload)
        except ApiException as e:
            return f"Exception when calling AlertApi->{e}"
        return response
