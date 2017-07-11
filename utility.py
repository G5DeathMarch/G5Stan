import requests, sys, os, praw, re

API_PATH = 'https://api.groupme.com/v3'

#sends a standard message to the group
def botMessage(message):
	#retrieve the appropriate bot_id from the JSON
	bot_id = os.environ.get('BOT_ID')
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post(API_PATH + '/bots/post', data = values)

def mention(message, mention_locations, mention_uids):
	"""
	Will send a message with a groupme mention within the text.
	ex: '@person1 i'm mentioning you'

	message: The string mention that contains both the '@username' mention
			 as well as the rest of the message being sent.
	mention_locations: a 2D array that stores the index in the message where the
		     mention starts and how long the mention text is. For example, with
		     the example message above you'll see [[0, 6]].
	mention_uids: an array of user ids where the index of them matches the index
		     of the locations.
	"""
	bot_id = os.environ.get('BOT_ID')
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
		'attachments' : {
			'type' : 'mentions',
			'loci' : mention_locations,
			'user_ids' : mention_uids
		}
	}

	r = requests.post(API_PATH + '/bots/post', data = values)


def invalidSearch():
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message)

def obtainHotSubmissions(subreddit_name, num_of_sub=1):
	"""
	Will take a subreddit string, and will grab a 
	number of hot urls and return them. The subreddit 
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

def stringToSeconds(time_string):
	"""
	Will take a string that determines time and will convert it
	into the corresponding amound of seconds. 

	Ex: '1 minute 30 seconds' or '1 minutes and 30 seconds' will both
	output 90. 

	time_string: The string that designates time. 
	"""
	# This is a python object that we're going to use to convert
	# specific strings into seconds.
	string_second_dict = { 
		'second': 1,
		'minute': 60,
		'hour': 3600,
		'day': (24 * 3600),
		'week': (7 * 24 * 3600),
		'month': (30.5 * 24 * 3600), # Approx 30 and a half days per month.
		'year': (12 * 30.5 * 24 * 3600)
	}

	time_string = time_string.lower()

	# First things first, we're going to remove the 'and' since it
	# really doesn't mean anything.
	time_string = re.sub(r"and?", "", time_string)


