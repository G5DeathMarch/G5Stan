import os
import commands
from flask import Flask, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    # receive JSON from groupme request containing message information
    r = request.get_json(force=True)
    # send .gif message
    message = r['text']
    print("request: {}".format(r))
    if message.startswith('/gif '):
        search_term = message[5:]
        commands.get_image(search_term)
    # send cheerUp message
    elif message.startswith('/cheerup'):
        commands.cheer_up('resources/compliments.txt')
    # Help message
    elif message.startswith('/helpmestan'):
        commands.help_me_stan('../README.md')
    # Eye-bleach
    elif message.startswith('/eyebleach'):
        commands.eye_bleach()
    # Crell memes
    elif message.startswith('/crell'):
        commands.crell_pic('resources/image_links.txt')
    # @group
    elif message.startswith('@group '):
        group_message = message[7:]
        group_id = r['group_id']
        commands.at_group(group_message, group_id)
    return "Success"


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
