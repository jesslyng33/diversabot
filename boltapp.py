import os
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv(".env")

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)