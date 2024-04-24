from .utils import append_if_not_none, prepare_payload, prepare_query_params

# - delete_agent(agent_id)
# - modify_agent(agent_id, **kwargs)
# - resume_agent(agent_id)
# - set_agent_task_execution_limit(agent_id, limit)
# - suspend_agent(agent_id)
# - create_agent_cluster(cluster_data)
# - delete_agent_cluster(cluster_id)
# - list_agent_clusters()
# - modify_agent_cluster(cluster_id, **kwargs)
# - read_agent_cluster(cluster_id)
# - resume_agent_cluster(cluster_id)
# - resume_agent_cluster_membership(cluster_id, agent_id)
# - return_agent_from_agent_cluster(cluster_id, agent_id)
# - set_agent_cluster_task_execution_limit(cluster_id, limit)
# - suspend_agent_cluster(cluster_id)
# - suspend_agent_cluster_membership(cluster_id, agent_id)

class Agents:
    def __init__(self, uc) -> None:
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def read_agent(self, query=None, **args):
        """
        Read agent
        :param query:
        :Argument Mappings:
        - id (or agent_id): agentid
        - name (or agent_name): agentname
        :return:
        Agent object
        """
        url = "/agent"
        
        field_mapping = {
            "agent_id": "agentid",
            "name": "agentname",
            "agent_name": "agentname",
            "id": "agentid"
        }
        
        parameters = prepare_query_params(query, field_mapping, args)
        response = self.uc.get(url, query=parameters)
        return response
    
    def list_agents(self):
        """
        List agents
        :return:
        List of agents
        """
        url = "/agent/list"
        response = self.uc.get(url)
        return response
    
    def list_agents_advanced(self, query=None, **args):
        """
        List agents advanced
        :param query:
        :Argument Mappings:
        - type: type
        - name (or agent_name): agentname
        - business_services: businessServices
        :return:
        List of agents
        """
        url = "/agent/listadv"
        field_mapping = {
            "type": "type",
            "name": "agentname",
            "agent_name": "agentname",
            "business_services": "businessServices"
        }

        parameters = prepare_query_params(query, field_mapping, args)
        response = self.uc.get(url, query=parameters)