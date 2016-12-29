import requests
import sys
import random

GIF_LIMIT = 10

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
	request = requests.get(url, params=payload)
	# lets grab a random gif from the returned images.
	gif = random.choice(request.json()['data'])
	message = gif['images']['downsized']['url']
	botMessage(message, id)
	
def cheerUp(bot_id):
	compliments = open('compliments.txt')
	message = random.choice(compliments.readlines())
	id = bot_id
	botMessage(message, bot_id)
	
#def atGroup(bot_id):

	