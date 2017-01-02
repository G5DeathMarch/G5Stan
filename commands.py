import requests
import sys
import random
from utility import botMessage, invalidSearch

GIF_LIMIT = 20

# ALL THE 'PYDOCS' (""") ARE USED FOR WHEN SOMEONE NEEDS HELP,
# NOT ACTUAL PYDOCS

# Searches the GIFY API for a gif that matches the search term.
def getImage(searchTerm, bot_id):
	"""
	/gif [searchTerm]: I try to find a gif that is relevant to
	the search term. Keyword is TRY.
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
	"""
	/cheerup: Everyone has a bad day and needs a pick-me-up. I
	gotchu.
	"""
	with open('compliments.txt') as compliments:
		message = random.choice(compliments.readlines())
		id = bot_id
		botMessage(message, bot_id)

def helpMeStan(bot_id, all_details):
	"""
	/helpmestan: I let you know what I can do.
	"""

	# These all details come from the help function of this
	# module, so we need to basically grab the function info
	print(type(all_details))
	print(all_details)
	# after_functions = all_details.split("FUNCTIONS", 1)[1]
	# function_info = after_functions.split("DATA",1)[0]
	# print(function_data)

#def atGroup(bot_id):

	