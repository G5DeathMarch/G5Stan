import requests
import sys
import praw
import os

#sends a standard message to the group
def botMessage(message, bot_id):
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post('https://api.groupme.com/v3/bots/post', data = values)

def invalidSearch(bot_id):
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message, bot_id)

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
