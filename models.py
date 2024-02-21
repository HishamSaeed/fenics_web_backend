from config import db

class Simulation(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    t_start = db.Column(db.Float, unique=False, nullable=False)
    t_end = db.Column(db.Float, unique=False, nullable=False)
    dt = db.Column(db.Float, unique=False, nullable=False)
    u_in = db.Column(db.Float, unique=False, nullable=False)
    u_out = db.Column(db.Float, unique=False, nullable=False)

    def to_json(self):
        return {
            "tStart": self.t_start,
            "tEnd": self.t_end,
            "dt": self.dt,
            "uIn": self.u_in,
            "uOut": self.u_out,
        }