from .utils import prepare_payload

class Scripts:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc
        self.field_mapping = {
            "script_name": "scriptname",
            "script_id": "scriptid",
        }

    def list_scripts(self):
        url = "/script/list"
        response = self.uc.get(url)
        return response

    def read_script(self, query=None, **args):
        """
        Read script details.
        Args:
        - query: Query parameters
        Args:
        - script_id: Script ID
        - script_name: Script name
        """
        url = "/script"
        parameters = prepare_payload(query, self.field_mapping, args)
        response = self.uc.get(url, query=parameters)
        return response

    def modify_script(self, payload):
        url = "/script"
        response = self.uc.put(url, query="", json_data=payload)
        return response

    def create_script(self, payload):
        url = "/script"
        response = self.uc.post(url, query="", json_data=payload)
        return response

    def delete_script(self, query=None, **args):
        """
        Delete script.
        Args:
        - query: Query parameters
        Args:
        - script_id: Script ID
        - script_name: Script name
        """
        url = "/script"
        parameters = prepare_payload(query, self.field_mapping, args)
        response = self.uc.delete(url, query=parameters)
        return response