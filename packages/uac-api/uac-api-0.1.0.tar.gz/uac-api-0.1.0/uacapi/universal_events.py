class UniversalEvents:
    def __init__(self, uc):
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def push_event(self, event_name, payload):
        url = f"/universalevent/push/{event_name}"
        self.log.debug("Launch task payload is {}".format(payload))
        headers = self.headers
        headers["Content-Type"] = "plain/text"
        response = self.uc.post(url, json_data=payload, parse_json=False, headers=headers)
        return response