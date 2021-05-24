import requests as req
import time
import random

url = "http://127.0.0.1:8000/clientupdate"  # TODO remove


class clientRequest:
    def __init__(self, adress, player, posy):
        if not type(adress) == str:
            raise "adress needs to be a string"
        if not type(player) == str:
            raise "player number needs to be a string"
        if not type(posy) == str:
            raise "player y position needs to be passed as a string"

        self.adress = adress + "clientupdate"
        self.connectadress = adress + "connect"
        self.headers = {
            "player": player,
            "posy": posy,
        }
        self.data = (
            "game client request :)"  # TODO remove this for more efficient request?
        )

    def postValues(self, posy):
        # print("HEADERS:", self.headers)
        self.headers["posy"] = str(posy)
        return str(req.post(self.adress, headers=self.headers, data=self.data).content)

    def connect(self, username):  # TODO matchmaking system
        return str(
            req.post(
                self.connectadress, headers="", data="client wants to connect :)"
            ).content
        )
