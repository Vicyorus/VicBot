#!/usr/bin/env python
# -*- coding: UTF-8 -*-
###############################################################################
#                            ___      __________                         
#                            \  \    /  /  ____/                         
#                             \  \  /  /  /__                            
#                              \  \/  /   __/                            
#                               \    /  /____                             
#                                \__/_______/                            
#                                                                       
#                             VICBOT CLIENT CORE                          
#                                   MK. II                                
#
#    This program is free software: you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
###############################################################################

import re
import sys
import time
import json
import urllib
from threading import Timer, Thread
import cookielib
import urllib2
import os


import requests

__version__ = 2.0

#This is used to keep the bot running
running = True

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
        

class Client(object):
    def __init__(self, username, password, site):
        self.wiki_path = site + "wikia.php?controller=Chat&format=json"
        
        #Cookie jar
        self.cookie_jar = cookielib.CookieJar()
        
        #HTTP opener
        self.opener = requests.Session()
        self.headers = {
            'User-Agent': 'vicbot v.2.0.0',
            'Accept': '*/*',
            'Content-Type': 'application/octet-stream',
            'Connection': 'keep-alive'
        }
        
        #Basic operations
        self.__login(username, password, site)
        data = self.__wikia_request()

        #Set the settings values 
        self.settings = {
            'chatkey': data['chatkey'],
            'server': data['nodeInstance'],
            'host': data["nodeHostname"],
            'room': data["roomId"]
        }
        
        #Chat url
        self.chat_url = "http://{}/socket.io/".format(self.settings['host'])
        self.t = 0
        self.request_data = {
            'name': username,
            'key': self.settings["chatkey"],
            'roomId': self.settings["room"],
            'serverId': self.settings['server'],
            'EIO': 2,
            'transport': 'polling'
        }   
        
        #Initial
        self.__set_sid(self.settings)
        
    def post(self, data):
        try:
            #This checks if the request is a ping to the server
            #used to keep the connection alive
            if data == 'ping':
                body = self.format_message('2')
            else:
                body = self.format_message( '42' + json.dumps(['message', json.dumps({'id': None, 'attrs': data})]) )
            
            #These lines set the URL and request data 
            self.request_data['t'] = "{}-{}".format(self.__timestamp(), self.t)
            request_data = urllib.urlencode( self.request_data )
            url = self.chat_url + '?' + request_data
        
            #This is the actual call
            response = self.opener.post( url, data=body, headers=self.headers )
            self.t += 1
            return response
        except: #Handle any exception (timeout, connection reset, etc.)
            print "An error ocurred. Restarting."
            self.restart()
            
    def get(self):
        try:
            #These lines set the URL and request data 
            self.request_data['t'] = "{}-{}".format(self.__timestamp(), self.t)
            request_data = urllib.urlencode( self.request_data )
            url = self.chat_url + '?' + request_data
        
            #This is the actual call
            response = self.opener.get( url, headers=self.headers )
            self.t += 1
            return response
        except: #Handle any exception (timeout, connection reset, etc.)
            print "An error ocurred. Restarting."
            self.restart()
        

    def restart(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        
    def __login(self, username, password, wiki):
        login_data = {
            'action': 'login',
            'lgname': username,
            'lgpassword': password,
            'format':'json'}
        data = urllib.urlencode(login_data)
        response = self.opener.post(wiki + "/api.php",data=login_data)
        content = json.loads(response.content)
        login_data['lgtoken'] = content['login']['token']
        data = urllib.urlencode(login_data)
        response = self.opener.post(wiki + "/api.php",data=login_data)
        content = json.loads(response.content)
        if content['login']['result'] != 'Success':
            print 'Couldn\'t log in: Quitting.'
            sys.exit(1)
        else:
            print "Connected as: {}".format(username)

    def __wikia_request(self):
        response = self.opener.get(self.wiki_path)
        content = json.loads(response.content)
        return content

    def __set_sid(self, settings):
        response = self.get()
        
        #This should work while the response's length is less than 100
        content = json.loads( response.content[5:] )
        
        #Set the sid for future requests
        self.request_data['sid'] = content['sid']
        return

    def __timestamp(self):
        unix = time.time()
        return str(int(round(unix, 0)))

    def __connection(self):
        response = self.get().content
        if "\x00\x02\xff40" in response:
            self.socket_connect()
            match = re.findall('\x00\x02\xff40\x00.*\xff42\[.*?,(.*)\]', response)
            try:
                content = json.loads( match[0] )
                return content
            except:
                return "\x00\x02\xff40" 
        elif "\xff42[" in response:
            match = re.findall('\x00.*\xff42\[.*?,(.*)\]', response)
            content = json.loads( match[0] )
            return content
        
        else:
            return response
 
    def connection(self):
        var = self.__connection()
        return var
        

    #Socket-related functions
    #These functions are related to the response of the server
    #or having to ping the server
    def socket_connect(self):
        print "Logged in to chat!"
        ping_thr = Thread(target=self.socket_ping)
        ping_thr.daemon =True
        ping_thr.start()

    def socket_ping(self):
        time.sleep(24)
        self.post('ping')
        self.socket_ping()
        return
 
    #Encoding functions
    #These functions are used to encode information that's being sent to the server
    def int_to_encoded(self, length):
        payload = ''
        for c in str(length):
            payload += chr(int(c))
        return "\x00" + payload + "\xff"

    def format_message(self, message):
        return self.int_to_encoded( len(message) ) + message

    def send(self, message):
        self.post({'msgType': 'chat', 'text': message})
        return

    def kick_user(self, user):
        self.post({'msgType': 'command', 'command': 'kick', 'userToKick': user})
        return    

    def disconnect(self, nodisconnect=False):
        running = False
        self.post({'msgType': 'command', 'command': 'logout'})
        if not nodisconnect:
            sys.exit(1)
        return

    def initialize(self):
       return 


class ChatBot(Thread):
    def __init__(self, username, password, site):
        self.username = username
        self.password = password
        self.c = Client(username, password, site)
        Thread.__init__(self)

    def on_join(self, c, e):
        pass

    def on_leave(self, c, e):
        pass

    def on_message(self, c, e):
        pass

    def on_kick(self, c, e):
        pass

    def on_ban(self, c, e):
        pass


    def run(self):
        while running:
            content = self.c.connection()
            if content in ("\x00\x02\xff40", "\x00\x01\xff3"):
                pass
            elif "Session ID unknown" in content:
                print "Error: Session ID unknown"
                self.c.restart()
            else:
                e = Event(content)
                if content["event"] == "join":
                    self.on_join(self.c, e)
                elif content["event"] == "logout":
                    self.on_leave(self.c, e)
                elif content["event"] == "part":
                    self.on_leave(self.c, e)
                elif content["event"] == "kick":
                    self.on_kick(self.c, e)
                elif content["event"] == "ban":
                    self.on_ban(self.c, e)
                elif content["event"] == "chat:add":
                    self.on_message(self.c, e)
                    
if __name__ == '__main__':
    print("""This file isn't exucutable.
Please go to http://community.wikia.com/wiki/User:Hairr/Chatbot for information
on how to set up. Thanks.""")
