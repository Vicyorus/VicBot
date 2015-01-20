import re
import time
import youtube
import urllib2
from timer import GetInHMS, seen
import wikibot
import codecs
import twitter

class command(object):
    def __init__(self, vicbot, username, password):
        self.c = vicbot
        self.username = username
        self.password = password
        wikibot.login(self.username, self.password)
    
    #Hello command function. Returns "Hello there"
    def hello_command(self, message):
        if message[6:] == '':
            return 'Hello there'
        else:
            return 'Hello there,%s' % message[6:]

    #Updated command function. Returns the size of the log file and the last time it was updated (in case it was previously updated).
    def updated_command(self, user):
        desired_time = int(time.time() - self.c.last_updated)
        with open('ChatBot.txt') as f:
            if self.c.updated:
                return '{}: The logs were last updated {} ago. There are currently ~{} lines in the log buffer.'.format(user, GetInHMS(desired_time, '%02d:%02d', 2), len(f.readlines()))
            else:
                return "{}: The logs haven't been updated since I logged in. There are currently ~{} lines in the log buffer.".format(user, len(f.readlines()))  
  
    #Dump buffer function. Clears the logfile, useful for spam attacks
    def dump_buffer_command(self):
        open('ChatBot.txt', 'w').close()
        return 'Log file cleared'

    #Logs command. Returns the link to the logs page.
    def log_command(self, user):
        return "{}: Logs can be seen [[Project:Chat/Logs|here]].".format(user)

    #YouTube information function. Returns a string with information about a video.
    def youtube_info(self, message):
        try:
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            url2 = url[0]
            if ('youtube.com' in url2 and 'watch?v=' in url2) or ('youtu.be' in url2):
                yt = youtube.YouTube(url2)
                return yt.video_information
            else:
                pass
        except urllib2.HTTPError as err:
            if err.code == 404 or err.code == 403:
                pass
        except IndexError or TypeError:
            pass

    #Update command function. Updates the logs to the current log page.
    def update_command(self, user):
        with open('ChatBot.txt') as f:
            #Leave the variable in here
            log_file = len(f.readlines())
            self.update_logs(user)
            return '{}: [[Project:Chat/Logs/{}|Logs]] updated (uploaded {} lines to the page).'.format(user, time.strftime('%d %B %Y', time.gmtime()), log_file)
  
    #Seen command. Tells the last time a certain user was seen in chat.
    def seen_command(self, user, message, dictionary, time):
        seen_user = message.split(' ', 1)[1]
        if seen_user in dictionary:
            seen_time = int(time - dictionary[seen_user])
            if seen_time == 0 or user == seen_user or seen_user == self.username:
                return 'I just saw %s right now.' % seen_user
            else:
                return seen(seen_user, seen_time)
        else:
            return "I haven't seen %s since I have been here." % seen_user

    #Log updater function.
    def update_logs(self, user=None):
        f = codecs.open('ChatBot.txt', 'r', encoding='utf-8')
        a = f.read()
        f.close()
        logger_page = 'Project:Chat/Logs/' + time.strftime('%d %B %Y', time.gmtime())
        if user is not None:
            summary = 'Updating chat logs (requested by [[User:' + user + '|' + user + ']])'
        else:
            summary = 'Updating chat logs'
        try:
            cut = wikibot.edit(logger_page)
            text = re.findall('(.*)\</pre\>', cut, re.DOTALL)[0]
        except:
            text = ''
        if text:
            new_text = text + a.replace('<', '&lt;').replace('>', '&gt;') + '</pre>\n[[Category:Wikia Chat logs|{0}]]'.format(time.strftime('%Y %m %d', time.gmtime()))
            wikibot.save(logger_page, new_text, summary=summary)
        else:
            new_text = '<pre class="ChatLog">\n' + a.replace('<', '&lt;').replace('>', '&gt;') + '</pre>\n[[Category:Wikia Chat logs|{0}]]'.format(time.strftime('%Y %m %d', time.gmtime()))
            wikibot.save(logger_page, new_text, summary=summary)
        
        #Clearing the log file
        open('ChatBot.txt', 'w').close()
        
        
        #Modify some important values on the client
        self.c.updated = True
        self.c.last_updated = time.time()
        self.c.log_thread()
        
    
    #Gauss command. Sums all the numbers on a secuence from 'x' to 'y' with a difference of 'z'.  
    def gauss_progression(self, x, y, z):
        if z != 0:
            if z > 0 and y > x or z < 0 and x > y:
                num = ((y - x) / z + 1) * (x + y) / 2
                return 'The sum of all the numbers from %d to %d with a common difference of %d is %d' % (x, y, z, num)
            else:
                return 'Incorrect value of first and/or last value of the sequence and/or common difference'
        else:
            return 'Incorrect value for common difference'

    #Twitter information. Returns a string with information from a specific tweet.
    def twitter_info(self, message):
        try:
            url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
            URL = url[0]
            t = twitter.Twitter(URL)
            return t.tweet_info
        except urllib2.HTTPError as err:
            if err.code == 404 or err.code == 403:
                pass
        except IndexError:
            pass
        
    def tell_say(self, user, tell):
        return "{0}, {1} told you: {2}".format(user, tell['user'], tell['text'])  
