import os
from flask import Flask, request
from commands import getImage, cheerUp, emptySearch
app = Flask(__name__)

# This is a dictionary that uses the group ID as the key
# and the Bot ID as the value
bot_ids = {
	'25759439':'6dde2d1f7ffcf21e690d6061bd',
	'27647802':'73b1c786742081243a7e44b2d7'
}

@app.route('/', methods=['POST'])
def result():
	#receive JSON from groupme request containing message information
	message = request.get_json(force=True)
	#retrieve the appropriate bot_id from the JSON
	bot_id = bot_ids[message['group_id']]
	#send .gif message
	if message['text'].startswith('/gif '):
		searchTerm = message['text'][5:]
		# If we actually have something that is more than a space
		if searchTerm and not searchTerm.isspace():
			print('Valid search')
			getImage(searchTerm, bot_id)
		else:
			print('EMPTY SEARCH')
			emptySearch(bot_id)

	#send cheerUp message
	elif message['text'].startswith('/cheerup'):
		cheerUp(bot_id)
	return "Success"
	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
