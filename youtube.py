import os
import re
import urllib2
import codecs
import sys
from timer import GetInHMS
import datetime
from urlparse import *

class YouTube(object):
    def __init__(self, url):
        self.video_id = self.video_id(url)
        self.video = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/' + self.video_id).read()

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

    def title_info(self):
        if "<title type='text'>" in self.video:
            x = self.video
            r = re.compile("<title type='text'>(.*?)</title><content")
            m = r.search(x)
            if m:
                titleInfo = m.group(1).decode('utf8')
            return titleInfo

    def views(self):
        if 'viewCount' in self.video:
            x = self.video
            r = re.compile("viewCount='(.*?)'/>")
            m = r.search(x)
            if m:
                CountInfo = '{:,}'.format(int(m.group(1)))
            return CountInfo

    def publish_date(self):
        if '<published>' in self.video:
            x = self.video
            r = re.compile('<published>(.*?)T')
            m = r.search(x)
            if m:
                UploadDate = m.group(1)
            return UploadDate

    def rating_ratio(self):
        if '<gd:rating average=' in self.video:
            x = self.video
            r = re.compile("<gd:rating average='(.*?)'")
            m = r.search(x)
            if m:
                RatingInfo = m.group(1)
            return RatingInfo

    def uploader_name(self):
        if '<name>' in self.video:
            x = self.video
            r = re.compile('<name>(.*?)</name>')
            m = r.search(x)
            if m:
                uploaderName = m.group(1)
            return uploaderName

    def video_lenght(self):
        if '</media:title>' in self.video:
            x = self.video
            r = re.compile("</media:title><yt:duration seconds='(.*?)'/>")
            m = r.search(x)
            if m:
                l = m.group(1)
                if int(l) < 3600:
                    lenghtInfo = GetInHMS(int(l), '%02d:%02d', 2)
                else:
                    lenghtInfo = datetime.timedelta(seconds=int(l))
            return lenghtInfo

    @property
    def video_information(self):
        return '[YOUTUBE] Title: {0} - Uploader: {1} - Duration: {2} - Views: {3} - Uploaded: {4} - http://youtu.be/{5}'.format(self.title_info(), self.uploader_name(), self.video_lenght(), self.views(), self.publish_date(), self.video_id)