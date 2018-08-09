from __future__ import print_function
import sys # used for the storage class
import requests
import pycurl # used for curling
import base64 # used for encoding string
import urllib.parse # used for enconding
from io import StringIO# used for curl buffer grabbing
import io
import re
import json # used for decoding json token
import time # used for stuff to do with the rate limiting
from time import sleep # used for rate limiting
from time import gmtime, strftime # used for gathering time
import twitter_credentials

OAUTH2_TOKEN = 'https://api.twitter.com/oauth2/token'

class Storage:
    def __init__(self):
        self.contents = ''
        self.line = 0

    def store(self, buf):
        self.line = self.line + 1
        self.contents = "%s%i: %s" % (self.contents, self.line, buf)

    def __str__(self):
        return self.contents


def getYear():
	return strftime("%Y", gmtime())

def getMonth():
	return strftime("%m", gmtime())

def getDay():
	return strftime("%d", gmtime())

def getHour():
	return strftime("%H", gmtime())

def getMinute():
	return strftime("%M", gmtime())	

def generateFileName():
	return getYear()+"-"+getMonth()+"-"+getDay()+""

# grabs the rate limit remaining from the headers
def grab_rate_limit_remaining(headers):
	limit = ''
	h = str(headers).split('\n')
	for line in h:
		if 'x-rate-limit-remaining:' in line:
			limit = line[28:-1]
	return limit

# grabs the time the rate limit expires
def grab_rate_limit_time(headers):
	x_time = ''
	h = str(headers).split('\n')
	for line in h:
		if 'x-rate-limit-reset:' in line:
			x_time = line[24:-1]
	return x_time

# obtains the bearer token
def get_bearer_token(consumer_key,consumer_secret):
	# enconde consumer key
	consumer_key = urllib.parse.quote(consumer_key)
	# encode consumer secret
	consumer_secret = urllib.parse.quote(consumer_secret)
# 	print(type(consumer_secret))
	# create bearer token
	bearer_token = consumer_key+':'+consumer_secret
	# base64 encode the token
	base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))
    # set headers
	headers = {
		"Authorization": "Basic " + base64_encoded_bearer_token.decode('utf-8') + "",
		"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
		"Content-Length": "29"}

	response = requests.post(OAUTH2_TOKEN, headers=headers, data={'grant_type': 'client_credentials'})
	to_json = response.json()
	return to_json['access_token']


def grab_a_tweet(bearer_token, tweet_id):
	# url
	url = "https://api.twitter.com/1.1/trends/place.json"
	formed_url ='?id='+tweet_id+'&result_type=popular' #include_entities=true
	headers = [ 
	str("GET /1.1/statuses/show.json"+formed_url+" HTTP/1.1"), 
	str("Host: api.twitter.com"), 
	str("User-Agent: jonhurlock Twitter Application-only OAuth App Python v.1"),
	str("Authorization: Bearer "+bearer_token+"")
	]
	buf = io.BytesIO()
	tweet = ''
	retrieved_headers = Storage()
	pycurl_connect = pycurl.Curl()
	pycurl_connect.setopt(pycurl_connect.URL, url+formed_url) # used to tell which url to go to
	pycurl_connect.setopt(pycurl_connect.WRITEFUNCTION, buf.write) # used for generating output
	pycurl_connect.setopt(pycurl_connect.HTTPHEADER, headers) # sends the customer headers above
	pycurl_connect.setopt(pycurl_connect.HEADERFUNCTION, retrieved_headers.store)
	#pycurl_connect.setopt(pycurl_connect.VERBOSE, True) # used for debugging, really helpful if you want to see what happens
	pycurl_connect.perform() # perform the curl
	tweet += buf.getvalue().decode('UTF-8') # grab the data
	pycurl_connect.close() # stop the curl
	#print retrieved_headers
	pings_left = grab_rate_limit_remaining(retrieved_headers)
	reset_time = grab_rate_limit_time(retrieved_headers)
	current_time = time.mktime(time.gmtime())
	return {'tweet':tweet, '_current_time':current_time, '_reset_time':reset_time, '_pings_left':pings_left}

consumer_key = twitter_credentials.CONSUMER_KEY # put your apps consumer key here
consumer_secret = twitter_credentials.CONSUMER_SECRET # put your apps consumer secret here

bearer_token = get_bearer_token(consumer_key,consumer_secret)

tweet = grab_a_tweet(bearer_token,'23424848') # grabs a single tweet & some extra bits
print(type(tweet['tweet']))
print(tweet['_current_time'])
json_obj = json.loads(tweet['tweet'])

for i in json_obj:
    for j in i['trends']:
        print(j['name'])

