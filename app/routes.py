from flask import request, jsonify, Blueprint
from models import DatasetModel
from validations import validate_request_data, validate_id
import logging

dataset_model = DatasetModel()
logger = logging.getLogger(__name__)
bp = Blueprint('routes', __name__, url_prefix='/v1')

def verify_id(id):
    is_valid, error_message = validate_id(id)
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
        return jsonify({'error': error_message}), 400
    
@bp.route('/dataset/<id>', methods=['GET'])
def get_dataset(id):
    verify_id(id)
    success, result = dataset_model.get_dataset(id)
    if success:
        if result:
            logger.info('Getting Datasets successfully')
            return jsonify(result), 200
        else:
            logger.warning(f'No datasets found for id: {id}')
            return jsonify([]), 200
    else:
        logger.error(f'Error retrieving dataset: {result}')
        return jsonify({'error': result}), 400
    
@bp.route('/dataset/<id>', methods=['PATCH'])
def update_dataset(id):
    verify_id(id)
    data = request.get_json()
    verify_dataset_data(data)
    success, error_message = dataset_model.update_dataset(id, data)
    if success:
        return jsonify({'message': 'Dataset updated'}), 200
    else:
        return jsonify({'error': error_message}), 400

@bp.route('/dataset/<id>', methods=['DELETE'])
def delete_dataset(id):
    verify_id(id)
    success, error_message = dataset_model.delete_dataset(id)
    if success:
        return jsonify({'message': 'Dataset soft deleted'}), 200
    else:
        return jsonify({'error': error_message}), 400
    
@bp.route('/dataset/<id>', methods=['PUT'])
def update_whole_dataset(id):
    verify_id(id)
    data = request.get_json()
    success, error_message = dataset_model.update_whole_dataset(id, data)
    if success:
        return jsonify({'message': 'Dataset updated'}), 200
    else:
        return jsonify({'error': error_message}), 400
    