from flask import request
import requests, sys, os, praw

BOT_PATH = 'https://api.groupme.com/v3/bots/'

#sends a standard message to the group
BASE_URL = 'https://api.groupme.com/v3/bots/post'

def botMessage(message):
    bot_id = os.environ.get('BOT_ID')
    values = {
        'bot_id' : bot_id,
        'text' : str(message),
    }
    print("send message values: {}".format(values))
    r = requests.post(BASE_URL, json = values)

def botImageMessage(image_url):
    bot_id = os.environ.get('BOT_ID')
    values = {
            'bot_id' : bot_id,
            'attachments' : [{
                'type' : 'image',
                'url' : image_url.strip()
            }]
    }
    print("send image values: {}".format(values))
    r = requests.post(BASE_URL, json = values)

def getMembers():
	"""
	Will grab all the current members in the group and return
	them.
	"""
	bot_id = os.environ.get('BOT_ID')
	# the group id is needed to grab the members in groupme
	group_id = request.get_json(force=True)['group_id']
	values = {
		'id' : group_id
	}

	r = requests.get(BOT_PATH + '/get', data=values)
	print(r['members'])

def invalidSearch():
    with open('failed_search.txt') as sayings:
        message = random.choice(sayings.readlines()).strip()
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
