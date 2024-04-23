from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class CustomDays:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_custom_day(self):
        url = "/customday/list"
        response = self.uc.get(url)
        return response
    
    def read_custom_day(self, name=None, sysid=None):
        url = "/customday"
        parameters = []
        append_if_not_none(parameters, name, "customdayname={var}")
        append_if_not_none(parameters, sysid, "customdayid={var}")
        response = self.uc.get(url, query=parameters)
        return response
    
    def modify_custom_day(self, payload):
        url = "/customday"
        response = self.uc.put(url, query="", json_data=payload)
        return response