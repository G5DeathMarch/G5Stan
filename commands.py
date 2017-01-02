import requests
import sys
import random
from utility import botMessage, invalidSearch

GIF_LIMIT = 20

def getImage(searchTerm, bot_id):
	"""
	/gif [searchTerm]: I try to find a gif that is relevant to
	the search term. 
	"""
	url = "http://api.giphy.com/v1/gifs/search"
	key = "dc6zaTOxFJmzC"
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
	with open('compliments.txt') as compliments:
		message = random.choice(compliments.readlines())
		id = bot_id
		botMessage(message, bot_id)

def helpMeStan(bot_id):
	details = help(this)
	print(details)

#def atGroup(bot_id):

	