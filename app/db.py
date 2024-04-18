import psycopg2
import psycopg2.pool

db_params = {
    'dbname': 'postgres',
    'user': 'obsrv_user',
    'password': 'obsrv123',
    'host': 'localhost',
    'port': '5432'
}

pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_params)


def get_connection():
    return pool.getconn()

def release_connection(conn):
    pool.putconn(conn)