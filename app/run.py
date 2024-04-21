from flask import Flask
from routes import bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(bp)

@app.route('/')
def homepage():
    return 'Welcome'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)