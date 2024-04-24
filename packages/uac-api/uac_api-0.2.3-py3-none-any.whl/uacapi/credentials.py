

# - create_credential(credential_data)
# - delete_credential(credential_id)
# - list_credentials()
# - modify_credential(credential_id, **kwargs)
# - read_credential(credential_id)

class Credentials:
    def __init__(self, uc):
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc
