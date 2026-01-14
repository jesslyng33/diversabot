from boltapp import app

@app.message("deltatau ping")
def message_pong(message, client):
    channel_id = message['channel']

    DELTATAU_TEST_CHANNEL_ID = 'C0A9D9U5LQG'
    DELTATAU_CHANNEL_ID = 'C32NG7H2T'

    if channel_id != DELTATAU_TEST_CHANNEL_ID and channel_id != DELTATAU_CHANNEL_ID:
        return

    """ Ping. Pong. """
    client.chat_postMessage(channel=channel_id, text="pong")
