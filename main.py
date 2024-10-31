from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Supply, FloorType, TileType, Room

app = Flask(__name__, template_folder='templates')
engine = create_engine('sqlite:///test.db')
app.secret_key = "secret"




@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add_room")
def add_room():
    if request.method == "POST":
        session['room_name'] = request.form['room_name']
        session['surface_area'] = float(request.form['surface_area'])
        session['floor_type'] = FloorType(request.form['floor_type'])
        session['cost_per_sqrft']=float(request.form['cost_per_sqrft'])
        if is_tiling_needed(session['tiling']):
            session['tiling_type'] =TileType(request.form['tiling_type'])
            session['tiling_cost_sqrft'] = float(request.form['tiling_cost_sqrft'])
            session['tiling_area'] = float(request.form['tiling_area'])
        ss = Session()
        new_room = Room(session['room_name'],session['surface_area'],session['floor_type'],
                        session['tiling_type'],session['tiling_cost_sqrft'],session['tiling_area'])
        ss.add(new_room)
        ss.commit()
        ss.close()
        return redirect(url_for('index'))
    return render_template('add_room.html')


def is_tiling_needed(is_tiling):
    if is_tiling:
        return True
    else:
        return False

def room_details():
    ss = Session()
    ss.query(Room)


@app.route('/add_supplies', methods=['GET', 'POST'])
def add_supplies():
    if request.method == 'POST':
        session["supply_name"] = request.form["supply_name"]
        session["quantity"] = request.form["quantity"]
        session['cost_per_item'] = request.form["cost_per_item"]

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
        room_deets = ss.query(Room).get(room_id)

        if room_deets:
            cost = room_deets.calc_cost()

            return render_template("supplies_details.html", room_deets=room_deets, **cost)

if __name__ == '__main__':
    app.run(debug=True)