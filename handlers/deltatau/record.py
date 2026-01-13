from app import SEMESTER_ID
from boltapp import app
from utils.utils import find_all_mentions, random_disappointed_greeting, random_excited_greeting
from db.diversaspots import insert_deltatau, get_num_points_for_user_id
from datetime import datetime, timezone

@app.event({
    "type" : "message",
    "subtype" : "file_share"
})
def record_challenge(message, client, logger):
    """ Records a New Mem Challenge. """
    channel_id = message['channel']

    # only process in deltatau or deltatau-test
    DELTATAU_TEST_CHANNEL_ID = 'C0A9D9U5LQG'
    DELTATAU_CHANNEL_ID = 'C32NG7H2T'

    if channel_id != DELTATAU_TEST_CHANNEL_ID and channel_id != DELTATAU_CHANNEL_ID:
        return

    user = message["user"]
    message_ts = message["ts"]
    ts = datetime.fromtimestamp(float(message["ts"]), tz=timezone.utc)
    channel_id = message["channel"]
    text: str = message["text"]

    # checking for point value
    try:
        points = int(text.strip())
    except ValueError:
        logger.info(f"User {user} did not list just the point value in their message.")
        reply = f"{random_disappointed_greeting()} <@{user}>, this challenge won't count " + \
            "because your message had something other than just point value! Delete and try again."
    else:
        if (filetype:= message['files'][0]['filetype']) != 'jpg' and filetype != 'png' and filetype != 'heic':
            logger.info(f'User {user} did not attach a JPG, HEIC, or a PNG file.')
            reply = f"{random_disappointed_greeting()} <@{user}>, This challenge doesn't count " + \
                "because you didn't attach a JPG, HEIC, or a PNG file! Delete and try again."

        else:
            logger.info(f"Recording New Mem Challenge from user {user} at timestamp {ts}.")
            insert_deltatau(ts=ts.isoformat(),
                                     new_mem = user,
                                     points = points,
                                     semester = SEMESTER_ID,
                                     flagged=False)
            reply = f"{random_excited_greeting()} <@{user}> challenge recorded with {points} points!"
    
    client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=reply)
    
