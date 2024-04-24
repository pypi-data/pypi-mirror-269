# PyUC-API - Api Wrapper for Universal Controller REST API


# Agents

- delete_agent(agent_id)
- list_agents()
- list_agents_advanced()
- modify_agent(agent_id, **kwargs)
- read_agent(agent_id)
- resume_agent(agent_id)
- set_agent_task_execution_limit(agent_id, limit)
- suspend_agent(agent_id)
- create_agent_cluster(cluster_data)
- delete_agent_cluster(cluster_id)
- list_agent_clusters()
- modify_agent_cluster(cluster_id, **kwargs)
- read_agent_cluster(cluster_id)
- resume_agent_cluster(cluster_id)
- resume_agent_cluster_membership(cluster_id, agent_id)
- return_agent_from_agent_cluster(cluster_id, agent_id)
- set_agent_cluster_task_execution_limit(cluster_id, limit)
- suspend_agent_cluster(cluster_id)
- suspend_agent_cluster_membership(cluster_id, agent_id)

# Audit Records

- list_audit_records()

# Bundles

- bundle_report()
- create_bundle(bundle_data)
- delete_bundle(bundle_id)
- list_bundles()
- modify_bundle(bundle_id, **kwargs)
- read_bundle(bundle_id)
- bundleless_promotion()
- cancel_scheduled_bundle_promotion(promotion_id)
- delete_scheduled_bundle_promotion(promotion_id)
- promote_bundle_or_schedule_bundle_promotion(bundle_id, promotion_data)
- create_promotion_target(target_data)
- modify_promotion_target(target_id, **kwargs)
- list_promotion_targets()
- delete_promotion_target(target_id)
- read_promotion_target(target_id)
- refresh_target_agents(target_id)

# Business Services

- create_business_service(service_data)
- delete_business_service(service_id)
- list_business_services()
- modify_business_service(service_id, **kwargs)
- read_business_service(service_id)

# Calendars

- add_existing_custom_day_to_calendar(calendar_id, custom_day_id)
- create_calendar(calendar_data)
- delete_calendar(calendar_id)
- list_calendars()
- modify_calendar(calendar_id, **kwargs)
- read_calendar(calendar_id)
- read_all_custom_days_of_calendar(calendar_id)
- remove_custom_day_from_calendar(calendar_id, custom_day_id)

# Cluster Nodes

- list_cluster_nodes()
- read_current_cluster_node()

# Connections

- database_connections()
- email_connections()
- email_templates()
- peoplesoft_connections()
- sap_connections()
- snmp_managers()

# Credentials

- create_credential(credential_data)
- delete_credential(credential_id)
- list_credentials()
- modify_credential(credential_id, **kwargs)
- read_credential(credential_id)

# Custom Days

- create_custom_day(custom_day_data)
- delete_custom_day(custom_day_id)
- list_custom_day_qualifying_dates(custom_day_id)
- list_custom_day_qualifying_periods(custom_day_id)
- list_custom_days()
- list_local_custom_day_qualifying_dates(custom_day_id)
- list_local_custom_day_qualifying_periods(custom_day_id)
- modify_custom_day(custom_day_id, **kwargs)
- read_custom_day(custom_day_id)

# Groups

- create_group(group_data)
- delete_group(group_id)
- list_groups()
- modify_group(group_id, **kwargs)
- read_group(group_id)

# LDAP

- read_ldap_settings()
- update_ldap_settings(ldap_settings_data)
- update_ldap_bind_password(password)

# Metrics

- universal_controller_metrics_prometheus()

# OAuth Clients

- create_oauth_client(client_data)
- modify_oauth_client(client_id, **kwargs)
- read_oauth_client(client_id)
- delete_oauth_client(client_id)
- list_oauth_clients()

# OMS Servers

- delete_oms_server()
- modify_oms_server()
- def list_oms_servers(self):
- def read_oms_server(self, query=None, **args):
- def create_oms_server(self, payload=None, **args):

# Other

- change_universal_controller_user_password(password)
- change_runtime_password_on_credentials(credential_id, password)
- list_properties()
- modify_property(property_name, value)
- read_property(property_name)
- run_report(report_data)

# Scripts

- create_script(script_data)
- delete_script(script_id)
- list_scripts()
- modify_script(script_id, **kwargs)
- read_script(script_id)

# Simulations

- create_update_simulation(simulation_data)
- delete_simulation(simulation_id)
- list_simulations()
- read_simulation(simulation_id)

# System

- retrieve_system_details()

# Task Instance

- cancel_task_instance(instance_id)
- clear_all_dependencies(instance_id)
- clear_exclusive_dependencies(instance_id)
- clear_instance_wait_dependencies(instance_id)
- clear_predecessor_dependencies(instance_id)
- clear_time_dependency(instance_id)
- clear_virtual_resource_dependencies(instance_id)
- delete_task_instance(instance_id)
- force_finish_task_instance(instance_id)
- force_finish_cancel_task_instance(instance_id)
- hold_task_instance(instance_id)
- issue_set_completed_command_for_manual_task_instance(instance_id)
- issue_set_started_command_for_manual_task_instance(instance_id)
- list_task_instances()
- list_task_instances_advanced()
- list_task_instance_variables_show_variables(instance_id)
- release_task_from_hold(instance_id)
- rerun_task_instance(instance_id)
- retrieve_task_instance_output(instance_id)
- set_or_modify_wait_time_duration_for_task_instance(instance_id, wait_time)
- set_priority_for_task_instance(instance_id, priority)
- skip_task_instance(instance_id)
- skip_task_instance_path(instance_id)
- unskip_task_instance(instance_id)

# Tasks

- create_task(task_data)
- delete_task(task_id)
- launch_task(task_id)
- list_tasks()
- list_tasks_advanced()
- modify_task(task_id, **kwargs)
- read_task(task_id)

# Triggers

- assign_execution_user_to_trigger(trigger_id, user_name)
- create_trigger(trigger_data)
- delete_trigger(trigger_id)
- enable_disable_trigger(trigger_id, enable=True)
- list_trigger_qualifying_times(trigger_id)
- list_triggers()
- list_triggers_advanced()
- modify_trigger(trigger_id, **kwargs)
- modify_time_of_time_trigger(trigger_id, new_time)
- read_trigger(trigger_id)
- trigger_now(trigger_id)
- unassign_execution_user_from_trigger(trigger_id)

# Universal Events

- universal_event_publishing()

# Universal Event Templates

- create_universal_event_template(template_data)
- delete_universal_event_template(template_id)
- list_universal_event_templates()
- modify_universal_event_template(template_id, **kwargs)
- read_universal_event_template(template_id)

# Universal Templates

- create_universal_template(template_data)
- delete_universal_template(template_id)
- list_universal_templates()
- modify_universal_template(template_id, **kwargs)
- read_universal_template(template_id)
- restore_default_universal_template_icon(template_id)
- set_universal_template_icon(template_id, icon_data)
- universal_template_delete_extension_archive(template_id)
- universal_template_download_extension_archive(template_id)
- universal_template_upload_extension_archive(template_id, file_data)
- universal_template_export(template_id)
- universal_template_import(file_data)

# Users

- create_user(user_data)
- create_personal_access_token(user_name)
- delete_user(user_name)
- list_personal_access_tokens(user_name)
- list_users()
- modify_user(user_name, **kwargs)
- read_user(user_name)
- revoke_personal_access_token(user_name, token_id)

# Variables

- create_global_variable(variable_data)
- delete_global_variable(variable_name)
- list_variables()
- list_variables_advanced()
- modify_global_variable(variable_name, **kwargs)
- read_global_variable(variable_name)
- set_variables(variable_data)

# Virtual Resources

- create_virtual_resource(resource_data)
- delete_virtual_resource(resource_id)
- list_virtual_resources()
- list_virtual_resources_advanced()
- modify_virtual_resource(resource_id, **kwargs)
- read_virtual_resource(resource_id)
- set_limit_on_virtual_resource(resource_id, limit)

# Webhooks

- assign_execution_user_to_webhook(webhook_id, execution_user)
- disable_webhook(webhook_id)
- enable_webhook(webhook_id)
- enable_disable_multiple_webhooks(webhook_ids, enable=True)
- list_webhooks()
- modify_webhooks(webhook_id, **kwargs)
- read_webhook(webhook_id)
- register_webhook(webhook_data)
- unassign_execution_user_from_webhook(webhook_id)
- unregister_webhook(webhook_id)

# Workflows

- insert_task_into_workflow_with_dependencies(workflow_id, task_data, dependencies)
- list_predecessors_successors_of_task_instance_in_a_workflow(workflow_id, instance_id)
- create_workflow(workflow_data)
- list_workflow_forecast(workflow_id)
- modify_workflow(workflow_id, **kwargs)
- read_workflow(workflow_id)