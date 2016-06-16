from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json

class Player(db.Model):

    player_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    birth_date = db.Column(db.DateTime, nullable=False)
    current_age = db.Column(db.Integer)
    birth_city = db.Column(db.String(30), nullable=False)
    birth_state_province = db.Column(db.String(30))
    birth_country = db.Column(db.String(30), nullable=False)
    height = db.Column(db.String(8), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    alternate_captain = db.Column(db.Boolean, nullable=False)
    captain = db.Column(db.Boolean, nullable=False)
    rookie = db.Column(db.Boolean, nullable=False)
    shoots_catches = db.Column(db.String(1))
    roster_status = db.Column(db.String(1), nullable=False)
    #current_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'))
    current_team_id = db.Column(db.Integer, nullable=False) #TODO: uncomment line above for prod
    primary_position = db.Column(db.String(2), nullable=False)

    def __init__(self, params):
        self.player_id = params['player_id']
        self.first_name = params['first_name']
        self.last_name = params['last_name']
        self.birth_date = params['birth_date']
        self.current_age = params['current_age']
        self.birth_city = params['birth_city']
        self.birth_state_province = params['birth_state_province']
        self.birth_country = params['birth_country']
        self.height = params['height']
        self.weight = params['weight']
        self.active = params['active']
        self.alternate_captain = params['alternate_captain']
        self.captain = params['captain']
        self.rookie = params['rookie']
        self.shoots_catches = params['shoots_catches']
        self.roster_status = params['roster_status']
        self.current_team_id = params['current_team_id']
        self.primary_position = params['primary_position']

