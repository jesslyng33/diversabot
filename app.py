# main.py
import os
from dotenv import load_dotenv
from boltapp import app

SEMESTER_ID = 's26'
CURRENT_SEMESTER_STRING= 'Spring 2026'
# Load environment variables
load_dotenv(".env")

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