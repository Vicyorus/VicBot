import json


class Event(object):
    def __init__(self, connection):
        self.connection = self.parse(connection)

    def parse(self, connection):
        returned = {}
        if connection["event"] == "join":
            connection["data"] = json.loads(connection["data"])
            
        elif connection["event"] != "disableReconnect":
            connection["data"] = json.loads(connection["data"])
            
        if connection["event"] == "kick":
            returned["user"] = [connection["data"]["attrs"]["kickedUserName"],
                                connection["data"]["attrs"]["moderatorName"]]
            returned["text"] = None
            returned["time"] = None
        
        elif connection["event"] == "chat:add" and connection["data"]["attrs"].has_key("wfMsg"):
            returned["user"] = [connection["data"]["attrs"]["msgParams"][1],
                                connection["data"]["attrs"]["msgParams"][0]]
            returned["text"] = None
            returned["time"] = None
        
        elif connection["event"] == "ban":
            returned["user"] = [connection["data"]["attrs"]["kickedUserName"],
                         connection["data"]["attrs"]["moderatorName"]]
            returned["text"] = None
            returned["time"] = connection["data"]["attrs"]["time"]
        
        elif connection["event"] == "logout":
            returned["user"] = connection["data"]["attrs"]["name"]
            returned["text"] = None
            returned["time"] = None
        
        elif connection["event"] == "join":
            returned["user"] = connection["data"]["attrs"]["name"]
            returned["text"] = None
            returned["time"] = None
        
        elif connection["event"] == "part":
            returned["user"] = connection["data"]["attrs"]["name"]
            returned["text"] = None
            returned["time"] = None
        
        elif connection["event"] == "chat:add":
            returned["user"] = connection["data"]["attrs"]["name"]
            returned["text"] = connection["data"]["attrs"]["text"]
            returned["time"] = None
        
        else:
            returned["user"] = None
            returned["text"] = None
            returned["time"] = None
        return returned

    @property
    def user(self):
        if self.connection['user']:
            return self.connection["user"]
        else:
            return None

    @property
    def text(self):
        if self.connection['text']:
            return self.connection["text"]
        else:
            return None

    @property
    def time(self):
        if self.connection['time']:
            return self.connection["time"]
        else:
            return None
        