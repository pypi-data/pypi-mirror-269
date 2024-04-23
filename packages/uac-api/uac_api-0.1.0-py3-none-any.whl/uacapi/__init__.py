import requests
import sys
import json
from .universal_events import UniversalEvents
from .audits import Audits

from .utils import strip_url

__version__ = "0.1.0"

class UniversalController():
    def __init__(self, base_url, credential=None, token=None, ssl_verify=True, logger=None, headers=None) -> None:
        self.log = logger
        self.base_url = strip_url(base_url)
        self.token = token
        self.ssl_verify = ssl_verify
        self.cridential = credential
        if headers:
            self.headers = headers
        else:
            self.headers = {"content-type": "application/json"}
        self.universal_events = UniversalEvents(self)
        self.audits = Audits(self)

    def post(self, resource, query="", json_data=None, headers=None, parse_response=True):
        return self.call("POST", resource, query, headers, json_data, parse_response)

    def put(self, resource, query="", json_data=None, headers=None, parse_response=True):
        return self.call("PUT", resource, query, headers, json_data, parse_response)

    def get(self, resource, query="", headers=None, parse_response=True):
        return self.call("GET", resource, query, headers, json_data=None, parse_response=parse_response)

    def delete(self, resource, query="", json_data=None, headers=None, parse_response=True):
        return self.call("DELETE", resource, query, headers, json_data, parse_response)

    def call(self, method, resource, query, headers, json_data, parse_response):
        self.log.debug("uac_rest_call start")
        if headers:
            _headers = headers
        else:
            _headers = self.headers
        
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

        if len(query) > 0:
            query = "?" + "&".join(query)
        uri = f"{self.base_url}/resources{resource}{query}"
        self.log.info(f"URL = {uri}")
        try:
            if method == "GET":
                response = requests.get(uri,
                                        headers=_headers,
                                        auth=self.cridential,
                                        verify=self.ssl_verify)
            elif method == "POST":
                self.log.debug(f"Payload = {json_data}")
                response = requests.post(uri,
                                        headers=_headers,
                                        auth=self.cridential,
                                        json=json_data,
                                        verify=self.ssl_verify)
            elif method == "DELETE":
                response = requests.delete(uri,
                                        headers=_headers,
                                        auth=self.cridential,
                                        json=json_data,
                                        verify=self.ssl_verify)
            elif method == "PUT":
                response = requests.put(uri,
                                        headers=_headers,
                                        auth=self.cridential,
                                        json=json_data,
                                        verify=self.ssl_verify)
            else:
                self.log.error(f"Unknown method {method}")
                raise
        except Exception as unknown_exception:
            self.log.error(f"Error Calling{self.base_url} API {sys.exc_info()}")
            raise
        if response.ok:
            pass
        else:
            self.log.error(f"{uri} Response Code : {response.status_code}")
            self.log.error(f"Failed with reason : {response.text}")
            response = None
            raise
        # if response:
        #     self.log.debug("response: " + response.text)
        resp_data = None
        try:
            if parse_response:
                resp_data = response.json()
                self.log.debug("received data: %s..." % json.dumps(resp_data))
            else:
                resp_data = response.text
                self.log.debug("received data: %s..." % resp_data)
        except Exception as unknown_exception:
            # no XML returned
            self.log.error("Couldn't parse the response.")
            resp_data = response.text
        self.log.debug("received data: %s..." % json.dumps(resp_data)[0:10])
        self.log.debug("uac_rest_call end")
        return resp_data

    # Universal Events
    def push_event(self, event_name, payload):
        return self.universal_events.push_event(event_name, payload)

    # Audits
    def list_audits(self):
        return self.audits.list_audits()

    