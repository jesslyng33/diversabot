# main.py
import os
from dotenv import load_dotenv
from slack_bolt import App

SEMESTER_ID = 'fs25'
CURRENT_SEMESTER_STRING= 'Fall 2025'
# Load environment variables
load_dotenv(".env")

# Initialize Slack app
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    raise_error_for_unhandled_request=True,
)

# ---- Import handlers so their @app decorators register ----
import handlers.record
import handlers.leaderboard
import handlers.stats
# import handlers.flag  # Commented out - functionality not implemented yet
import handlers.misc
import handlers.error

# ---- Start the bot ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
