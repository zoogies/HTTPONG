import requests as req

url = "http://127.0.0.1:8000/clientupdate"
headers = {
    "player": str(input("playerID: ")),
    "posy": input("ypos: "),
}
data = "game client request :)"  # TODO remove this for more efficient request?

print(req.post(url, headers=headers, data=data).content)
