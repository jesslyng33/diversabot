# # main.py
# import os
# from dotenv import load_dotenv
# from boltapp import app

# SEMESTER_ID = 's26'
# CURRENT_SEMESTER_STRING= 'Spring 2026'
# # Load environment variables
# load_dotenv(".env")

# # ---- Import handlers so their @app decorators register ----
# import handlers.diversaspots.record
# import handlers.diversaspots.leaderboard
# import handlers.diversaspots.stats
# # import handlers.flag  # Commented out - functionality not implemented yet
# import handlers.diversaspots.misc
# import handlers.diversaspots.error
# import handlers.deltatau.misc
# import handlers.deltatau.leaderboard
# import handlers.deltatau.record

# # ---- Start the bot ----
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 3000))
#     app.start(port=port)

from flask import Flask, request
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os

bolt_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

flask_app = Flask(__name__)
handler = SlackRequestHandler(bolt_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)
