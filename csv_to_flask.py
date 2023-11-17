#!/usr/bin/env python
from io import TextIOWrapper
import csv

from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# Create Flaskk app, config the db and load the db object
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)





