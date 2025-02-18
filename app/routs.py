from app import app
from flask import render_template, send_from_directory

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/img', 'favicon.ico')

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/work')
def work():
    return render_template("work.html")

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/projects/<project_name>')
def project(project_name):
    return render_template(f"projects/{project_name}.html")