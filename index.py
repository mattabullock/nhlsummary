import requests
import json
from flask import Flask, request, render_template
from nhlsummary.object import Player
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/hockey.db'
db = SQLAlchemy(app)

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
        print players[id]
        player_id = players[id]['id']
        first_name = players[id]['firstName']
        last_name = players[id]['lastName']
        new_player = Player.Player(player_id, first_name, last_name)

        playerObjects.append(new_player.getJSON())

    return json.dumps(playerObjects)

def getData(game_id):
    url = 'http://statsapi.web.nhl.com/api/v1/game/' + game_id + '/feed/live'
    return requests.get(url)

if __name__ == "__main__":
    app.run()
