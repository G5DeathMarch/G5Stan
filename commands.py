import requests
import sys
import random

GIF_LIMIT = 20

#sends a standard message to the group
def botMessage(message, bot_id):
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post('https://api.groupme.com/v3/bots/post', data = values)

#retrieves gif from giphy API and sends it as a message
def getImage(searchTerm, bot_id):
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

# If Stan received an empty string to search, we're going
# to send back an error message.
def emptySearch(bot_id):
	with open('empty_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message, bot_id)

def invalidSearch(bot_id):
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message, bot_id)

#def atGroup(bot_id):

	