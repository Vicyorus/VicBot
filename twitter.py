import urllib2
import json
import re
from HTMLParser import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Twitter(object):

    def __init__(self, url):
        self.tweet_id = url[-18:]
        self.tweet = urllib2.urlopen('https://api.twitter.com/1/statuses/oembed.json?id=' + str(self.tweet_id)).read()
        self.tweet = json.loads(self.tweet)

    def tweet_text(self):
        r = re.compile('<blockquote class="twitter-tweet"><p>(.*?)</p>')
        m = r.search(self.tweet['html'])
        if m:
            text = m.group(1)
            if '&#10;' in text:
                text.replace('&#10;', ' ')
            h = HTMLParser()
            text = h.unescape(text)
            s = MLStripper()
            text = s.feed(text)
            return s.get_data()

    def tweet_user(self):
        r = re.compile('</p>&mdash; (.*?) <a')
        m = r.search(self.tweet['html'])
        if m:
            user = m.group(1).decode('utf8')
            return user

    def tweet_date(self):
        r = re.compile('{0}">(.*?)</a></blockquote>'.format(self.tweet_id))
        m = r.search(self.tweet['html'])
        if m:
            date = m.group(1)
            return date

    @property
    def tweet_info(self):
        return '[TWITTER] Text: {0} - User: {1} - Posted: {2}'.format(self.tweet_text(), self.tweet_user(), self.tweet_date())


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
