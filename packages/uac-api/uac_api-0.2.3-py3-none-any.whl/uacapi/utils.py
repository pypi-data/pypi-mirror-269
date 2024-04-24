import json, re
import requests
import os
from datetime import datetime

def append_if_not_none(list_name, variable, format, exclude_empty=True):
    if "{}" in format:
        format = format.replace("{}", "{var}")

    if variable is not None:
        if exclude_empty: # we don't want empty records
            if len(variable) == 0:
                return
        _value = format.format(var=requests.utils.quote(variable, safe='()'))
        list_name.append(_value)


def set_if_not_none(_dict, field, value, format="{}", exclude_empty=True):
    if value is None:
        return
    
    if exclude_empty: # we don't want empty records
        if len(value) == 0:
            return
    set_if_not_equal(_dict, field, value, None, format=format)


def set_if_not_equal(_dict, field, value, default, format="{}"):
    if value != default:
        if "{}" in format:
            format = format.replace("{}", "{var}")
        _value = format.format(var=value)

        _dict[field] = _value


def format_json(json_obj):
    json_string = json.dumps(json_obj, indent=4, sort_keys=True)
    json_string = re.sub(r"\n\s*\{", " {", json_string)
    json_string = re.sub(r"\n\s*\]", " ]", json_string)
    json_string = re.sub(r"\[\],", "[ ],", json_string)
    json_string = re.sub(r"\":(\s*[^\n]+)", "\" :\\1", json_string)
    return json_string


def strip_url(url):
    return url.strip('/').strip(' ')


def get_first_element(_list, default=None):
    if len(_list) == 0:
        return default
    else:
        return _list[0]


def is_xml(response):
    content_type = response.headers.get("Content-Type")
    if content_type is None:
        return False
    return "xml" in content_type


def is_json(response):
    content_type = response.headers.get("Content-Type")
    if content_type is None:
        return False
    return "json" in content_type

def is_sql_statement(string):
    """Checks if a string is a SQL statement.

    Args:
        string: The string to be checked.

    Returns:
        True if the string is a SQL statement, False otherwise.
    """

    sql_keywords = [
        "SELECT", "FROM", "WHERE", "ORDER BY", "GROUP BY", "HAVING", "INSERT INTO",
        "UPDATE", "DELETE", "CREATE TABLE", "ALTER TABLE", "DROP TABLE", "CREATE DATABASE",
        "ALTER DATABASE", "DROP DATABASE", "BEGIN TRANSACTION", "COMMIT TRANSACTION",
        "ROLLBACK TRANSACTION"
    ]

    sql_regex = re.compile(r"\b(?:%s)\b" % "|".join(sql_keywords))

    return sql_regex.search(string) is not None

def remove_sysid_tag(json_structure):
    """Removes the "sysId" tag from all list objects in a JSON structure.

    Args:
        json_structure: The JSON structure to be modified.

    Returns:
        The modified JSON structure.
    """

    for list_object in json_structure["actions"].values():
        if isinstance(list_object, list):
            for list_object_item in list_object:
                if isinstance(list_object_item, dict) and "sysId" in list_object_item:
                    del list_object_item["sysId"]
    
    return json_structure

def convert_to_variable_name(string):
    """Converts a string to a Python variable name format.

    Args:
        string: The string to be converted.

    Returns:
        A string in Python variable name format.
    """

    # Remove all spaces and special characters.
    string = re.sub(r"[^\w]", "_", string)

    # Make the first character lowercase.
    string = string[0].lower() + string[1:]

    return string

def update_ld_library_path(new_path):
    # Get the current value of LD_LIBRARY_PATH
    current_value = os.environ.get('LD_LIBRARY_PATH', '')

    # Add the new path to the current value
    if current_value:
        updated_value = f"{current_value}:{new_path}"
    else:
        updated_value = new_path

    return updated_value

def check_ebs_internal_pattern(content):
  """
  Checks if the content includes a pattern like `$Flex$` or `$profile$`.

  Args:
    content: The content to check.

  Returns:
    True if the content includes the pattern, False otherwise.
  """

  pattern = r'\$(\w+)\$\.'
  matches = re.findall(pattern, content)
  if matches:
    return True
  else:
    return False

def update_ebs_fields(json_content):
    try:
        resp_app_short_name = json_content.get("textField1")
        if resp_app_short_name.get("name") == "resp_app_short_name":
            resp_app_short_name["value"] = "${resp_app_short_name}"
        
        responsibility = json_content.get("textField2")
        if responsibility.get("name") == "responsibility":
            responsibility["value"] = "${responsibility}"
        
        program_name = json_content.get("textField4")
        if program_name.get("name") == "program_name":
            program_name["value"] = "${program_name}"

        program_short_name = json_content.get("textField7")
        if program_short_name.get("name") == "program_short_name":
            program_short_name["value"] = "${program_short_name}"
    finally:
        return json_content
    
def prepare_payload(payload, field_mapping, args):
    _payload = None
    if payload is not None:
        _payload = payload
    else:
        _payload = { }
        # Process additional arguments (**args)
        for arg_key, arg_value in args.items():
            if arg_key in field_mapping:
                _payload[field_mapping[arg_key]] = arg_value
    
    return _payload

def prepare_query_params(query, field_mapping, args):
    if query is not None:
        parameters = query
    else:
        parameters = []
        
        for field, var in args.items():
            if field in field_mapping:
                append_if_not_none(parameters, var, field_mapping[field] + "={var}")
        
    return parameters