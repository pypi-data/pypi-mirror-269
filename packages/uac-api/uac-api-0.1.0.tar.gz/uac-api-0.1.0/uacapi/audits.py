from .utils import append_if_not_none, set_if_not_none, set_if_not_equal
import json

class Audits:
    def __init__(self, uc):
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc

    def list_audits(self, payload=None, **args):
        '''
        payload: Payload of the request
        Args Mapping:
        - type: auditType
        - source: source
        - updated_time: updatedTime
        - updated_time_type: updatedTimeType
        - include_child_audit: includeChildAudits
        - created_by: createdBy
        - status: status
        - table_record_name(or name): tableRecordName
        - table_name (or table): tableName
        - table_key (or key): tableKey
        '''
        url = "/audit/list"
        if payload is not None:
            _payload = payload
        else:
            _payload = { }

            field_mapping = {
                "type": "auditType",
                "source": "source",
                "updated_time": "updatedTime",
                "updated_time_type": "updatedTimeType",
                "include_child_audit": "includeChildAudits",
                "created_by": "createdBy",
                "status": "status",
                "table_record_name": "tableRecordName",
                "table_name": "tableName",
                "table_key": "tableKey",
                "name": "tableRecordName",
                "table": "tableName",
                "key": "tableKey"
            }

            # Process additional arguments (**args)
            for arg_key, arg_value in args.items():
                if arg_key in field_mapping:
                    _payload[field_mapping[arg_key]] = arg_value

        response = self.uc.post(url, json_data=_payload)
        return response