import re
import time
import YouTube
import urllib2
from URL import video_id
from timer import GetInHMS, seen
import wikibot
import codecs
from datetime import datetime
#Included some swears, feel free to add more
swear = ['ass', 'shit', 'bitch', 'boobs', 'cunt', 'dick', 'fuck', 'wanker', 'motherfucker', 'nigga',
         'nigger', 'penis', 'piss', 'pissed', 'pussy', 'sex', 'tits', 'whore']

class command(object):
  def __init__(self, username, password):
    self.username = username
    self.password = password
    
  #Hello command function. Returns "Hello there"
  def hello_command(self, message):
   if message[6:] == '':
         return "Hello there"
   else:
         return "Hello there,%s" % message[6:]

  #Updated command function. Returns the size of the log file and the last time it was updated (in case it was previously updated).
  def updated_command(self, user, timesec, updated):
    desired_time = int(time.time() - timesec)
    with open('ChatBot.txt') as f:
        if (updated == False):
            return "%s: The logs haven't been updated since I logged in. There are currently ~%d lines in the log buffer." % (user, len(f.readlines()))
        elif (updated):
            return "%s: The logs were last updated %s ago. There are currently ~%d lines in the log buffer." % (user, GetInHMS(desired_time, "%02d:%02d", 2), len(f.readlines()))

  #Dump buffer function. Clears the logfile, useful for spam attacks
  def dump_buffer_command(self):
    with open("ChatBot.txt", "w") as file:
         pass
    return "Log file cleared" 

  #Logs command. Returns the link to the logs page.
  def log_command(self):
    return "Logs can be seen [[Project:Chat/Logs|here]]."

  #YouTube information function. Returns a string with information about a video.
  def youtube_info(self, message):
    try:
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        m = url[0]
        url2 = str(video_id(m)) 
        return YouTube.youtube(url2)
    except urllib2.HTTPError, err:
         if err.code == 404 or err.code == 403:
                   pass
    except IndexError:
         pass

  #Update command function. Updates the logs to the current log page.
  def update_command(self, user):
    with open('ChatBot.txt') as f:
        log_file = len(f.readlines())
        self.update_logs(user)
        return "[[Project:Chat/Logs/%s|Logs]] updated (uploaded %d lines to the page)." % (time.strftime("%d %B %Y",                                                                                                                                                    time.gmtime()), log_file)             
      
  #Seen command. Tells the last time a certain user spoke.
  def seen_command(self, user, message, dictionary, time):
     seen_user = message.split(" ", 1)[1]
     if seen_user in dictionary:
                   seen_time = int(time- dictionary[seen_user])
                   if seen_time == 0 or user == seen_user or seen_user == self.username:
                       return "I just saw %s right now." % seen_user  
                   else:
                     return seen(seen_user, seen_time)
     else:                
               return "I haven't seen %s since I have been here." % (seen_user)

  #Log updater function.
  def update_logs(self, user):
      wikibot.login(self.username, self.password)
      f = codecs.open('ChatBot.txt', 'r', encoding='utf-8')
      a = f.read()
      f.close()                    
      utc = datetime.utcnow()
      logger_page = 'Project:Chat/Logs/' + time.strftime('%d %B %Y', time.gmtime())
      if user is not None:
         summary = 'Updating chat logs (requested by [[User:' + user + '|' + user + ']])'
      else:
         summary = 'Updating chat logs'
      try:
         cut = wikibot.edit(logger_page)
         text = cut[:-36]
      except KeyError:
         text = ''
      if text:
         new_text = text + '\n' + a.replace('<','&lt;').replace('>','&gt;') + '</pre>\n[[Category:Wikia Chat logs]]'
         wikibot.save(logger_page, new_text, summary=summary)
      else:
         new_text = '<pre class="ChatLog">\n' + a.replace('<','&lt;').replace('>','&gt;') + '</pre>\n[[Category:Wikia Chat logs]]'
         wikibot.save(logger_page, new_text, summary=summary)
      w = open('ChatBot.txt','w')
      w.write('')
      w.close()
      wikibot.logout()
      
  #Swear filter function. Kicks users in case a swear is included on the text.
  def swear_filter(self, text):
    for item in swear:
        if item in text:
            return True
            break