import os
import inspect
import commands
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
	#receive JSON from groupme request containing message information		
 	r = request.get_json(force=True)
	#send .gif message
	message = r['text']
	if message.startswith('/gif '):
		searchTerm = message[5:]
		commands.getImage(searchTerm)
	#send cheerUp message
	elif message.startswith('/cheerup'):
		commands.cheerUp()
	# Help message
	elif message.startswith('/helpmestan'):
		commands.helpMeStan()
	# Eyebleach
	elif message.startswith('/eyebleach'):
		commands.eyeBleach()
	# Reminder
	elif message.startswith('/remindme '):
		# We expect the text to be in this format
		# 'in [time] to [message]'
		textContent = message[10:]
		user_id = r['user_id']
		username = r['name']
		commands.remindme(user_id, username, textContent)		

	return "Success"
	
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)