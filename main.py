import os
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import matplotlib.pyplot as plt
import seaborn as sns
from models import Room, Supply, FloorType, TileType

app = Flask(__name__, )
app.secret_key = "secret"

os.makedirs("static", exist_ok=True)

engine = create_engine('sqlite:///supply_tracker.db')
Session = sessionmaker(bind=engine)


@app.route("/")
def index():
    with Session() as ss:
        graph()
        room = ss.query(Room).all()
    return render_template('index.html', rooms=room, plot_url=url_for("static", filename="graph.png"))


def graph():
    with Session() as ss:
        rooms = ss.query(Room).all()
        tiling_costs = [room.tiling_cost_per_sqft for room in rooms]
        room_names = [room.name for room in rooms]
        plt.figure(figsize=(10, 6))
        sns.barplot(x=tiling_costs, y=room_names, palette="Blues")
        plt.xlabel("Tiling Cost per sqft")
        plt.ylabel("Room Name")
        img_path = os.path.join(app.root_path, "static", "graph.png")
        plt.savefig(img_path)
        plt.close()


@app.route("/add_room", methods=["GET", "POST"])
def add_room():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["surface_area"] = float(request.form["surface_area"])

        floor_type = request.form["flooring_type"]
        session["flooring_type"] = floor_type
        session["flooring_cost_per_sqft"] = float(getattr(FloorType, floor_type).value)

        tiling = request.form["tiling"]
        session["tiling"] = tiling
        session["tiling_cost_per_sqft"] = float(getattr(TileType, tiling).value) if tiling else 0
        session["tiling_area"] = float(request.form["tiling_area"])
        room_data = {
            "name": session["name"],
            "surface_area": session["surface_area"],
            "flooring_type": session["flooring_type"],
            "flooring_cost_per_sqft": session["flooring_cost_per_sqft"],
            "tiling": session["tiling"],
            "tiling_cost_per_sqft": session["tiling_cost_per_sqft"],
            "tiling_area": session["tiling_area"],
        }

        new_room = Room(**room_data)
        costs = new_room.calc_cost()
        with Session() as ss:
            ss.add(new_room)
            ss.commit()
            ss.close()

        return render_template(
            'add_room.html',
            name=session.get('name', ''),
            surface_area=session.get("surface_area", 0.0),
            flooring_type=session.get("flooring_type", ''),
            flooring_cost_per_sqft=session.get("flooring_cost_per_sqft", 0.0),
            tiling=session.get("tiling", ''),
            tiling_cost_per_sqft=session.get("tiling_cost_per_sqft", 0.0),
            tiling_area=session.get("tiling_area", 0.0),
            **costs
        )

    return render_template("add_room.html", flooring_types=FloorType.__members__.items(),
                           flooring_tiles=TileType.__members__.items())


@app.route("/edit_room")
def edit_room():
    if request.method == "GET":
        session['room_name'] = request.form["room_name"]
    return render_template("edit_room.html", room=get_specific_room(session['room_name']))


@app.route("/room_details")
def room_details():
    session['name'] = request.form['name']
    return render_template('room_details.html', room=get_specific_room(session['name']))


def get_specific_room(name):
    with Session() as ss:
        return ss.query(Room).filter_by(name=name).first()


def is_tiling_needed(is_tiling):
    if is_tiling:
        return True
    else:
        return False


@app.route('/add_supplies', methods=['GET', 'POST'])
def add_supplies():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session["supply_name"] = request.form["supply_name"]
        session["quantity"] = int(request.form["quantity"])
        session['cost_per_item'] = float(request.form["cost_per_item"])

        supply_data = {
            "supply_name": session["supply_name"],
            "quantity": session["quantity"],
            "cost_per_item": session["cost_per_item"],
        }

        new_supply = Supply(**supply_data)
        with Session() as ss:
            ss.add(new_supply)
            ss.commit()
            ss.close()

        return redirect(url_for("index"))
    return render_template('add_supplies.html', room_name=session["name"], supply_name=session["supply_name"],
                           quantity=session["quantity"], cost_per_item=session["cost_per_item"])


@app.route("/supplies_details", methods=['GET', 'POST'])
def supply_details(room_id):
    with Session() as ss:
        if request.method == 'POST':
            room_deets = ss.query(Room).filter(Room.id == room_id).first()

            if room_deets:
                cost = room_deets.calc_cost()

                return render_template("supplies_details.html", room_deets=room_deets, **cost)


if __name__ == '__main__':
    app.run()
