from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

# - create_virtual_resource(resource_data)
# - delete_virtual_resource(resource_id)
# - list_virtual_resources_advanced()
# - modify_virtual_resource(resource_id, **kwargs)
# - read_virtual_resource(resource_id)
# - set_limit_on_virtual_resource(resource_id, limit)

class VirtualResources:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_virtual_resource(self):
        url = "/virtual/list"
        response = self.uc.get(url)
        return response