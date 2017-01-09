import requests
import sys
import random
from utility import botMessage, invalidSearch

GIF_LIMIT = 1

def getImage(searchTerm, bot_id):
	"""
	Stan searches the GIFY API for a gif that matches the search 
	term.
	"""
	url = "http://api.giphy.com/v1/gifs/search"
	key = os.environ.get('GIPHY_KEY')
	id = bot_id
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
		id = bot_id
		botMessage(message, bot_id)

def helpMeStan(bot_id, detail):
	"""
	Will take the detail what exactly Stan can do.
	If the detail is empty it will just print out the command
	names. If there is a detail it will try and print out the
	specifics of that command, or send an error if it can't find
	the command.

	Will use the README for this information
	"""
	pass


#def atGroup(bot_id):

	