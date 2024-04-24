from .utils import prepare_query_params, prepare_payload

# Missing
# - delete_oms_server(oms_id)
# - modify_oms_server(oms_id, **kwargs)


class OmsServers:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_oms_servers(self):
        url = "/omsserver/list"
        response = self.uc.get(url)
        return response

    def read_oms_server(self, query=None, **args):
        """
        Read OMS server details.
        Args:
        - query: Query parameters
        Args:
        - server_id: Server ID
        - server_address: Server address
        """
        url = "/omsserver"
        field_mapping = {
            "server_id": "serverid", 
            "server_address": "serveraddress" 
        }
        parameters = prepare_query_params(query, field_mapping, args)

        response = self.uc.get(url, query=parameters)
        return response

    def create_oms_server(self, payload=None, **args):
        url = "/omsserver"
        field_mapping = {
            "server_address": "serverAddress"
        }
        payload = prepare_payload(payload, field_mapping, args)
        response = self.uc.post(url, json_data=payload, parse_response=False)
        return response