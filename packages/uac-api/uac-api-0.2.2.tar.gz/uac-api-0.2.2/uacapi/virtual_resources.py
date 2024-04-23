from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class VirtualResources:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_virtual_resource(self):
        url = "/virtual/list"
        response = self.uc.get(url)
        return response