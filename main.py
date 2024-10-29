from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
app = Flask(__name__)
engine = create_engine('sqlite:///test.db')
app.secret_key = "secret"

@app.route('/')
def index():
    return render_template("index.html")
