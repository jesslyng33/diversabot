from app import SEMESTER_ID
from boltapp import app
from utils.utils import find_all_mentions, random_disappointed_greeting, random_excited_greeting
from db.deltatau import insert_deltatau, get_num_points_for_user_id
from db.diversaspots import insert_diversaspot, get_num_spots_for_user_id
from datetime import datetime, timezone

@app.event({
    "type": "message",
    "subtype": "file_share"
})
def record(message, client, logger):
    """
    RECORDS NEW MEM (DELTATAU) CHALLENGE OR DIVERSASPOT

    1)
    Records a New Mem (DeltaTau) Challenge entry.
    Rule: message text must be JUST a whole number (like "7") AND an image must be attached.
    That number is added to the user's total points (via inserting a row with that points value).

    2)
    Records a DiversaSpot.
    """
    
    # Basic info from Slack
    channel_id = message.get("channel")

    # only process in deltatau or deltatau-test
    DELTATAU_TEST_CHANNEL_ID = 'C0A9D9U5LQG'
    DELTATAU_CHANNEL_ID = 'C32NG7H2T'
    DIVERSASPOT_CHANNEL_ID = 'CT88GU87Q'
    DIVERSASPOT_TEST_CHANNEL_ID = 'C09GFABA58C'

    if channel_id != DELTATAU_TEST_CHANNEL_ID and channel_id != DELTATAU_CHANNEL_ID and channel_id != DIVERSASPOT_CHANNEL_ID and channel_id != DIVERSASPOT_TEST_CHANNEL_ID:
        return
      
    if channel_id == DELTATAU_TEST_CHANNEL_ID or channel_id == DELTATAU_CHANNEL_ID:
      user = message.get("user")
      message_ts = message.get("ts")

      # Convert Slack timestamp string -> datetime
      ts = datetime.fromtimestamp(float(message_ts), tz=timezone.utc)

      # Text the user typed with the upload
      text = (message.get("text") or "").strip()

      # --- 1) Check that the text is a plain integer like "7" ---
      # Slack always gives you text as a STRING, never an int.
      # So we must validate the string and then convert it.
      if not text.isdigit():
          logger.info(f"User {user} did not send a plain integer. text={text!r}")
          reply = (
              f"{random_disappointed_greeting()} <@{user}>, this challenge won't count because your message "
              f"must be *only a number* (example: `7`). Delete and try again."
          )
          client.chat_postMessage(channel=channel_id, thread_ts=message_ts, text=reply)
          return

      points = int(text)

      # Optional: block 0-point submissions
      if points <= 0:
          reply = (
              f"{random_disappointed_greeting()} <@{user}>, please use a positive number (example: `7`). "
              f"Delete and try again."
          )
          client.chat_postMessage(channel=channel_id, thread_ts=message_ts, text=reply)
          return

      # --- 2) Check that a file exists and is an allowed image type ---
      files = message.get("files") or []
      if len(files) == 0:
          logger.info(f"User {user} did not attach a file.")
          reply = (
              f"{random_disappointed_greeting()} <@{user}>, this challenge won't count because you didn't attach an image. "
              f"Delete and try again."
          )
          client.chat_postMessage(channel=channel_id, thread_ts=message_ts, text=reply)
          return

      filetype = (files[0].get("filetype") or "").lower()
      if filetype not in ("jpg", "jpeg", "png", "heic"):
          logger.info(f"User {user} uploaded unsupported filetype: {filetype}")
          reply = (
              f"{random_disappointed_greeting()} <@{user}>, this challenge doesn't count because you didn't attach a "
              f"JPG/JPEG/PNG/HEIC image. Delete and try again."
          )
          client.chat_postMessage(channel=channel_id, thread_ts=message_ts, text=reply)
          return

      # --- 3) Insert into DB (this is how you record the points) ---
      logger.info(f"Recording DeltaTau entry from user {user} at {ts.isoformat()} with points={points}")
      insert_deltatau(
          ts=ts.isoformat(),
          new_mem=user,
          points=points,
          semester=SEMESTER_ID,
          flagged=False
      )

      # --- 4) Get updated total and reply ---
      total_points = get_num_points_for_user_id(user, SEMESTER_ID)
      reply = (
          f"{random_excited_greeting()} <@{user}>, recorded *{points}* points! "
          f"You now have *{total_points}* total points."
      )

      client.chat_postMessage(
          channel=channel_id,
          thread_ts=message_ts,
          text=reply
      )
    elif channel_id == DIVERSASPOT_CHANNEL_ID or channel_id == DIVERSASPOT_TEST_CHANNEL_ID:
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