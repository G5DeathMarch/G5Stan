import requests, sys, os

#sends a standard message to the group
def botMessage(message):
	#retrieve the appropriate bot_id from the JSON
	bot_id = os.environ.get('BOT_ID')
	values = {
		'bot_id' : bot_id,
		'text' : str(message),
	}
	r = requests.post('https://api.groupme.com/v3/bots/post', data = values)

def invalidSearch():
	with open('failed_search.txt') as sayings:
		message = random.choice(sayings.readlines())
		botMessage(message)