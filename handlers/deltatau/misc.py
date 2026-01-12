from boltapp import app

@app.message("deltatau ping")
def message_pong(message, client):
    """ Ping. Pong. """
    channel_id = message['channel']
    client.chat_postMessage(channel=channel_id, text="pong")
