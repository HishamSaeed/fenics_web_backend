from flask import jsonify, request
from config import app, db, socketIo
from models import Simulation
from solver.helix_simulation import solve_helix_simulation


@app.route("/simulate", methods=["POST"])
def simulate():
    simulation = get_simulation()
    socketIo.emit("simulation_running", True)
    solve_helix_simulation(simulation)
    socketIo.emit("simulation_running", False)

    return jsonify({"message": "Simulation Finished!"}), 201

@app.route("/t_start", methods=["GET", "POST"])
def update_t_start():
    simulation = get_simulation()

    if request.method == "POST":
        simulation.t_start = request.json['value']
        db.session.commit()
        socketIo.emit("update_t_start", {"value": simulation.t_start})
        return jsonify({"message": "tStart set"}), 201
    else:
        return jsonify({"value": simulation.t_start })

@app.route("/t_end", methods=["GET", "POST"])
def update_t_end():
    simulation = get_simulation()

    if request.method == "POST":
        simulation.t_end = request.json['value']
        db.session.commit()
        socketIo.emit("update_t_end", {"value": simulation.t_end})
        return jsonify({"message": "tEnd set"}), 201
    else:
        return jsonify({"value": simulation.t_end })

@app.route("/dt", methods=["GET", "POST"])
def update_dt():
    simulation = get_simulation()

    if request.method == "POST":
        simulation.dt = request.json['value']
        db.session.commit()
        socketIo.emit("update_dt", {"value": simulation.dt})
        return jsonify({"message": "dt set"}), 201
    else:
        return jsonify({"value": simulation.dt })
    
@app.route("/u_in", methods=["GET", "POST"])
def update_u_in():
    simulation = get_simulation()

    if request.method == "POST":
        simulation.u_in = request.json['value']
        db.session.commit()
        socketIo.emit("update_u_in", {"value": simulation.u_in})
        return jsonify({"message": "uIn set"}), 201
    else:
        return jsonify({"value": simulation.u_in })

@app.route("/u_out", methods=["GET", "POST"])
def update_u_out():
    simulation = get_simulation()
    if request.method == "POST":
        simulation.u_out = request.json['value']
        db.session.commit()
        socketIo.emit("update_u_out", {"value": simulation.u_in})
        return jsonify({"message": "uOut set"}), 201
    else:
        return jsonify({"value": {"value": simulation.u_out}})

@app.route("/simulation", methods=["GET"])
def simulation():
    simulation = get_simulation()
    return jsonify({"tStart": simulation.t_start, "tEnd": simulation.t_end, "dt": simulation.dt, "uIn": simulation.u_in, "uOut": simulation.u_out})

@app.route("/create_simulation", methods=["POST"])
def create_simulation():
    simulation = Simulation.query.get(1)
    if simulation:
        db.session.delete(simulation)
        db.session.commit()

    new_simulation = Simulation()
    new_simulation.id = 1
    new_simulation.t_start = 0
    new_simulation.t_end = 10
    new_simulation.dt = 0.1
    new_simulation.u_in = 20
    new_simulation.u_out = -20
    db.session.add(new_simulation)
    db.session.commit()
    socketIo.emit("update_t_start", {"value": new_simulation.t_start})
    socketIo.emit("update_t_end", {"value": new_simulation.t_end})
    socketIo.emit("update_dt", {"value": new_simulation.dt})
    socketIo.emit("update_u_in", {"value": new_simulation.u_in})
    socketIo.emit("update_u_out", {"value": new_simulation.u_out})

    return jsonify({"message": "Simulation Created!"}), 201

def get_simulation():
    simulation = Simulation.query.get(1)

    if not simulation:
        return jsonify({"message": "Simulation does not exist"})
    else:
        return simulation
@app.route('/publish_events', methods=["POST"])    
def publish_events():
    simulation = get_simulation()
    socketIo.emit("update_t_start", {"value": simulation.t_start})
    socketIo.emit("update_t_end", {"value": simulation.t_end})
    socketIo.emit("update_dt", {"value": simulation.dt})
    socketIo.emit("update_u_in", {"value": simulation.u_in})
    socketIo.emit("update_u_out", {"value": simulation.u_out})
    return jsonify({"message": "events published succseefully"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    socketIo.run(app=app, debug=True, host='0.0.0.0')