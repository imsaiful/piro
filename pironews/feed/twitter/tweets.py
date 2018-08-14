from __future__ import print_function
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
import numpy as np
import string
from nltk.corpus import stopwords
from collections import Counter
from nltk import word_tokenize
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

# Ignore this class, its just to do with handling of HTTP headers
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



# performs a basic search for a given query
def search_for_a_tweet(bearer_token, query):
	# url to perform search
	url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
	formed_url ='?screen_name='+query+'&count=200'
	headers = [ 
	str("GET /1.1/search/tweets.json"+formed_url+" HTTP/1.1"), 
	str("Host: api.twitter.com"), 
	str("User-Agent: jonhurlock Twitter Application-only OAuth App Python v.1"),
	str("Authorization: Bearer "+bearer_token+"")
	]
	buf = io.BytesIO()
	results = ''
	pycurl_connect = pycurl.Curl()
	pycurl_connect.setopt(pycurl_connect.URL, url+formed_url) # used to tell which url to go to
	pycurl_connect.setopt(pycurl_connect.WRITEFUNCTION, buf.write) # used for generating output
	pycurl_connect.setopt(pycurl_connect.HTTPHEADER, headers) # sends the customer headers above
	#pycurl_connect.setopt(pycurl_connect.VERBOSE, True) # used for debugging, really helpful if you want to see what happens
	pycurl_connect.perform() # perform the curl
	results = buf.getvalue().decode('UTF-8') # grab the data
	json_obj = json.loads(results)
# 	print(json_obj['text'])
	pycurl_connect.close() # stop the curl
	return results


	
# examples of how to use the code
consumer_key = twitter_credentials.CONSUMER_KEY # put your apps consumer key here
consumer_secret = twitter_credentials.CONSUMER_SECRET # put your apps consumer secret here

bearer_token = get_bearer_token(consumer_key,consumer_secret) # generates a bearer token
# print(type(bearer_token))
search_results = search_for_a_tweet(bearer_token,'BBCWorld') # does a very basic search
json_obj = json.loads(search_results)
print(json_obj[0]['created_at'])

tweets_list = []
for i in json_obj:
    sub = re.sub(r"http\S+", "", i['text'])
    if len(sub) > 40:
        tweets_list.append(sub)

tokens = [word_tokenize(i) for i in tweets_list]
    
    
stop_words = set(stopwords.words('english'))
    
PS = PorterStemmer()
filtered_sentence = []
for token in tokens:
    for word in token:
        if word.lower() not in stop_words:
            filtered_sentence.append(PS.stem(word.capitalize()))

# print(filtered_sentence)
    
counts = Counter(filtered_sentence)
l=list(counts.most_common(10))
for x in l:
    print(x)
    
#plotting Bar graph

label = [y[1] for y in l]
news = [x[0] for x in l]
index = np.arange(len(news))
plt.bar(index, label)
plt.xlabel('News', fontsize=15)
plt.ylabel('Number of news Appear', fontsize=15)
plt.xticks(index, news, fontsize=10, rotation=30)
plt.title('News today')
plt.show()


#pie chat
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(aspect="equal"))

recipe = [list(x) for x in l]
# print(recipe)

ingredients = [x[0] for x in recipe]
data= [float(x[1]) for x in recipe]


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))

ax.legend(wedges, ingredients,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 20, 1))

plt.setp(autotexts, size=10, weight="bold")

ax.set_title("Matplotlib News: A pie")

plt.show()

