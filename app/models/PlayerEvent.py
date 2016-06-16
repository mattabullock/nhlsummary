from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db
import json

class PlayerEvent(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.player_id'))
    player_type = db.Column(db.String(10), nullable=False)

    def __init__(self, params):
        self.event_id = params['event_id']
        self.player_id = params['player_id']
        self.player_type = params['player_type']

