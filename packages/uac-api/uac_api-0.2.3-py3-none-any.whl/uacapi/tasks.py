from .utils import prepare_query_params, prepare_payload

# - create_task(task_data)
# - delete_task(task_id)
# - launch_task(task_id)
# - list_tasks()
# - list_tasks_advanced()
# - modify_task(task_id, **kwargs)
# - read_task(task_id)

class Tasks:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_tasks_advanced(self, query=None, **args):
        url = "/task/listadv"
        field_mapping = {
            "task_name": "taskName",
            "business_service": "businessServices",
            "type": "type",
            "updated_time": "updatedTime",
            "updated_time_type": "updatedTimeType",
            "workflow_id": "workflowid",
            "workflow_name": "workflowname",
        }
        parameters = prepare_query_params(query, field_mapping, args)

        response = self.uc.get(url, query=parameters)
        return response
    
    def read_task(self, query=None, **args):
        url = "/task"
        field_mapping = {
            "task_name": "taskname",
            "task_id": "taskid",
        }
        parameters = prepare_query_params(query, field_mapping, args)
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
        """
        Launch task.
        Args:
        - payload: Task payload
        - hold: Hold task
        - hold_reason: Hold reason
        - launch_reason: Launch reason
        - name: Task name
        - simulate: Simulate task
        - time_zone: Time zone
        - vertices: Vertices
        - variables: Variables
        - virtual_resources: Virtual resources
        """
        url = "/task/ops-task-launch"
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
        _payload = prepare_payload(payload, field_mapping, args)

        response = self.uc.post(url, json_data=_payload)
        return response