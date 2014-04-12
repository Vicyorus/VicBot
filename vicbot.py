#!/usr/bin/env python
# -*- coding: UTF-8 -*-
##########################################################################
# VicBot - A chatbot/logger for Wikia Chats. 
#    Copyright (C) 2014  Vicyorus 
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
##########################################################################

#IMPORTS
import chatbot
import sys
import codecs
import time
from datetime import datetime
import wikibot
from command import command

#VARIABLES AND MISC.
wiki_username = sys.argv[1]
wiki_password = sys.argv[2]
wiki_name = 'http://' + sys.argv[3] +  '.wikia.com/'
wikibot.site(wiki_name)
command = command(wiki_username, wiki_password)
initial_time = time.time()
userdict = {}
#END OF VARIABLES

class VicBot(chatbot.ChatBot):
    def __init__(self):
        chatbot.ChatBot.__init__(self, wiki_username, wiki_password, wiki_name)
        self.last_updated = time.time()
        self.logger_on = True
        self.hello_status = True
        self.youtubeinfo = True
        self.twitterinfo = True
        self.seen = True
        self.new_day = False
        self.updated = False
        
    def on_welcome(self, c, e):
        print 'Logged in.'
        c.send('Hello')
               
    def on_join(self, c, e):
        if (self.logger_on):
            self.format_message(user=e.user.encode('ascii','ignore'),event='join')
        print '%s -!- %s has joined Special:Chat.' % (time.strftime('%H:%M', time.gmtime()), e.user)
        if e.user not in userdict or e.user in userdict:
            userdict[e.user] = time.time()
                    
    def on_leave(self, c, e):
        if (self.logger_on):
	    self.format_message(user=e.user.encode('ascii','ignore'),event='leave')
        print '%s -!- %s has left Special:Chat.' % (time.strftime('%H:%M', time.gmtime()), e.user)

    def on_kick(self, c, e):
        if (self.logger_on):
            self.format_message(user=e.user[0].encode('ascii','ignore'),
                                       mod=e.user[1].encode('ascii','ignore'),event='kick')
        print '%s -!- %s has been kicked by %s from Special:Chat.' % (time.strftime('%H:%M', time.gmtime()), e.user[0], e.user[1]) #Prints a copy on the console

    def on_ban(self, c, e):
        if (self.logger_on):
            if e.time != None:
		self.format_message(user=e.user[0].encode('ascii','ignore'),
                                        mod=e.user[1].encode('ascii','ignore'),time=e.time,event='ban')                                                                                                                                                      
            else:
		self.format_message(user=e.user[0].encode('ascii','ignore'),
                                        mod=e.user[1].encode('ascii','ignore'),event='unban')
        if e.time != None:
            print '%s -!- %s was banned from Special:Chat for %s seconds by %s' % (time.strftime('%H:%M', time.gmtime()),
                                                                                       e.user[0], e.time, e.user[1])
        else:
            print '%s -!- %s was unbanned from Special:Chat by %s' % (time.strftime('%H:%M', time.gmtime()),
                                                                          e.user[0], e.user[1])            

    def on_message(self, c, e):
        msg = e.text.lower()
        if (self.logger_on):
	    self.format_message(user=e.user,text=e.text,event='message')
            
        #Prints the messages on the console
        print u'%s <%s>: %s' % (time.strftime('%H:%M', time.gmtime()), e.user, e.text)
       
        #Hello command switch
        if msg.startswith('/hon') and not self.hello_status and (wikibot.userrights(e.user)):
            self.hello_status = True
            c.send('The /hello command is ON')
        elif msg.startswith('/hoff') and self.hello_status and (wikibot.userrights(e.user)):
            self.hello_status = False
            c.send('The /hello command is OFF')
       
        #Logging switch
        if msg.startswith('/lon') and not self.logger_on and (wikibot.userrights(e.user)):
            self.logger_on = True
	    c.send('Logging is ENABLED')	   
        elif msg.startswith('/loff') and self.logger_on and (wikibot.userrights(e.user)):
	    self.logger_on = False
	    command.update_command(None)
	    self.updated = True
	    c.send('Logging is DISABLED')
       
        #YouTube video information switch
        if msg.startswith('/yton') and not self.youtubeinfo and (wikibot.userrights(e.user)):
	    self.youtubeinfo = True
	    c.send('YouTube information is ON')
        elif msg.startswith('/ytoff') and self.youtubeinfo and (wikibot.userrights(e.user)):
	    self.youtubeinfo = False
  	    c.send('YouTube information is OFF')
       
        #Seen command switch
        if msg.startswith('/seenon') and not self.seen and (wikibot.userrights(e.user)):
	    self.seen = True
	    c.send('The /seen command is now ON')
        elif msg.startswith('/seenoff') and self.seen and (wikibot.userrights(e.user)):
	    self.seen = False
	    c.send('The /seen command is now OFF')
	   
        #Twitter tweet information switch
        if msg.startswith('/twon') and not self.twitterinfo and (wikibot.userrights(e.user)):
	    self.twitterinfo = True
	    c.send('Twitter information is ON')
        elif msg.startswith('/twoff') and self.twitterinfo and (wikibot.userrights(e.user)):
	    self.twitterinfo = False
	    c.send('Twitter information is OFF')
       
        #Hello command
        if msg.startswith('/hello'):
            c.send(command.hello_command(e.text))
       
        #Goodbye command
        if msg.startswith('/bye'):
            c.send('Goodbye!')  
       
        #Quit command
        if msg.startswith('/quit') and (wikibot.userrights(e.user)):
            sys.exit(1)

        #Updated command
        if msg.startswith('/updated') and (wikibot.userrights(e.user)):
            c.send(command.updated_command(e.user, self.last_updated, self.updated))
       
        #Logs command
        if msg.startswith('/logs'):
            c.send(command.log_command())

        #Dump buffer commannd
        if msg.startswith('/dumpbuffer') and (wikibot.userrights(e.user)):
            c.send(command.dump_buffer_command())

        #YouTube information
        if ('http' and 'youtu' in msg) and (e.user != wiki_username):
            c.send(command.youtube_info(e.text))

        #Seen command
        if msg.startswith('/seen '):
            if self.seen:
                if e.user not in userdict:
                    userdict[e.user] = time.time()
            c.send(command.seen_command(e.user, e.text, userdict, time.time()))  

        #Kicking command
        if msg.startswith('/kick') and (wikibot.userrights(e.user)):
	    try:
	        user = e.text.split(' ', 1)[1]
                if (wikibot.userrights(user)):
                    pass
                else:
	            c.kick_user(user)
	    except IndexError:
	        pass
       
        #Swear filter
        #if command.swear_filter(msg) and not (wikibot.userrights(e.user)):
        #    c.kick_user(e.user)	         
       
        #Log updater command
        if msg.startswith('/updatelogs') and (wikibot.userrights(e.user)):
            c.send(command.update_command(e.user))
            self.updated = True
       
        #Adds users to the user dictionary, for the !seen command
        if e.user not in userdict or e.user in userdict:
            userdict[e.user] = time.time()          
       
        #????
        if msg.startswith('/gauss '):
	    cond = e.text.replace("/gauss ", "")
            cond = cond.split(", ")
            try:
	        x = cond[0]
                y = cond[1]
                z = cond[2]
                c.send(command.gauss_progression(int(x), int(y), int(z)))
            except IndexError or ValueError:
	        pass
       
        if ('https://twitter.com/' in msg) and self.twitterinfo:
            c.send(command.twitter_info(e.text))
     
    def format_message(self, **kwargs):
	f = codecs.open('ChatBot.txt', 'a', encoding = 'utf-8')
        time = '%02d:%02d' % (datetime.utcnow().hour, datetime.utcnow().minute)
        if kwargs['event'] == 'join':
            f.write(time + ' -!- ' + kwargs['user'] + ' has joined Special:Chat.\n')
        elif kwargs['event'] == 'leave':
            f.write(time + ' -!- ' + kwargs['user'] + ' has left Special:Chat.\n')
        elif kwargs['event'] == 'message':
            f.write(time + ' <' + kwargs['user'] + '> ' + kwargs['text'] + '\n')
        elif kwargs['event'] == 'kick':
            f.write(time + ' -!- ' + kwargs['user'] + ' was kicked from Special:Chat by ' + kwargs['mod'] + '\n')
        elif kwargs['event'] == 'ban':
            f.write(time + ' -!- ' + kwargs['user'] + ' was banned from Special:Chat for ' + str(kwargs['time']) + ' seconds by ' + kwargs['mod'] + '.\n')
        elif kwargs['event'] == 'unban':
            f.write(time + ' -!- ' + kwargs['user'] + ' was unbanned from Special:Chat by ' + kwargs['mod'] + '.\n')
        f.close()
        
if __name__ == '__main__':
    bot = VicBot()
    bot.start()       
