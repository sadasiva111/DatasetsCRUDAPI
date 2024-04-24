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
    }

    required_fields = [ "dataset_id", "type"]
    # optional_fields = list(set(field_types.keys()) - set(required_fields))

    for field in required_fields:
        if field not in data:
            error_message = f"Missing required field: {field}"
            return False, error_message
        if not isinstance(data[field], field_types[field]):
            error_message = f"Invalid data type for '{field}'. Expected {field_types[field].__name__}."
            return False, error_message

    # for field in optional_fields:
    #     if field in data and not isinstance(data[field], field_types[field]):
    #         error_message = f"Invalid data type for '{field}'. Expected {field_types[field].__name__}."
    #         return False, error_message

    return True, error_message

def validate_request_data(data):
    if not data:
        return False, "No json data is given"
    return True, None

def validate_id(id):
    if not id:
        return False, "No id given"
    return True, None
