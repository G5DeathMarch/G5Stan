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
    print(r)
    if message.startswith('/gif '):
        print("/gif called with: {}".format(message[5:]))
        searchTerm = message[5:]
        commands.getImage(searchTerm)
    #send cheerUp message
    elif message.startswith('/cheerup'):
        print("/cheerup called")
        commands.cheerUp()
    # Help message
    elif message.startswith('/helpmestan'):
        print("/helpmestan called")
        commands.helpMeStan()
    # Eyebleach
    elif message.startswith('/eyebleach'):
        print("/eyebleach called")
        commands.eyeBleach()
    elif message.startswith('/crell'):
        print("/crell called")
        commands.crellPic()
    return "Success"
    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
