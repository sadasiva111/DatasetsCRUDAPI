def validate_dataset_data(data):
    required_fields = ['id', 'dataset_id', 'type', 'name', 'validation_config', 'extraction_config',
                       'dedup_config', 'data_schema', 'denorm_config', 'router_config', 'dataset_config',
                       'tags', 'data_version', 'status', 'created_by', 'updated_by', 'created_date',
                       'updated_date', 'published_date']

    for field in required_fields:
        if field not in data or data[field] is None:
            return False, f"Missing required field: {field}"
        
    return True, None

def validate_request_data(data):
    if not data:
        return False, "No json data is given"
    return True, None

def validate_dataset_id(dataset_id):
    if not dataset_id:
        return False, "No dataset_id given"
    return True, None
