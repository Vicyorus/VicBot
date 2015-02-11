"""
MWHair - Mediawiki wrapper
Description - This is a mediawiki client written by Hairr <hairrazerrr@gmail.com>
It was orignally created to be used at http://runescape.wikia.com/

This library is free software; you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation; either version 2.1 of the License, or (at your option)
any later version.

This library is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import urllib2
import urllib
import json
import sys
import time
from cookielib import CookieJar

__version__ = 2.0
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.add_headers = [('User-Agent','Python Mwhair')]

def site(site):
	"""
	@description: Sets the wiki's api
	@use:
	import mwhair

	mwhair.wiki('http://foo.com/api.php')
	@other: You must specifiy the url of the api with the http protocol and without the www
	"""
	global wiki
	wiki = site + "/api.php"

def login(username, password):
	"""
	@description: Used to login to the mediawiki through the API
	@use:
	import mwhair

	mwhair.login(username, password)
	"""
	login_data = { 
	'action'    :  'login',
	'lgname'    : username, 
	"lgpassword": password, 
	'format'    : 'json'
	}
	data = urllib.urlencode(login_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	login_data['lgtoken'] = content['login']['token']
	data = urllib.urlencode(login_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	if content['login']['result'] == 'Success':
		print 'Now logged in as %s' % content['login']['lgusername']
		edittokens()
	elif content ['login']['result'] == 'NeedToken':
		print 'Error occured while trying to log in...'
		sys.exit(1)
	elif content ['login']['result'] == 'WrongPass':
		print 'Incorrect password.'
		sys.exit(1)
	else:
		print 'Error occured.'
		sys.exit(1)

def logout():
	"""
	@description: Used to logout of the wiki through the API
	@use:
	import mwhair

	mwhair.logout()
	"""
	logout_data = {
	'action':'logout',
	'format':'json'
	}
	data = urllib.urlencode(logout_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	print "Successfully logged out"

def edittokens():
	"""
	@description: Used to gather tokens to edit, delete, protect, move, block, unblock, email, and import
	@use: This shouldn't be used in a seperate script, the information is gathered on login and used throughout mwhair
	"""
	edit_token_data = {
	'action':'query',
	'prop':'info',
	'titles':'Main Page',
	'intoken':'edit|delete|protect|move|block|unblock|email|import',
	'format':'json'
	}
	data = urllib.urlencode(edit_token_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	try:
		warnings = content['warnings']['info']['*']
	except:
		warnings = None
	if warnings != None:
		if 'edit' in warnings:
			print 'No edit token: Quitting....'
			sys.exit(1)
		else:
			global edit_token
			edit_token = thes['edittoken']

		if 'delete' in warnings:
			global delete_token
			delete_token = None
		else:
			delete_token = thes['deletetoken']

		if 'protect' in warnings:
			global protect_token
			protect_token = None
		else:
			protect_token = thes['protecttoken']

		if 'move' in warnings:
			global move_token
			move_token = None
		else:
			move_token = thes['movetoken']

		if 'block' in warnings:
			global block_token
			block_token = None
		else:
			block_token = thes['blocktoken']

		if 'unblock' in warnings:
			global unblock_token
			unblock_token = None
		else:
			unblock_token = thes['unblocktoken']

		if 'email' in warnings:
			email_token = None
		else:
			email_token = thes['emailtoken']

		if 'import' in warnings:
			import_token = None
		else:
			import_token = thes['importtoken']
	else:
		edit_token = thes['edittoken']
		delete_token = thes['deletetoken']
		protect_token = thes['protecttoken']
		move_token = thes['movetoken']
		block_token = thes['blocktoken']
		unblock_token = thes['unblocktoken']
		email_token = thes['emailtoken']
		import_token = thes['importtoken']

def edit(title, section=None):
	"""
	@description: Gathers information about a specified page
	@use:import mwhair

	foo = mwhair.edit('bar')
	@other: This then makes the variable foo the contents of bar
	"""
	read_page_data = {
	'action':'query',
	'prop':'revisions',
	'titles':title,
	'rvprop':'timestamp|content',
	'format':'json'
	}
	if section:
		read_page_data['rvsection'] = section
	data = urllib.urlencode(read_page_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	try:
		wikipage = thes['revisions'][0]['*']
		return wikipage
	except KeyError:
		wikipage = ''
		return wikipage


def save(title, text='',summary='',minor=False,bot=True,section=False):
	"""
	@description: Saves the contents of the page
	@use:
	import mwhair

	mwhair.save('foo')
	@other: text needs to be specified, if not, the page will only be purged
	to create a non-bot edit, specifiy bot=False, otherwise, it'll be marked as a bot edit
	"""
	save_data = {
	'action':'edit',
	'title':title,
	'summary':summary,
	'token':edit_token,
	'format':'json'
	}
	try:
		save_data['text'] = text.encode('utf-8')
	except:
		save_data['text'] = text
	if bot is False:
		pass
	else:
		save_data['bot'] = 'True'
	if minor != False:
		save_data['minor'] = minor
	if not text:
		save_data['text'] = purge(title) # This will make the page purge
	if section != False:
		save_data['section'] = section
	if text:
		data = urllib.urlencode(save_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content

def userrights(title):
        user_right_data = {
        'action':'query',
        'list':'users',
        'ususers':title,
        'usprop':'groups',
        'format':'json'
        }
        data = urllib.urlencode(user_right_data)
        response = opener.open(wiki,data)
        content = json.load(response)
        rights = tuple(content['query']['users'][0]['groups'])
        for group in rights:
                returnlist = [group for group in rights]
                if u'sysop' in returnlist or u'chatmoderator' in returnlist:
                        return True
                else:
                        return False
