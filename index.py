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
    print("request: {}".format(r))
    if message.startswith('/gif '):
        searchTerm = message[5:]
        commands.getImage(searchTerm)
    # send cheerUp message
    elif message.startswith('/cheerup'):
        commands.cheerUp()
    # Help message
    elif message.startswith('/helpmestan'):
        commands.helpMeStan()
    # Eyebleach
    elif message.startswith('/eyebleach'):
        commands.eyeBleach()
    # Crell memes
    elif message.startswith('/crell'):
        commands.crellPic()
    # @group
    elif message.startswith('@group '):
        group_message = message[6:]
        group_id = r['group_id']
        commands.atGroup(group_message, group_id)

    return "Success"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
