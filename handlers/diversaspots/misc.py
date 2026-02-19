from boltapp import app
from utils.utils import find_all_mentions
from utils.blocks import rule_blocks, help_blocks

@app.message("diversabot ping")
def message_pong(message, client):
    """ Ping. Pong. """
    channel_id = message['channel']
    client.chat_postMessage(channel=channel_id, text="pong")

@app.message("diversabot rules")
def post_rules(message, client):
    """Post rules"""
    channel_id = message["channel"]
    blocks = rule_blocks()
    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="Displaying rules information."
    )

@app.message("diversabot help")
def post_help(message, client):
    """Diversabot's commands"""
    channel_id = message["channel"]
    blocks = help_blocks()
    client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text="Information on Diversabot's commands."
    )


# WIP 
# @app.message("diversabot miss")
# def post_miss(message, client):
#     user_id = message["user"]
#     channel_id = message["channel"]
#     message_ts = message["ts"]
#     tagged_users: list[str] = find_all_mentions(message["text"])

#     if len(tagged_users) == 0:
#         message_text = "Please tag someone to use this command!"
#         client.chat_postMessage(
#             channel=channel_id,
#             thread_ts=message_ts,
#             text=message_text
#         )
#         return
    
#     elif len(tagged_users) > 1:
#         message_text = "Please tag only one person to use this command!"
#         client.chat_postMessage(
#             channel=channel_id,
#             thread_ts=message_ts,
#             text=message_text
#         )
#         return
    
#     tagged_user = tagged_users[0]
#     random_image_url: str

#     with Session(engine) as session:
#         # Queries a random spot from the DB that has not been flagged and has the tagged user in it.
#         random_tagged_spot = session.query(DiversaSpot) \
#                 .filter(DiversaSpot.tagged.any(tagged_user)) \
#                 .filter(DiversaSpot.flagged == False) \
#                 .order_by(sqlalchemy.func.random()) \
#                 .first() 
#         if random_tagged_spot is None:
#             random_image_url ="Too bad ... they're elusive and haven't been spotted yet :("
#         else:
#             random_image_url = random_tagged_spot.image_url

#     message_text = f"Aww ... you miss {get_name_from_user_id(tagged_user, app)}? :pleading_face::point_right::point_left:"

#     blocks = miss_blocks(message_text, random_image_url)

#     client.chat_postMessage(
#             channel=channel_id,
#             blocks=blocks,
#             text="Displaying miss information."
#         )

# @app.message("diversabot help")
# def post_help(message, client):
#     """Post help commands"""
#     channel_id = message["channel"]
#     blocks = help_blocks()
#     client.chat_postMessage(
#         channel=channel_id,
#         blocks=blocks,
#         text="Displaying help information."
#     )
