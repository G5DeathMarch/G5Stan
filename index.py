import os
import commands
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
	#receive JSON from groupme request containing message information		
 	message = request.get_json(force=True)
	#retrieve the appropriate bot_id from the JSON
	bot_id = os.environ.get('BOT_ID')
	#send .gif message
	if message['text'].startswith('/gif '):
		searchTerm = message['text'][5:]
		commands.getImage(searchTerm, bot_id)
	#send cheerUp message
	elif message['text'].startswith('/cheerup'):
		commands.cheerUp(bot_id)
	# Help message
	elif message['text'].startswith('/helpmestan'):
		details = help(commands)
		commands.helpMeStan(bot_id, details)
	return "Success"
	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
