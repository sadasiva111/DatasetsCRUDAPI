from flask import request
from db import get_connection, release_connection
from validations import validate_dataset_data

class DatasetModel:
    def __init__(self):
        self.conn = None
        self.cur = None

    def get_conn(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def rel_conn(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            release_connection(self.conn)

        
    def create_dataset(self, data):
        is_valid, error_message = validate_dataset_data(data)
        if not is_valid:
            return False, error_message

        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"
            
        try:
            cur.execute("""INSERT INTO datasets
                (id, dataset_id, "type", "name", validation_config, extraction_config, dedup_config, data_schema, denorm_config, router_config, dataset_config, tags, data_version, status, created_by, updated_by, created_date, updated_date, published_date)
                VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
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
            return True, None
        except Exception as e:
            conn.rollback()
            print(f"Error creating dataset: {e}")
            return False, str(e)
        finally:
            self.rel_conn()

    def get_dataset(self, dataset_id):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"
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
                return True, dataset_list
            else:
                return False, "No datasets found for the given dataset_id"
        except Exception as e:
            print(f"Error retrieving dataset: {e}")
            return False, str(e)
        finally:
            self.rel_conn()


    def update_dataset(self, dataset_id, data):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
            set_clause = ', '.join([f"{field} = %s" for field in data.keys()])
            query = f"UPDATE datasets SET {set_clause} WHERE dataset_id = %s"
            values = list(data.values())
            values.append(dataset_id)

            cur.execute(query, values)
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error updating dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()

    def delete_dataset(self, dataset_id):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
            cur.execute("DELETE FROM datasets WHERE dataset_id = %s", (dataset_id,))
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error deleting dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()


    def update_whole_dataset(self, dataset_id, data):
        conn, cur = self.get_conn()
        if not conn or not cur:
            return False, "Failed to get database connection"

        try:
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
                WHERE dataset_id = %s
            """
            values = (
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
                data['published_date'],
                dataset_id
            )

            cur.execute(query, values)
            conn.commit()
            return True, None

        except Exception as e:
            conn.rollback()
            print(f"Error updating dataset: {e}")
            return False, str(e)

        finally:
            self.rel_conn()