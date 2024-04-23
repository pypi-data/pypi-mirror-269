from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

class Tasks:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_tasks_advanced(self, query=None, task_name="*", **args):
        url = "/task/listadv"
        if query is not None:
            parameters = query
        else:
            parameters = [f"taskname={task_name}"]
            field_mapping = {
                "business_service": "businessServices",
                "type": "type",
                "updated_time": "updatedTime",
                "updated_time_type": "updatedTimeType",
                "workflow_id": "workflowid",
                "workflow_name": "workflowname",
            }
            for field, var in args.items():
                if field in field_mapping:
                    append_if_not_none(parameters, field, var + "={var}")

        response = self.uc.get(url, query=parameters)
        return response
    
    def read_task(self, name=None, sysid=None):
        url = "/task"
        parameters = []
        append_if_not_none(parameters, name, "taskname={var}")
        append_if_not_none(parameters, sysid, "taskid={var}")
        response = self.uc.get(url, query=parameters)
        return response

    def modify_task(self, payload):
        url = "/task"
        response = self.uc.put(url, query="", json_data=payload)
        return response
    
    def create_task(self, payload):
        url = "/task"
        response = self.uc.post(url, query="", json_data=payload)
        return response
    
    def launch_task(self, payload=None, **args):
        url = "/task/ops-task-launch"
        if payload is not None:
            _payload = payload
        else:
            _payload = { }

            field_mapping = {
                "hold": "hold",
                "hold_reason": "holdReason",
                "launch_reason": "launchReason",
                "name": "name",
                "simulate": "simulate",
                "time_zone": "timeZone",
                "vertices": "vertices",
                "variables": "Variables",
                "virtual_resources": "virtualResources",
            }

            # Process additional arguments (**args)
            for arg_key, arg_value in args.items():
                if arg_key in field_mapping:
                    _payload[field_mapping[arg_key]] = arg_value

        response = self.uc.post(url, json_data=payload)
        return response