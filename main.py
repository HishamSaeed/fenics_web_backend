from flask import jsonify, request
from config import app


@app.route("/")
def home():
    print("Hello world")
    return 'Hello, world! , this is just a demo for flask . This is a demo for fenicsWeb, test CORS'

if __name__ == "__main__":
    ##with app.app_context():
    ##    db.create_all()
    app.run(debug=True)    
    ## socketIo.run(app=app, debug=True)