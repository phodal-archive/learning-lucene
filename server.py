#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

from flask import Flask
import flask
from indexers import search

PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

@app.route('/')
def home():
    search()
    return flask.jsonify({"led": "true"})
