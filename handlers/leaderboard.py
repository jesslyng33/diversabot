from app import app, SEMESTER_ID, CURRENT_SEMESTER_STRING
from utils.utils import get_name_from_user_id 
from utils.blocks import leaderboard_blocks
from datetime import date
from db.diversaspots import get_ranked_leaderboard

@app.message("diversabot leaderboard")
def post_leaderboard(message, client):
    """Outputs leaderboard for the current semester."""
    channel_id = message["channel"]

    leaderboard = get_ranked_leaderboard(SEMESTER_ID)

    message_text = ""
    for entry in leaderboard:
        rank = entry["rank"]
        user_id = entry["user_id"]
        num_spots = entry["num_spots"]

        # Slack user lookup
        name = get_name_from_user_id(user_id, client)
        message_text += f"*#{rank}: {name}* with {num_spots} spots\n"

    blocks = leaderboard_blocks(date.today(), message_text, CURRENT_SEMESTER_STRING)

    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="Displaying leaderboard information."
    )

