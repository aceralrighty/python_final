from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Supply

app = Flask(__name__, template_folder='templates')
engine = create_engine('sqlite:///test.db')
app.secret_key = "secret"




@app.route("/")
def index():
    return render_template('index.html')

@app.route("/add_room")
def add_room():
    return render_template('add_room.html')


def is_tiling_needed(is_tiling):
    if is_tiling:
        return True
    else:
        return False

@app.route('/add_supplies', methods=['GET', 'POST'])
def add_supplies():
    if request.method == 'GET':
        session["supply_name"] = request.form["supply_name"]
        session["quantity"] = request.form["quantity"]
        session['cost_per_item'] = request.form["cost_per_item"]
        session["is_tiling_needed"] = is_tiling_needed(request.form["is_tiling_needed"])

        ss = Session()
        new_supply = Supply(name=session["supply_name"], quantity=session["quantity"], cost_per_item=session["cost_per_item"])
        ss.add(new_supply)
        ss.commit()
        ss.close()

