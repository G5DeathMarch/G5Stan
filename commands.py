import requests
import sys
import random
import os
from utility import botMessage, invalidSearch

GIF_LIMIT = 1

def getImage(searchTerm, bot_id):
	"""
	Stan searches the GIFY API for a gif that matches the search 
	term.
	"""
	url = "http://api.giphy.com/v1/gifs/search"

	id = bot_id
	key = os.environ.get('GIPHY_KEY')
	payload = {
		'q':searchTerm,
		'limit': GIF_LIMIT,
		'api_key':key
	}
	try:
		request = requests.get(url, params=payload)
		# lets grab a random gif from the returned images.
		gif = random.choice(request.json()['data'])
		message = gif['images']['downsized']['url']
		botMessage(message, id)
	except:
		# If we failed to find something from our search,
		# we send back an error message. Stan style.
		invalidSearch(id)
	
def cheerUp(bot_id):
	"""
	Stan sends a message that will cheer up the members of the group
	chat.
	"""
	with open('compliments.txt') as compliments:
		message = random.choice(compliments.readlines())
		botMessage(message, bot_id)

def helpMeStan(bot_id):
	"""
	Will detail what stan can do and will
	use the README for this information
	"""
	with open('README.md') as readme:
		readme_content = readme.readlines()
		# We're grabbing everything about the different
		# functions of Stan.
		command_content = readme_content.split('commands:')[1]
		botMessage(command_content, bot_id)


#def atGroup(bot_id):

	