from flask import jsonify
from config import app, db
from solver.helix_simulation import solveHelixSimulation


@app.route("/simulate", methods=["POST"])
def simulate():
    solveHelixSimulation()

    return jsonify({"message": "Simulation Finished!"}), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)