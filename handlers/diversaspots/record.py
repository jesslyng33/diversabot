from app import SEMESTER_ID
from boltapp import app
from utils.utils import find_all_mentions, random_disappointed_greeting, random_excited_greeting
from db.diversaspots import insert_diversaspot, get_num_spots_for_user_id
from datetime import datetime, timezone

@app.event("message")
def record_spot(message, client, logger):
    """ Records a DiversaSpot. """
    # only handle file_share messages
    # if message.get('subtype') != 'file_share':
    #     return

    # logger.info(f"[DIVERSASPOT] record_spot handler triggered for channel {message.get('channel')}")

    channel_id = message.get('channel')
    logger.info(f"[DIVERSASPOT] Step 1: got channel {channel_id}")

    # after the channel check...
    logger.info(f"[DIVERSASPOT] Step 2: passed channel check")

    user = message.get('user')
    message_ts = message.get('ts')
    logger.info(f"[DIVERSASPOT] Step 3: user={user}, ts={message_ts}")

    text: str = message.get("text", "")
    tagged_users: list[str] = find_all_mentions(text)
    logger.info(f"[DIVERSASPOT] Step 4: tagged_users={tagged_users}")

    files = message.get('files', [])
    logger.info(f"[DIVERSASPOT] Step 5: files={files}")

    # only process in diversaspot or diversaspot-test
    DIVERSASPOT_CHANNEL_ID = 'CT88GU87Q'
    DIVERSASPOT_TEST_CHANNEL_ID = 'C09GFABA58C'

    if channel_id != DIVERSASPOT_CHANNEL_ID and channel_id != DIVERSASPOT_TEST_CHANNEL_ID:
        logger.info(f"[DIVERSASPOT] Ignoring message from channel {channel_id}")
        return
    
    logger.info(f"[DIVERSASPOT] Processing message from channel {channel_id}")
        
    user = message.get("user")
    message_ts = message.get("ts")

    ts_raw = message.get("ts")
    ts = (
        datetime.fromtimestamp(float(ts_raw), tz=timezone.utc)
        if ts_raw is not None
        else None
    )

    text: str = message.get("text", "")
    tagged_users: list[str] = find_all_mentions(text)

    files = message.get('files', [])

    if len(tagged_users) == 0:
        logger.info(f"User {user} did not tag anyone in their DiversaSpot.")
        reply = f"{random_disappointed_greeting()} <@{user}>, this DiversaSpot doesn't count " + \
                "because you didn't mention anyone! Delete and try again."

    elif not files:
        logger.info(f"User {user} did not attach any file.")
        reply = f"{random_disappointed_greeting()} <@{user}>, this DiversaSpot doesn't count because you " + \
                "didn't attach a JPG, HEIC, or a PNG file! Delete and try again."

    elif files[0].get('filetype', '') not in ['jpg', 'png', 'heic']:
        logger.info(f"User {user} did not attach a JPG, HEIC, or a PNG file.")
        reply = f"{random_disappointed_greeting()} <@{user}>, this DiversaSpot doesn't count because you " + \
                "didn't attach a JPG, HEIC, or a PNG file! Delete and try again."

    else:
        logger.info(f"Recording DiversaSpot from user {user} at timestamp {ts}.")
        insert_diversaspot(timestamp=ts.isoformat(),
                        spotter=user,
                        tagged=tagged_users,
                        semester=SEMESTER_ID,
                        flagged=False)

    # Sending confirmation message.
    num_spots = get_num_spots_for_user_id(user, SEMESTER_ID)
    reply = f"{random_excited_greeting()} <@{user}>, you now have {num_spots} DiversaSpots!"
    
    # if len(tagged_users) == 0:
    #     logger.info(f"User {user} did not tag anyone in their DiversaSpot.")
    #     reply = f"{random_disappointed_greeting()} <@{user}>, this DiversaSpot doesn't count " + \
    #             "because you didn't mention anyone! Delete and try again."
        
    # elif (filetype := message['files'][0]['filetype']) != 'jpg' and filetype != 'png' and filetype != 'heic':
    #     logger.info(f"User {user} did not attach a JPG, HEIC, or a PNG file.")
    #     reply = f"{random_disappointed_greeting()} <@{user}>, This DiversaSpot doesn't count because you " + \
    #             "didn't attach a JPG, HEIC, or a PNG file! Delete and try again."
    # # add another elif here to redirect to deltatau bot if attached is
    # # an integer and an image  
    # else:
    #     logger.info(f"Recording DiversaSpot from user {user} at timestamp {ts}.")   
    #     insert_diversaspot(timestamp=ts.isoformat(), 
    #                        spotter=user, 
    #                        tagged=tagged_users, 
    #                        semester=SEMESTER_ID, 
    #                        flagged=False)

    #     # Sending confirmation message.
    #     num_spots = get_num_spots_for_user_id(user, SEMESTER_ID)
    #     reply = f"{random_excited_greeting()} <@{user}>, you now have {num_spots} DiversaSpots!"

    client.chat_postMessage(
        channel=channel_id,
        thread_ts=message_ts,
        text=reply
    )


# WIP for future diversabot miss
# Creating new image file name for S3 bucket.
# Format: <user_id>_<timestamp>.<filetype>
# image_url = message['files'][0]['url_private']
# path = urlparse(image_url).path
# image_ext = os.path.splitext(path)[1] # e.g .jpg
# new_s3_file_name = f"{S3_BUCKET_FOLDER_NAME}/{user}_{message_ts}{image_ext}"

# Extracting image data from Slack URL and uploading it into S3 bucket.
# resp = requests.get(image_url, headers={"Authorization" : f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"})
# s3_client.put_object(Bucket='diversaspots', Body=resp.content, Key=new_s3_file_name)
# s3_image_url = S3_BUCKET_URL + new_s3_file_name

# Inserting DiversaSpot into DB. 
