from flask import Flask, jsonify
from routes import bp
from db import get_connection, release_connection, pool
import socket

app = Flask(__name__)
app.register_blueprint(bp)

@app.route('/')
def homepage():
    return 'Welcome'

@app.route('/health')
def health():
    app_health = check_app_health()
    db_health = check_db_health()

    if app_health and db_health:
        hostname, host_ip = fetchDetails()
        response_data = {
            "status": "OK",
            "hostname": hostname,
            "host_ip": host_ip
        }
        return jsonify(response_data), 200
    else:
        status_code = 503 if not app_health else 500
        error_message = "Application error" if not app_health else "Database connection error"
        return f"Error: {error_message}", status_code
    
def fetchDetails():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)

def check_app_health():
    return fetchDetails()

def check_db_health():
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        return True
    except Exception:
        return False
    finally:
        if conn:
            release_connection(conn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)