from flask import request, render_template
from models.Player import Player
from app import app, db
import requests
import json
from datetime import datetime

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data")
def data():
    # game_id = request.args.get('gameid')
    game_id='2015020884'
    page_data = getData(game_id).text
    return getPlayers(page_data)

def getPlayers(page_data):
    json_data = json.loads(page_data)
    players = json_data['gameData']['players']

    playerObjects = []
    for id in players:
        player = Player.query.filter_by(player_id=players[id]['id']).first()
        if player is not None:
            new_player = player
        else:
            params = {
                'player_id' : players[id]['id'],
                'first_name' : players[id]['firstName'],
                'last_name' : players[id]['lastName'],
                'birth_date' : datetime.strptime(players[id]['birthDate'], '%Y-%m-%d'),
                'current_age' : players[id]['currentAge'],
                'birth_city' : players[id]['birthCity'],
                'birth_state_providence' : players[id]['birthStateProvidence'] if 'birthStateProvidence' in players[id] else None,
                'birth_country' : players[id]['birthCountry'],
                'height' : players[id]['height'],
                'weight' : players[id]['weight'],
                'active' : players[id]['active'],
                'alternate_captain' : players[id]['alternateCaptain'],
                'captain' : players[id]['captain'],
                'rookie' : players[id]['rookie'],
                'shoots_catches' : players[id]['shootsCatches'],
                'roster_status' : players[id]['rosterStatus'],
                'current_team_id' : players[id]['currentTeam']['id'],
                'primary_position' : players[id]['primaryPosition']['code']
            }
            new_player = Player(params)
            db.session.add(new_player)

        playerObjects.append(new_player.getJSON())

    db.session.commit()
    return json.dumps(playerObjects)

def getData(game_id):
    url = 'http://statsapi.web.nhl.com/api/v1/game/' + game_id + '/feed/live'
    return requests.get(url)

if __name__ == "__main__":
    app.run()
