import json

class Player:
    player_id = 0
    first_name = ''
    last_name = ''

    def __init__(self, player_id, first_name, last_name):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name

    def getJSON(self):
        obj = {
            'player_id' : self.player_id,
            'first_name' : self.first_name,
            'last_name' : self.last_name
        }
        return json.dumps(obj)
