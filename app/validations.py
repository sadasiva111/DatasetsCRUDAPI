import re

def validate_dataset_data(data):
    error_message = ""

    # Validate required fields
    required_fields = ["id", "dataset_id", "type", "name", "validation_config", "extraction_config", "dedup_config",
                       "data_schema", "denorm_config", "router_config", "dataset_config", "tags", "data_version",
                       "status", "created_by", "updated_by", "created_date", "updated_date", "published_date"]
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        error_message = f"Missing required fields: {', '.join(missing_fields)}"
        return False, error_message

    # Validate data types
    if not isinstance(data["id"], int):
        error_message = "Invalid data type for 'id'. Expected int."
        return False, error_message

    if not isinstance(data["dataset_id"], str):
        error_message = "Invalid data type for 'dataset_id'. Expected str."
        return False, error_message

    if not isinstance(data["type"], str):
        error_message = "Invalid data type for 'type'. Expected str."
        return False, error_message

    if not isinstance(data["name"], str):
        error_message = "Invalid data type for 'name'. Expected str."
        return False, error_message

    if not isinstance(data["validation_config"], dict):
        error_message = "Invalid data type for 'validation_config'. Expected dict."
        return False, error_message

    if not isinstance(data["extraction_config"], dict):
        error_message = "Invalid data type for 'extraction_config'. Expected dict."
        return False, error_message

    if not isinstance(data["dedup_config"], dict):
        error_message = "Invalid data type for 'dedup_config'. Expected dict."
        return False, error_message

    if not isinstance(data["data_schema"], dict):
        error_message = "Invalid data type for 'data_schema'. Expected dict."
        return False, error_message

    if not isinstance(data["denorm_config"], dict):
        error_message = "Invalid data type for 'denorm_config'. Expected dict."
        return False, error_message

    if not isinstance(data["router_config"], dict):
        error_message = "Invalid data type for 'router_config'. Expected dict."
        return False, error_message

    if not isinstance(data["dataset_config"], dict):
        error_message = "Invalid data type for 'dataset_config'. Expected dict."
        return False, error_message

    #Need to be changed to list
    # if not isinstance(data["tags"], str):
    #     error_message = "Invalid data type for 'tags'. Expected list."
    #     return False, error_message

    if not isinstance(data["data_version"], int):
        error_message = "Invalid data type for 'data_version'. Expected str."
        return False, error_message

    if not isinstance(data["status"], str):
        error_message = "Invalid data type for 'status'. Expected str."
        return False, error_message

    if not isinstance(data["created_by"], str):
        error_message = "Invalid data type for 'created_by'. Expected str."
        return False, error_message

    if not isinstance(data["updated_by"], str):
        error_message = "Invalid data type for 'updated_by'. Expected str."
        return False, error_message

    # Validate date formats
    date_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$'
    if not re.match(date_pattern, data["created_date"]):
        error_message = "Invalid format for 'created_date'. Expected YYYY-MM-DD."
        return False, error_message

    if not re.match(date_pattern, data["updated_date"]):
        error_message = "Invalid format for 'updated_date'. Expected YYYY-MM-DD."
        return False, error_message

    if not re.match(date_pattern, data["published_date"]):
        error_message = "Invalid format for 'published_date'. Expected YYYY-MM-DD."
        return False, error_message

    return True, None

def validate_request_data(data):
    if not data:
        return False, "No json data is given"
    return True, None

def validate_dataset_id(dataset_id):
    if not dataset_id:
        return False, "No dataset_id given"
    return True, None
