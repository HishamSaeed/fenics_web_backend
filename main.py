from flask import jsonify, request
from config import app

@app.route("/")
def home():
    return 'Hello, world! , this is just a demo for flask . This is a demo for fenicsWeb, test CORS main program'

@app.route('/t_start', methods=["GET"])
def getTStart():
    response = jsonify({'tStart': 742}) 
    return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')    