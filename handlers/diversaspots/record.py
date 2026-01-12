from app import SEMESTER_ID
from boltapp import app
from utils.utils import find_all_mentions, random_disappointed_greeting, random_excited_greeting
from db.diversaspots import insert_diversaspot, get_num_spots_for_user_id
from datetime import datetime, timezone

@app.event({
    "type" : "message",
    "subtype" : "file_share"
})
def record_spot(message, client, logger):
    """ Records a DiversaSpot. """
    user = message["user"]
    message_ts = message["ts"]
    ts = datetime.fromtimestamp(float(message["ts"]), tz=timezone.utc)
    channel_id = message["channel"]
    text: str = message["text"]
    tagged_users: list[str] = find_all_mentions(text)
    
    if len(tagged_users) == 0:
        logger.info(f"User {user} did not tag anyone in their DiversaSpot.")
        reply = f"{random_disappointed_greeting()} <@{user}>, this DiversaSpot doesn't count " + \
                "because you didn't mention anyone! Delete and try again."
        
    elif (filetype := message['files'][0]['filetype']) != 'jpg' and filetype != 'png' and filetype != 'heic':
        logger.info(f"User {user} did not attach a JPG, HEIC, or a PNG file.")
        reply = f"{random_disappointed_greeting()} <@{user}>, This DiversaSpot doesn't count because you " + \
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
