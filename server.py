from flask import Flask
import flask
import indexers

PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

#
# @app.cli.command('create_index')
# def create_index():
#     indexers.create_index()


@app.route('/')
def home():
    return flask.jsonify({"led": "true"})
