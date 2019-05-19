import requests
import sys
import os
import random
from utility import *


def get_image(search_term, gif_limit=1):
    """
    Stan searches the GIFY API for a gif that matches the search 
    term.
    """
    url = "http://api.giphy.com/v1/gifs/search"
    key = os.environ.get('GIPHY_KEY')
    payload = {
        'q': search_term,
        'limit': gif_limit,
        'api_key': key
    }
    try:
        request = requests.get(url, params=payload)
        # lets grab a random gif from the returned images.
        gif = random.choice(request.json()['data'])
        message = gif['images']['downsized']['url']
        bot_message(message)
    except requests.RequestException:
        # If we failed to find something from our search,
        # we send back an error message. Stan style.
        invalid_search()


def cheer_up(cheerup_file):
    """
    Stan sends a message that will cheer up the members of the group
    chat.
    """
    with open(cheerup_file) as compliments:
        message = random.choice(compliments.readlines()).strip()
        bot_message(message)


def help_me_stan(readme_file):
    """
    Will detail what stan can do and will use the README
    to grab all the information about the different functions
    """
    function_lines = []
    with open(readme_file) as readme:
        for line in readme:
            # We're checking to see if we hit the string that
            # shows when we're talking about commands
            if 'commands:' in line:
                for line in readme:
                    """
                     if we ever get to the point where commands
                     aren't last in the README, this is where
                     we'd break.
                    """
                    function_lines.append(line)
        
        message = ''.join(function_lines)
        bot_message(message)


def eye_bleach():
    """
    Will send 3 gifs/images that will be of adorable things that
    should cover up the current conversation screen. We'll just
    scrape from r/eyebleach
    """
    # we're going to grab the top five incase one of the submissions
    # is a reddit text post, then we can filter it out.
    submissions = obtain_hot_submissions('eyebleach', num_of_sub=5)

    sub_count = 0

    for submission in submissions:
        if 'reddit.com' not in submission.url and sub_count < 3:
            bot_message(submission.url)
            sub_count += 1


def crell_pic(image_file):
    with open(image_file) as pics:
        image = random.choice(pics.readlines())
        bot_image_message(image)
