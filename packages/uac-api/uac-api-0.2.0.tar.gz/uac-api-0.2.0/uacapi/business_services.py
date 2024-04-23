from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class BusinessServices:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def business_service_list(self):
        url = "/businessservice/list"
        response = self.uc.get(url)
        return response