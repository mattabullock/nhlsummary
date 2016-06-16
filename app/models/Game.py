from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json

class Game(db.Model):

    game_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(5))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    game_state = db.Column(db.String(15))
    game_state_id = db.Column(db.Integer)

    def __init__(self, params):
        self.game_id = params['game_id']
        self.type = params['type']
        self.start_time = params['start_time']
        self.end_time = params['end_time']
        self.game_state = params['game_state']
        self.game_state_id = params['game_state_id']

