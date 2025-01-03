from flask import Flask

app = Flask(__name__)
app.secret_key = 'dev'

try:
    app.config.from_pyfile('../instance/config.py')
except FileNotFoundError as e:
    print("Config file not found in /instance/config.py")

from app import routs