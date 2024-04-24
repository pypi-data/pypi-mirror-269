from .utils import prepare_payload, prepare_query_params

# - cancel_task_instance(instance_id)
# - clear_all_dependencies(instance_id)
# - clear_exclusive_dependencies(instance_id)
# - clear_instance_wait_dependencies(instance_id)
# - clear_predecessor_dependencies(instance_id)
# - clear_time_dependency(instance_id)
# - clear_virtual_resource_dependencies(instance_id)
# - delete_task_instance(instance_id)
# - force_finish_task_instance(instance_id)
# - force_finish_cancel_task_instance(instance_id)
# - hold_task_instance(instance_id)
# - issue_set_completed_command_for_manual_task_instance(instance_id)
# - issue_set_started_command_for_manual_task_instance(instance_id)
# - list_task_instances_advanced()
# - list_task_instance_variables_show_variables(instance_id)
# - release_task_from_hold(instance_id)
# - retrieve_task_instance_output(instance_id)
# - set_or_modify_wait_time_duration_for_task_instance(instance_id, wait_time)
# - set_priority_for_task_instance(instance_id, priority)
# - skip_task_instance(instance_id)
# - skip_task_instance_path(instance_id)
# - unskip_task_instance(instance_id)

class TaskInstances:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def get_task_instance(self, payload=None, **args):
        url = "/taskinstance/list"
        field_mapping = {
            "task_instance_id": "sysId"
        }
        
        _payload = prepare_payload(payload, field_mapping, args)
        response = self.uc.post(url, json_data=_payload)
        if len(response) == 1:
            return response[0]
        else:
            return None

    def retrieve_output(self, query=None, **args):
        url = "/taskinstance/retrieveoutput"
        field_mapping = {
            "task_instance_id": "taskinstanceid",
            "numlines": "numlines",
            "output_type": "outputtype"
        }
        parameters = prepare_query_params(query, field_mapping, args)
        response = self.uc.get(url, query=parameters)
        return response

    def rerun_task_instance(self, payload=None, **args):
        url = "/taskinstance/rerun"
        field_mapping = {
            "task_instance_id": "id"
        }
        _payload = prepare_payload(payload, field_mapping, args)
        
        response = self.uc.post(url, json_data=_payload)
        return response

    def list_task_instances(self, payload=None, **args):
        """
        List task instances
        Args:
        - agent_name: Agent name
        - business_services: Business services
        - custom_field_1: Custom field 1
        - custom_field_2: Custom field 2
        - execution_user: Execution user
        - instance_number: Instance number
        - late: Late
        - late_early: Late or early
        - name: Name
        - operational_memo: Operational memo
        - status: Status
        - status_description: Status description
        - sys_id: Sys ID
        - task_id: Task ID
        - task_name: Task name
        - template_id: Template ID
        - template_name: Template name
        - trigger_id: Trigger ID
        - trigger_name: Trigger name
        - type: Type
        - updated_time: Updated time
        - updated_time_type: Updated time type
        - workflow_definition_id: Workflow definition ID
        - workflow_definition_name: Workflow definition name
        - workflow_instance_criteria: Workflow instance criteria
        - workflow_instance_id: Workflow instance ID
        - workflow_instance_name: Workflow instance name
        """
        url = "/taskinstance/list"

        field_mapping = {
            "agent_name": "agentName",
            "business_services": "businessServices",
            "custom_field_1": "customField1", 
            "custom_field_2": "customField2", 
            "execution_user": "executionUser",
            "instance_number": "instanceNumber",
            "late": "late", 
            "late_early": "lateEarly", 
            "name": "name",
            "operational_memo": "operationalMemo",
            "status": "status",
            "status_description": "statusDescription",
            "sys_id": "sysId",
            "task_id": "taskId",
            "task_name": "taskName",
            "template_id": "templateId",
            "template_name": "templateName",
            "trigger_id": "triggerId",
            "trigger_name": "triggerName",
            "type": "type", 
            "updated_time": "updatedTime", 
            "updated_time_type": "updatedTimeType",
            "workflow_definition_id": "workflowDefinitionId",
            "workflow_definition_name": "workflowDefinitionName",
            "workflow_instance_criteria": "workflowInstanceCriteria", 
            "workflow_instance_id": "workflowInstanceId",
            "workflow_instance_name": "workflowInstanceName" 
        }


        _payload = prepare_payload(payload, field_mapping, args)
            
        response = self.uc.post(url, json_data=_payload)
        return response