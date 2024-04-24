import os
import psycopg2
import psycopg2.pool
from dotenv import load_dotenv

load_dotenv()

db_params = {
    'dbname': os.getenv('POSTGRES_DB', 'postgres'),
    'user': os.getenv('POSTGRES_USER', 'postgres'), 
    'password': os.getenv('POSTGRES_PASSWORD', 'yj3OyEEppH'),
    'host': os.getenv('POSTGRES_HOST', 'postgresql.postgres'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_params)

def get_connection():
    return pool.getconn()

def release_connection(conn):
    pool.putconn(conn)