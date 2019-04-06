"""
File that contains functions that provide us some common
functionality for other classes / files
"""

import requests
import os
import praw
import random

API_PATH = 'https://api.groupme.com/v3'
BASE_URL = 'https://api.groupme.com/v3/bots/post'


# sends a standard message to the group
def bot_message(message):
    bot_id = os.environ.get('BOT_ID')
    values = {
        'bot_id': bot_id,
        'text': str(message),
    }
    print("send message values: {}".format(values))
    r = requests.post(BASE_URL, json=values)


def bot_image_message(image_url):
    bot_id = os.environ.get('BOT_ID')
    values = {
            'bot_id': bot_id,
            'attachments': [{
                'type': 'image',
                'url': image_url.strip()
            }]
    }
    print("send image values: {}".format(values))
    r = requests.post(BASE_URL, json=values)


def mention(message, mention_indices, mention_uids):
    """
    Sends a message that has a mention in the text.
    message should contain the @mentions 
    mention_indices array of arrays that contain [index, length]
    mention_uids: array of user ids, should match with the mention_indices
    """
    bot_id = os.environ.get('BOT_ID')
    values = {
        'bot_id': bot_id,
        'text': str(message),
        'attachments': {
            'type': 'mentions',
            'loci': mention_indices,
            'user_ids': mention_uids
        }
    }

    print("mention values: {}".format(values))

    r = requests.post(BASE_URL, json=values)


def get_members(group_id):
    """
    Will grab all the current members in the group and return
    them.
    """
    token = os.environ.get('GROUPME_TOKEN')    
    url_string = '{0}/groups/{1}?token={2}'.format(API_PATH, group_id, token)
    r = requests.get(url_string)
    json = r.json()

    print("Members: {}".format(json['response']['members']))

    return json['response']['members']


def invalid_search():
    with open('resources/failed_search.txt') as sayings:
        message = random.choice(sayings.readlines()).strip()
        bot_message(message)


def obtain_hot_submissions(subreddit_name, num_of_sub=1):
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
