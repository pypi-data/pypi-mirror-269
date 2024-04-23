from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class Scripts:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def script_list(self):
        url = "/script/list"
        response = self.uc.get(url)
        return response

    def script_read(self, name=None, sysid=None):
        url = "/script"
        parameters = []
        append_if_not_none(parameters, name, "scriptname={var}")
        append_if_not_none(parameters, sysid, "scriptid={var}")
        response = self.uc.get(url, query=parameters)
        return response

    def script_modify(self, payload):
        url = "/script"
        response = self.uc.put(url, query="", json_data=payload)
        return response

    def script_create(self, payload):
        url = "/script"
        response = self.uc.post(url, query="", json_data=payload)
        return response

    def script_delete(self, name=None, sysid=None):
        url = "/script"
        parameters = []
        append_if_not_none(parameters, name, "scriptname={var}")
        append_if_not_none(parameters, sysid, "scriptid={var}")
        response = self.uc.delete(url, query=parameters)
        return response