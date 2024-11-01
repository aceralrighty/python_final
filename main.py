import os

from flask import Flask, render_template, request, session, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Supply, FloorType, TileType, Room
import matplotlib.pyplot as plt
import seaborn as sns
from models import ss, Room, Supply

app = Flask(__name__, )
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)


@app.route("/")
def index():
    room = ss.query(Room).all()
    return render_template('index.html', rooms=room)


@app.route("/add_room")
def add_room():
    if request.method == "POST":
        name = request.form["name"]
        surface_area = float(request.form["surface_area"])
        flooring_type = request.form["flooring_type"]
        flooring_cost_per_sqft = float(request.form["flooring_cost_per_sqft"])
        tiling = request.form["tiling"]
        tiling_cost_per_sqft = float(request.form["tiling_cost_per_sqft"])
        tiling_area = float(request.form["tiling_area"])
        room_data = {
            "name": name,
            "surface_area": surface_area,
            "flooring_type": flooring_type,
            "flooring_cost_per_sqft": flooring_cost_per_sqft,
            "tiling": tiling,
            "tiling_cost_per_sqft": tiling_cost_per_sqft,
            "tiling_area": tiling_area,
        }
        plt.figure(figsize=(10, 6))
        sns.barplot(x=tiling_cost_per_sqft, y=flooring_cost_per_sqft, data=room_data, palette="Blues")
        img_path = os.path.join(app.root_path, "static", "graph.png")
        plt.savefig(img_path)
        plt.close()

        ss.add(**room_data)
        ss.commit()
        ss.close()
        return redirect(url_for("index"))

    return render_template('add_room.html')


# @app.route("/edit_room")
# def edit_room():
#     if request.method == "GET":
#
#     return render_template("edit_room.html")

@app.route("/room_details")
def room_details():
    session['name'] = request.form['name']
    return render_template('room_details.html', room=get_specific_room(session['name']))


def get_specific_room(name):
    return ss.query(Room).filter_by(name=name).first()


def is_tiling_needed(is_tiling):
    if is_tiling:
        return True
    else:
        return False


@app.route('/add_supplies', methods=['GET', 'POST'])
def add_supplies():
    if request.method == 'POST':
        session["supply_name"] = request.form["supply_name"]
        session["quantity"] = int(request.form["quantity"])
        session['cost_per_item'] = float(request.form["cost_per_item"])

        supply_data = {
            "supply_name": session["supply_name"],
            "quantity": session["quantity"],
            "cost_per_item": session["cost_per_item"],
        }

        new_supply = Supply(**supply_data)
        ss.add(new_supply)
        ss.commit()
        ss.close()


@app.route("/supplies_details", methods=['GET', 'POST'])
def room_details(room_id):
    if request.method == 'POST':
        room_deets = ss.query(Room).filter(Room.id == room_id).first()

        if room_deets:
            cost = room_deets.calc_cost()

            return render_template("supplies_details.html", room_deets=room_deets, **cost)


if __name__ == '__main__':
    app.run()
