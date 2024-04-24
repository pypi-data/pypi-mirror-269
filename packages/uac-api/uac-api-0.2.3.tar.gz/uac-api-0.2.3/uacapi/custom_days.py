from .utils import prepare_payload

# - create_custom_day(custom_day_data)
# - delete_custom_day(custom_day_id)
# - list_custom_day_qualifying_dates(custom_day_id)
# - list_custom_day_qualifying_periods(custom_day_id)
# - list_local_custom_day_qualifying_dates(custom_day_id)
# - list_local_custom_day_qualifying_periods(custom_day_id)


class CustomDays:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_custom_day(self):
        url = "/customday/list"
        response = self.uc.get(url)
        return response
    
    def read_custom_day(self, query=None, **args):
        url = "/customday"
        field_mapping = {
            "customday_name": "customdayname",
            "customday_id": "customdayid"
        }
        parameters = prepare_payload(query, field_mapping, args)
        response = self.uc.get(url, query=parameters)
        return response
    
    def modify_custom_day(self, payload):
        url = "/customday"
        response = self.uc.put(url, query="", json_data=payload)
        return response