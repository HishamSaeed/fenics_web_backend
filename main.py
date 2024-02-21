from flask import jsonify, request, send_file
from config import app, db
from models import Simulation
from solver.helix_simulation import solve_helix_simulation
import os

@app.route("/simulate", methods=["POST"])
def simulate():
    simulation = get_simulation()
    solve_helix_simulation(simulation)

    return jsonify({"message": "Simulation Finished!"}), 201

@app.route("/t_start//<float:t_start>", methods=["GET", "POST"])
def update_t_start(t_start):
    simulation = get_simulation()

    if request.method == "POST":
        simulation.t_start = t_start
        db.session.commit()
        return jsonify({"message": "tStart set"}), 201
    else:
        return jsonify({"tStart": simulation.t_start })

@app.route("/t_end/<float:t_end>", methods=["GET", "POST"])
def update_t_end(t_end):
    simulation = get_simulation()

    if request.method == "POST":
        simulation.t_end = t_end
        db.session.commit()
        return jsonify({"message": "tEnd set"}), 201
    else:
        return jsonify({"tEnd": simulation.t_end })

@app.route("/dt/<float:dt>", methods=["GET", "POST"])
def update_dt(dt):
    simulation = get_simulation()

    if request.method == "POST":
        simulation.dt = dt
        db.session.commit()
        return jsonify({"message": "dt set"}), 201
    else:
        return jsonify({"dt": simulation.dt })
    
@app.route("/u_in/<float:u_in>", methods=["GET", "POST"])
def update_u_in(u_in):
    simulation = get_simulation()

    if request.method == "POST":
        simulation.u_in = u_in
        db.session.commit()
        return jsonify({"message": "uIn set"}), 201
    else:
        return jsonify({"uIn": simulation.u_in })

@app.route("/mesh_file_name", methods=["GET"])
def get_mesh_file_name():
    simulation = get_simulation()
    
    return jsonify({"meshFileName": simulation.mesh_file_name })

@app.route("/u_out/<float:u_out>", methods=["GET", "POST"])
def update_u_out(u_out):
    simulation = get_simulation()
    if request.method == "POST":
        simulation.u_out = u_out
        db.session.commit()
        return jsonify({"message": "uOut set"}), 201
    else:
        return jsonify({"uOut": simulation.u_out })
    
@app.route("/simulation", methods=["GET"])
def simulation():
    simulation = get_simulation()
    return jsonify({"tStart": simulation.t_start, "tEnd": simulation.t_end, "dt": simulation.dt, "uIn": simulation.u_in, "uOut": simulation.u_out})

@app.route("/download", methods=["GET"])
def download_file():
    path = "./solver/helix_mesh_physical_region.xml"
    return send_file(path, as_attachment=True)


@app.route("/upload_mesh", methods=["POST"])
def upload_mesh():
    uploaded_file = request.files["file"]

    simulation = get_simulation()
    simulation.mesh_file_name = uploaded_file.filename
    db.session.commit()
    
    destination = os.path.join('meshes/',uploaded_file.filename)
    uploaded_file.save(destination)

    return jsonify({"message": "File Uploaded Successfully"}), 201

@app.route("/create_simulation", methods=["POST"])
def create_simulation():
    simulation = Simulation.query.get(1)
    if simulation :
        db.session.delete(simulation)
        db.session.commit()

    new_simulation = Simulation()
    new_simulation.id = 1
    new_simulation.t_start = 0
    new_simulation.t_end = 10
    new_simulation.dt = 0.1
    new_simulation.u_in = 20
    new_simulation.u_out = -20
    new_simulation.mesh_file_name = ""
    db.session.add(new_simulation)
    db.session.commit()

    return jsonify({"message": "Simulation Created!"}), 201

def get_simulation():
    simulation = Simulation.query.get(1)

    if not simulation:
        return jsonify({"message": "Simulation does not exist"})
    else:
        return simulation
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)