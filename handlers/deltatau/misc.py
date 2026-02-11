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


@app.message("deltatau rules")
def post_deltatau_rules(message, client):
    """Post DeltaTau rules"""

    channel_id = message["channel"]

    rules_text = (
        "*DeltaTau Official Rules!!*\n\n"
        "Please follow these rules so that New Mem Challenges goes smoothly!\n\n"
        
        "*Rule 1:* Every DeltaTau submission must include an image AND a number in the message text. "
        "The number will be added to your total points.\n\n"

        "*Rule 2:* The number submitted must be a whole number. "
        "Decimals, negative numbers, or non-numeric text will not count.\n\n"

        "*Rule 3:* Each image submission counts as one entry. "
        "If multiple numbers are included, only the first valid number will be used.\n\n"

        "*Rule 4:* Submissions must be original and posted in this designated DeltaTau channel. "
        "Posts in other channels will not count.\n\n"

        "*Rule 5:* The leaderboard is determined by total accumulated points at the end of New Mem Challenges. "
    )

    client.chat_postMessage(
        channel=channel_id,
        text=rules_text
    )
