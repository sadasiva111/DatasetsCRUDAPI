from flask import Flask, request, jsonify
from db import conn

app = Flask(__name__)

@app.route('/v1/dataset', methods=['POST'])
def create_dataset():
    cur = conn.cursor()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error':'No json data given'}), 400
        dataset_id = data.get('dataset_id')
        cur.execute("""INSERT INTO datasets
    (id, dataset_id, "type", "name", validation_config, extraction_config, dedup_config, data_schema, denorm_config, router_config, dataset_config, tags, data_version, status, created_by, updated_by, created_date, updated_date, published_date)
                    VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,(
                data['id'],
                data['dataset_id'],
                data['type'],
                data['name'],
                data['validation_config'],
                data['extraction_config'],
                data['dedup_config'],
                data['data_schema'],
                data['denorm_config'],
                data['router_config'],
                data['dataset_config'],
                data['tags'],
                data['data_version'],
                data['status'],
                data['created_by'],
                data['updated_by'],
                data['created_date'],
                data['updated_date'],
                data['published_date']
            ))
        conn.commit()
        return jsonify({'message':'Created Dataset'})
    except Exception as e:
            conn.rollback()
            return jsonify({'error':str(e)}),500
    finally:
        cur.close()  

@app.route('/v1/dataset/<dataset_id>', methods=['GET'])
def get_dataset(dataset_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM datasets WHERE dataset_id = %s", (dataset_id,))
        datasets = cur.fetchall()
        dataset_list = []
        if datasets:
            for dataset in datasets:
                dataset_dict = {
                    'id': dataset[0],
                    'dataset_id': dataset[1],
                    'type': dataset[2],
                    'name': dataset[3],
                    'validation_config': dataset[4],
                    'extraction_config': dataset[5],
                    'dedup_config': dataset[6],
                    'data_schema': dataset[7],
                    'denorm_config': dataset[8],
                    'router_config': dataset[9],
                    'dataset_config': dataset[10],
                    'tags': dataset[11],
                    'data_version': dataset[12],
                    'status': dataset[13],
                    'created_by': dataset[14],
                    'updated_by': dataset[15],
                    'created_date': dataset[16],
                    'updated_date': dataset[17],
                    'published_date': dataset[18]
                }
                dataset_list.append(dataset_dict)
            return jsonify(dataset_list), 200
        else:
            return jsonify({'error': 'Dataset not found'}), 404
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    finally:
        cur.close()

@app.route('/v1/dataset/<dataset_id>', methods=(['PATCH']))
def update_dataset(dataset_id):
    cur = conn.cursor()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error':'No json data given'}), 400
        set_clause = ', '.join([f"{field} = %s" for field in data.keys()])
        query = f"UPDATE datasets SET {set_clause} WHERE dataset_id = %s"
        values = list(data.values())
        values.append(dataset_id)
        cur.execute(query, values)
        conn.commit()
        return jsonify({'message':'Dataset Updated'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error':str(e)}), 500
    finally:
        cur.close()

@app.route('/v1/dataset/<dataset_id>', methods=(['DELETE']))
def detele_dataset(dataset_id):
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM datasets WHERE dataset_id = %s", (dataset_id,))
        conn.commit()
        return jsonify({'message':'Deleted'})
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    finally:
        cur.close()

@app.route('/v1/dataset/<dataset_id>', methods=['PUT'])
def update_whole_dataset(dataset_id):
    cur = conn.cursor()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error':'No json data given'})
        
        query = """
                UPDATE datasets
                SET dataset_id = %s, type = %s, name = %s, validation_config = %s,
                    extraction_config = %s, dedup_config = %s, data_schema = %s,
                    denorm_config = %s, router_config = %s, dataset_config = %s,
                    tags = %s, data_version = %s, status = %s, created_by = %s,
                    updated_by = %s, created_date = %s, updated_date = %s,
                    published_date = %s
                WHERE dataset_id = %s
            """
        values = (
                data['dataset_id'], data['type'], data['name'],
                data['validation_config'], data['extraction_config'],
                data['dedup_config'], data['data_schema'], data['denorm_config'],
                data['router_config'], data['dataset_config'], data['tags'],
                data['data_version'], data['status'], data['created_by'],
                data['updated_by'], data['created_date'], data['updated_date'],
                data['published_date'], dataset_id
            )
        
        cur.execute(query,values)
        conn.commit()
        return jsonify({'message':'Dataset Updated'})
    except Exception as e:
        conn.rollback()
        return jsonify({'error':str(e)}), 500
    finally:
        cur.close()


if __name__ == '__main__':
    app.run(debug=True)
