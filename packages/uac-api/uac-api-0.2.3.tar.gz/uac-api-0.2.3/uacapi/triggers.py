# - assign_execution_user_to_trigger(trigger_id, user_name)
# - create_trigger(trigger_data)
# - delete_trigger(trigger_id)
# - enable_disable_trigger(trigger_id, enable=True)
# - list_trigger_qualifying_times(trigger_id)
# - list_triggers()
# - list_triggers_advanced()
# - modify_trigger(trigger_id, **kwargs)
# - modify_time_of_time_trigger(trigger_id, new_time)
# - read_trigger(trigger_id)
# - trigger_now(trigger_id)
# - unassign_execution_user_from_trigger(trigger_id)

class Triggers:
    def __init__(self, uc):
        self.log = uc.log
        self.headers = uc.headers
        self.uc = uc
