#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import urllib2
import codecs
import sys
from timer import GetInHMS
import datetime

titleInfo = ''
uploaderName = ''
CountInfo = '' 
UploadDate = '' 
RatingInfo = '' 
lenghtInfo = ''
def youtube(url):
	    videoName = url
            f = urllib2.urlopen("http://gdata.youtube.com/feeds/api/videos/" + videoName)
            for line in f:
	        if "<title type='text'>" in line:
		    x = line
		    r = re.compile("<title type='text'>(.*?)</title><content")
		    m = r.search(x)
		    if m:
                        global titleInfo
                        titleInfo = m.group(1).decode('utf8')
                        
		if "viewCount" in line:
		    x = line
		    r = re.compile("viewCount='(.*?)'/>")
		    m = r.search(x)
		    if m:
		        global CountInfo
			CountInfo = "{:,}".format(int(m.group(1)))
		
		if "<published>" in line:
		    x = line
		    r = re.compile("<published>(.*?)T")
		    m = r.search(x)
		    if m:
		        global UploadDate
		        UploadDate = m.group(1)
		        
		if "<gd:rating average=" in line:
		     x = line
		     r = re.compile("<gd:rating average='(.*?)'")
		     m = r.search(x)
		     if m:
		        global RatingInfo
		        RatingInfo = m.group(1)

		if "<name>" in line:
                    x = line
                    r = re.compile("<name>(.*?)</name>")
                    m = r.search(x)
                    if m:
                        global uploaderName
                        uploaderName = m.group(1)
		        
		if "</media:title>" in line:
		    x = line
		    r = re.compile("</media:title><yt:duration seconds='(.*?)'/>")
		    m = r.search(x)
		    if m:
		        l = m.group(1)
		        global lenghtInfo
		        if int(l) < 3600:
                            lenghtInfo = GetInHMS(int(l), "%02d:%02d", 2)
                        else:
                            lenghtInfo = datetime.timedelta(seconds = int(l))
	    return "[YOUTUBE] Title: %s - Uploader: %s - Duration: %s - Views: %s - Uploaded: %s - http://youtu.be/%s" % (titleInfo, uploaderName, lenghtInfo, CountInfo, UploadDate, videoName)        
