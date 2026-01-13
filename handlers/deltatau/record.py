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
    """ Records a New Mem Challenge. """
    user = message["user"]
    message_ts = message["ts"]
    ts = datetime.fromtimestamp(float(message["ts"]), tz=timezone.utc)
    channel_id = message["channel"]
    text: str = message["text"]
    tagged_users: list[str] = find_all_mentions(text)