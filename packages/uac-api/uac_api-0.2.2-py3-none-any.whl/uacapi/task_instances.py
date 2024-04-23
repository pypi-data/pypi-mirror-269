from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class TaskInstances:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def get_task_instance(self, payload=None, task_instance_id=None):
        url = "/taskinstance/list"
        if payload is not None:
            _payload = payload
        else:
            _payload = {
                "sysId": task_instance_id
            }
        
        response = self.uc.post(url, json_data=_payload)
        if len(response) == 1:
            return response[0]
        else:
            return None

    def retrieve_output(self, parameters=None, task_instance_id=None, numlines=100):
        url = "/taskinstance/retrieveoutput"
        if parameters is not None:
            _parameters = parameters
        else:
            _parameters = []
            _parameters.append(f"taskinstanceid={task_instance_id}")
            _parameters.append(f"numlines={numlines}")
            _parameters.append("outputtype=OUTERR")
        response = self.uc.get(url, query=_parameters)
        return response

    def rerun(self, payload=None, task_instance_id=None):
        url = "/taskinstance/rerun"
        if payload is not None:
            _payload = payload
        else:
            _payload = {
                "id": task_instance_id
            }
        
        response = self.uc.post(url, json_data=_payload)
        return response
