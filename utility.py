import requests
import sys

#sends a standard message to the group
def botMessage(message, bot_id):
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post('https://api.groupme.com/v3/bots/post', data = values)

def invalidSearch(bot_id):
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message, bot_id)