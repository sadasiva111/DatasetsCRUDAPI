import re

def validate_dataset_data(data):
    error_message = ""
    field_types = {
        "id": int,
        "dataset_id": str,
        "type": str,
        "name": str,
        "validation_config": dict,
        "extraction_config": dict,
        "dedup_config": dict,
        "data_schema": dict,
        "denorm_config": dict,
        "router_config": dict,
        "dataset_config": dict,
        "tags": dict,
        "data_version": int,
        "status": str,
        "created_by": str,
        "updated_by": str,
        "created_date": str,
        "updated_date": str,
        "published_date": str
    }

    required_fields = [ "dataset_id", "type", "published_date", "updated_date", "created_date"]
    optional_fields = list(set(field_types.keys()) - set(required_fields))

    date_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$'

    for field in required_fields:
        if field not in data:
            error_message = f"Missing required field: {field}"
            return False, error_message
        if not isinstance(data[field], field_types[field]):
            error_message = f"Invalid data type for '{field}'. Expected {field_types[field].__name__}."
            return False, error_message

    for field in optional_fields:
        if field in data and not isinstance(data[field], field_types[field]):
            error_message = f"Invalid data type for '{field}'. Expected {field_types[field].__name__}."
            return False, error_message

    for date_field in ["created_date", "updated_date", "published_date"]:
        if date_field in data and not re.match(date_pattern, data[date_field]):
            error_message = f"Invalid format for '{date_field}'. Expected YYYY-MM-DD HH:MM:SS.SSS."
            return False, error_message

    return True, error_message

def validate_request_data(data):
    if not data:
        return False, "No json data is given"
    return True, None

def validate_id(id):
    if not id:
        return False, "No id given"
    return True, None
