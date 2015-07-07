import os
import urllib2
import codecs
import sys
from timer import GetInHMS
import datetime
from urlparse import *
import json

# TODO: Implement this class so it's only created once 
# instead of making one for each URL

class YouTube(object):
    #Thanks, Sactage!
    YOUTUBE_URL = "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=%s&key=%s"
    try:
        API_KEY = json.loads(open("config.json", "r").read())["youtube-key"]
    except KeyError:
        print "ERROR: No YouTube API key has been found, YouTube info is OFF."
        print "To use this functionality, you need a Public API access key from a Google Project."
        API_KEY = False
        
    def __init__(self, url):
        self.video_id = self.video_id(url)
        if self.API_KEY:
            self.video = json.loads(
            urllib2.urlopen(self.YOUTUBE_URL % (self.video_id, self.API_KEY)).read()
            )["items"][0]
        else:
            self.video = False

    def video_id(self, value):
        query = urlparse(value)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com', 'm.youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]

    @property
    def video_information(self):
        if self.video:
            return '[YOUTUBE] Title: {0} - Uploader: {1} - Views: {2} - http://youtu.be/{3}'.format(
                self.video["snippet"]["title"], 
                self.video["snippet"]["channelTitle"], 
                self.video["statistics"]["viewCount"], 
                self.video_id
            )
        else:
            return ""
