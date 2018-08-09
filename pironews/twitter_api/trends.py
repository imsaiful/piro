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

