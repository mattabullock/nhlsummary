from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json

class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'))
    game_id = db.Column(db.Integer) #TODO: enable line above for prod
    event = db.Column(db.String(100), nullable=False)
    event_type_id = db.Column(db.String(100), nullable=False)
    event_code = db.Column(db.String(10), nullable=False)
    event_idx = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Integer, nullable=False)
    period_type = db.Column(db.Integer, nullable=False)
    period_time = db.Column(db.String(10), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    home_goals = db.Column(db.Integer, nullable=False)
    away_goals = db.Column(db.Integer, nullable=False)
    x_coord = db.Column(db.Integer)
    y_coord = db.Column(db.Integer)
    team_id = db.Column(db.Integer)

    def __init__(self, params):
        self.game_id = params['game_id']
        self.event = params['event']
        self.event_type_id = params['event_type_id']
        self.event_code = params['event_code']
        self.event_idx = params['event_idx']
        self.event_id = params['event_id']
        self.period = params['period']
        self.period_type = params['period_type']
        self.period_time = params['period_time']
        self.date_time = params['date_time']
        self.home_goals = params['home_goals']
        self.away_goals = params['away_goals']
        self.x_coord = params['x_coord']
        self.y_coord = params['y_coord']
        self.team_id = params['team_id']

