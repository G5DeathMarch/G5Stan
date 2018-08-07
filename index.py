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
    elif message.startswith('/crell'):
        commands.crellPic()
    return "Success"
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
