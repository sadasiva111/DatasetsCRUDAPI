from flask import request
from db import get_connection, release_connection
from validations import validate_dataset_data
import json
from datetime import datetime

class DatasetModel:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_system_time(self):
        return datetime.now()
    
    def get_conn(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def rel_conn(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            release_connection(self.conn)

        
    # def create_dataset(self, data):

    #     conn, cur = self.get_conn()
    #     if not conn or not cur:
    #         return False, "Failed to get database connection"
            
    #     try:
    #         created_date = self.get_system_time()
    #         cur.execute("""INSERT INTO datasets
    #             (id, dataset_id, "type", "name", validation_config, extraction_config, dedup_config, data_schema, denorm_config, router_config, dataset_config, tags, data_version, status, created_by, updated_by, created_date, updated_date, published_date)
    #             VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #         """, (
    #             data['id'],
    #             data['dataset_id'],
    #             data['type'],
    #             data['name'],
    #             json.dumps(data['validation_config']),
    #             json.dumps(data['extraction_config']),
    #             json.dumps(data['dedup_config']),
    #             json.dumps(data['data_schema']),
    #             json.dumps(data['denorm_config']),
    #             json.dumps(data['router_config']),
    #             json.dumps(data['dataset_config']),
    #             json.dumps(data['tags']),
    #             data['data_version'],
    #             data['status'],
    #             data['created_by'],
    #             data['updated_by'],
    #             created_date,
    #             created_date,
    #             created_date
    #         ))
    #         is_valid, error_message = validate_dataset_data(data)
    #         if not is_valid:
    #             return False, error_message
    #         conn.commit()
    #         return True, None
    #     except Exception as e:
    #         conn.rollback()
    #         print(f"Error creating dataset: {e}")
    #         return False, str(e)
    #     finally:
    #         self.rel_conn()

    def create_dataset(self, data):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
            created_date = self.get_system_time()
            keys = ['id', 'dataset_id', 'type', 'name', 'validation_config', 'extraction_config', 'dedup_config', 'data_schema', 'denorm_config', 'router_config', 'dataset_config', 'tags', 'data_version', 'status', 'created_by', 'updated_by']
            values = [data.get(key, None) for key in keys]
            for i, key in enumerate(['validation_config', 'extraction_config', 'dedup_config', 'data_schema', 'denorm_config', 'router_config', 'dataset_config', 'tags']):
                if values[keys.index(key)] is not None:
                    values[keys.index(key)] = json.dumps(values[keys.index(key)])
            values.extend([created_date, created_date, created_date])
            cur.execute("""INSERT INTO datasets (id, dataset_id, "type", "name", validation_config, extraction_config, dedup_config, data_schema, denorm_config, router_config, dataset_config, tags, data_version, status, created_by, updated_by, created_date, updated_date, published_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", tuple(values))

            is_valid, error_message = validate_dataset_data(data)
            if not is_valid:
                return False, error_message

            conn.commit()
            return True, None
        except Exception as e:
            conn.rollback()
            print(f"Error creating dataset: {e}")
            return False, str(e)
        finally:
            self.rel_conn()

    def get_dataset(self, id):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"
        try:
            cur.execute("SELECT * FROM datasets WHERE id = %s AND is_deleted = false", (id,))
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
                return True, dataset_list
            else:
                return False, "No datasets found for the given id"
        except Exception as e:
            print(f"Error retrieving dataset: {e}")
            return False, str(e)
        finally:
            self.rel_conn()


    def update_dataset(self, id, data):
        is_valid, error_message = validate_dataset_data(data)
        if not is_valid:
            return False, error_message
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
            for key, value in data.items():
                if isinstance(value, dict):
                    data[key] = json.dumps(value)

            cur.execute("SELECT COUNT(*) FROM datasets WHERE id = %s AND is_deleted = false", (id,))
            count = cur.fetchone()[0]
            if count == 0:
                return False, "Dataset not found or already deleted"

            set_clause = ', '.join([f"{field} = %s" for field in data.keys()])
            query = f"UPDATE datasets SET {set_clause} WHERE id = %s"
            updated_date = self.get_system_time()
            data['updated_date'] = updated_date
            values = list(data.values())
            values.append(id)

            cur.execute(query, values)
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error updating dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()

    def delete_dataset(self, id):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
            cur.execute("SELECT is_deleted FROM datasets WHERE id = %s", (id,))
            result = cur.fetchone()

            if result and result[0]:
                return False, "Dataset has already been deleted"
            cur.execute("UPDATE datasets SET is_deleted = true WHERE id = %s", (id,))
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error soft deleting dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()


    def update_whole_dataset(self, id, data):
        is_valid, error_message = validate_dataset_data(data)
        if not is_valid:
            return False, error_message
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"
        

        try:
            cur.execute("SELECT COUNT(*) FROM datasets WHERE id = %s AND is_deleted = false", (id,))
            count = cur.fetchone()[0]
            if count == 0:
                return False, "Dataset not found or already deleted"
            
            if not data:
                return False, "No JSON data provided"

            query = """
                UPDATE datasets SET
                    dataset_id = %s,
                    type = %s,
                    name = %s,
                    validation_config = %s,
                    extraction_config = %s,
                    dedup_config = %s,
                    data_schema = %s,
                    denorm_config = %s,
                    router_config = %s,
                    dataset_config = %s,
                    tags = %s,
                    data_version = %s,
                    status = %s,
                    created_by = %s,
                    updated_by = %s,
                    created_date = %s,
                    updated_date = %s,
                    published_date = %s
                WHERE id = %s
            """
            values = (
                data['dataset_id'],
                data['type'],
                data['name'],
                json.dumps(data['validation_config']),
                json.dumps(data['extraction_config']),
                json.dumps(data['dedup_config']),
                json.dumps(data['data_schema']),
                json.dumps(data['denorm_config']),
                json.dumps(data['router_config']),
                json.dumps(data['dataset_config']),
                json.dumps(data['tags']),
                data['data_version'],
                data['status'],
                data['created_by'],
                data['updated_by'],
                id
            )
            updated_date = self.get_system_time()
            data['updated_date'] = updated_date,

            cur.execute(query, values)
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error updating dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()