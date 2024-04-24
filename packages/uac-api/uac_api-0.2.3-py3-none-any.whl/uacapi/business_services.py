from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

# - create_business_service(service_data)
# - delete_business_service(service_id)
# - modify_business_service(service_id, **kwargs)
# - read_business_service(service_id)

class BusinessServices:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_business_services(self):
        url = "/businessservice/list"
        response = self.uc.get(url)
        return response