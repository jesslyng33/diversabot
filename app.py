# main.py
import os
from dotenv import load_dotenv
from boltapp import app

<<<<<<< HEAD
SEMESTER_ID = 'sp26'
CURRENT_SEMESTER_STRING= 'Fall 2025'
=======
SEMESTER_ID = 's26'
CURRENT_SEMESTER_STRING= 'Spring 2026'
>>>>>>> f04ce1f2ebf25fcfcee5d26455ecb2f050760fb3
# Load environment variables
load_dotenv(".env")

# ---- Import handlers so their @app decorators register ----
import handlers.diversaspots.record
import handlers.diversaspots.leaderboard
import handlers.diversaspots.stats
# import handlers.flag  # Commented out - functionality not implemented yet
import handlers.diversaspots.misc
import handlers.diversaspots.error
import handlers.deltatau.misc
import handlers.deltatau.leaderboard
import handlers.deltatau.record

# ---- Start the bot ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)