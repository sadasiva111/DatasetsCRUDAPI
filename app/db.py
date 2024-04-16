import psycopg2

db_params = {
    'dbname': 'postgres',
    'user': 'obsrv_user',
    'password': 'obsrv123',
    'host': 'localhost',
    'port': '5432'
}

def connect_to_db():
    conn = psycopg2.connect(**db_params)
    return conn

conn = connect_to_db()