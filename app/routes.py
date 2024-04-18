from flask import request, jsonify, Blueprint
from models import DatasetModel
from validations import validate_request_data, validate_dataset_id
import logging

dataset_model = DatasetModel()
logger = logging.getLogger(__name__)
bp = Blueprint('routes', __name__, url_prefix='/v1')

def verify_dataset_id(dataset_id):
    is_valid, error_message = validate_dataset_id(dataset_id)
    if not is_valid:
        logger.error(error_message)
        return jsonify({'error': error_message}), 400
    
def verify_dataset_data(data):
    is_valid, error_message = validate_request_data(data)
    if not is_valid:
        logger.error(error_message)
        return jsonify({'error': error_message}), 400

@bp.route('/dataset', methods=['POST'])
def create_dataset():
    data = request.get_json()
    verify_dataset_data(data)
    success, error_message = dataset_model.create_dataset(data)
    if success:
        logger.info('Dataset created successfully')
        return jsonify({'message': 'Created Dataset'})
    else:
        logger.error(f'Error creating dataset: {error_message}')
        return jsonify({'error': error_message}), 500
    
@bp.route('/dataset/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    verify_dataset_id(dataset_id)
    success, result = dataset_model.get_dataset(dataset_id)
    if success:
        if result:
            logger.info('Getting Datasets successfully')
            return jsonify(result), 200
        else:
            logger.warning(f'No datasets found for dataset_id: {dataset_id}')
            return jsonify([]), 200
    else:
        logger.error(f'Error retrieving dataset: {result}')
        return jsonify({'error': result}), 500
    
@bp.route('/dataset/<dataset_id>', methods=['PATCH'])
def update_dataset(dataset_id):
    verify_dataset_id(dataset_id)
    data = request.get_json()
    verify_dataset_data(data)
    success, error_message = dataset_model.update_dataset(dataset_id, data)
    if success:
        return jsonify({'message': 'Dataset updated'}), 200
    else:
        return jsonify({'error': error_message}), 500

@bp.route('/dataset/<dataset_id>', methods=['DELETE'])
def delete_dataset(dataset_id):
    verify_dataset_id(dataset_id)
    success, error_message = dataset_model.delete_dataset(dataset_id)
    if success:
        return jsonify({'message': 'Dataset soft deleted'}), 200
    else:
        return jsonify({'error': error_message}), 500
    
@bp.route('/dataset/<dataset_id>', methods=['PUT'])
def update_whole_dataset(dataset_id):
    verify_dataset_id(dataset_id)
    data = request.get_json()
    success, error_message = dataset_model.update_whole_dataset(dataset_id, data)
    if success:
        return jsonify({'message': 'Dataset updated'}), 200
    else:
        return jsonify({'error': error_message}), 500
    