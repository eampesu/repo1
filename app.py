from flask import Flask
from flask import redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy.sql import text

app = Flask(__name__)
app.secret_key=getenv("SECRET_KEY")
import routes
