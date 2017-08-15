"""
File that contains functions that provide us some common
functionality for other classes / files
"""

import requests, sys, os, praw, random

GROUPME_BOT_PATH = 'https://api.groupme.com/v3/bots/'

#sends a standard message to the group
def botMessage(message):
	#retrieve the appropriate bot_id from the JSON
	bot_id = os.environ.get('BOT_ID')	
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post(GROUPME_BOT_PATH + 'post', data=values)

def invalidSearch():
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message)

def obtainHotSubmissions(subreddit_name, num_of_sub=1):
	"""
	Will take a subreddit string, and will grab a 
	number of urls and return them. The subreddit 
	string doesn't need the r/, but we'll make sure to 
	get rid of it before hand.
	"""
	# remove the r/ from the subreddit name
	if subreddit_name.startswith('r/'):
		subreddit_name = subreddit_name[2:]

	reddit = praw.Reddit(client_id=os.environ.get('REDDIT_CLIENT_ID'),
						 client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
						 user_agent=os.environ.get('USER_AGENT'),
						 username=os.environ.get('REDDIT_USERNAME'),
						 password=os.environ.get('REDDIT_PASSWORD'))

	subreddit = reddit.subreddit(subreddit_name)

	return subreddit.hot(limit=num_of_sub)
