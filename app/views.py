from app import app, db
from flask import request, render_template
from models.Player import Player
from models.Event import Event
from models.Game import Game
from models.PlayerEvent import PlayerEvent
import requests
import json
from datetime import datetime

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/data")
def data():
    game_id = request.args.get('gameid')
    game = Game.query.filter_by(game_id=game_id).first()
    print game
    if game is None:
        response = fullLoad(game_id)
    else:
        response = loadFromDB(game)
    return 'asdf'

@app.route("/scheduleGrab")
def grab():
    getFromSchedule('2015-10-01', '2016-06-15')
    return "nothing"

def getFromSchedule(start_date, end_date):
    url = 'http://statsapi.web.nhl.com/api/v1/schedule?startDate='+start_date+'&endDate='+end_date
    page_data = requests.get(url).text
    json_data = json.loads(page_data)
    for date in json_data['dates']:
        print date['date']
        for game in date['games']:
            fullLoad(game['gamePk'])

def loadFromDB(game):
    events = Event.query.join(PlayerEvent, Event.id==PlayerEvent.event_id).filter(Event.game_id==game.game_id).all()
    return 'asdf'

def fullLoad(game_id):
    page_data = getData(game_id).text
    players = getPlayers(page_data)
    getGame(page_data)
    getEvents(page_data)
    return 'asdf'

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
                'current_age' : players[id]['currentAge'] if 'currentAge' in players[id].keys() else None,
                'birth_city' : players[id]['birthCity'],
                'birth_state_province' : players[id]['birthStateProvince'] if 'birthStateProvince' in players[id].keys() else None,
                'birth_country' : players[id]['birthCountry'],
                'height' : players[id]['height'],
                'weight' : players[id]['weight'],
                'active' : players[id]['active'],
                'alternate_captain' : players[id]['alternateCaptain'] if 'alternateCaptain' in players[id].keys() else False,
                'captain' : players[id]['captain'] if 'captain' in players[id].keys() else False,
                'rookie' : players[id]['rookie'] if 'rookie' in players[id].keys() else False,
                'shoots_catches' : players[id]['shootsCatches'] if 'shootsCatches' in players[id].keys() else None,
                'roster_status' : players[id]['rosterStatus'],
                'current_team_id' : players[id]['currentTeam']['id'] if 'currentTeam' in players[id].keys() else -1,
                'primary_position' : players[id]['primaryPosition']['code']
            }
            new_player = Player(params)
            db.session.add(new_player)

    db.session.commit()

def getEvents(page_data):
    json_data = json.loads(page_data)
    all_plays = json_data['liveData']['plays']['allPlays']
    game_id = json_data['gamePk']

    event_ids = [event['about']['eventId'] for event in all_plays]
    db_events = Event.query.filter_by(game_id=game_id).filter(Event.id.in_(event_ids))
    for event in all_plays:
        db_hit = False
        for ev in db_events:
            if ev.game_id == game_id and ev.event_id == event['about']['eventId']:
                db_hit = True
        if db_hit:
            new_event = event
        else:
            if 'x' in event['coordinates'].keys():
                x_coord = event['coordinates']['x'];
                y_coord = event['coordinates']['y'];
            else:
                x_coord = None
                y_coord = None
            if 'team' in event.keys():
                team_id = event['team']['id']
            else:
                team_id = None
            params = {
                'game_id' : game_id,
                'event' : event['result']['event'],
                'event_type_id' : event['result']['eventTypeId'],
                'event_code' : event['result']['eventCode'],
                'event_idx' : event['about']['eventIdx'],
                'event_id' : event['about']['eventId'],
                'period' : event['about']['period'],
                'period_type' : event['about']['periodType'],
                'period_time' : event['about']['periodTime'],
                'date_time' : datetime.strptime(event['about']['dateTime'], '%Y-%m-%dT%H:%M:%SZ'),
                'home_goals' : event['about']['goals']['home'],
                'away_goals' : event['about']['goals']['away'],
                'x_coord' : x_coord,
                'y_coord' : y_coord,
                'team_id' : team_id
            }
            new_event = Event(params)
            db.session.add(new_event)

            for player in event['players']:
                params = {
                    'event_id' : new_event.id,
                    'player_id' : player['player']['id'],
                    'player_type' : player['playerType']
                }
                new_player_event = PlayerEvent(params)
                db.session.add(new_player_event)

    db.session.commit()

def getGame(page_data):
    json_data = json.loads(page_data)
    game = json_data['gameData']
    game_id = json_data['gamePk']
    db_game = Game.query.filter_by(game_id=game_id).first()
    if db_game:
        new_game = db_game
    else:
        params = {
            'game_id' : game['game']['pk'],
            'type' : game['game']['type'],
            'start_time' : datetime.strptime(game['datetime']['dateTime'], '%Y-%m-%dT%H:%M:%SZ'),
            'end_time' : datetime.strptime(game['datetime']['endDateTime'], '%Y-%m-%dT%H:%M:%SZ'),
            'game_state' : game['status']['abstractGameState'],
            'game_state_id' : game['status']['codedGameState']
        }
        new_game = Game(params)
        db.session.add(new_game)

    db.session.commit()

def getData(game_id):
    url = 'http://statsapi.web.nhl.com/api/v1/game/' + str(game_id) + '/feed/live'
    return requests.get(url)

if __name__ == "__main__":
    app.run()
