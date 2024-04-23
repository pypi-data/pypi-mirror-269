from .utils import append_if_not_none, set_if_not_none, set_if_not_equal

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
        if query is not None:
            parameters = query
        else:
            parameters = []
            field_mapping = {
                "agent_id": "agentid",
                "name": "agentname",
                "agent_name": "agentname",
                "id": "agentid"
            }
            for field, var in args.items():
                if field in field_mapping:
                    append_if_not_none(parameters, var, field_mapping[field] + "={var}")

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
        if query is not None:
            parameters = query
        else:
            parameters = []
            field_mapping = {
                "type": "type",
                "name": "agentname",
                "agent_name": "agentname",
                "business_services": "businessServices"
            }
            for field, var in args.items():
                if field in field_mapping:
                    append_if_not_none(parameters, var, field_mapping[field] + "={var}")
        
        response = self.uc.get(url, query=parameters)