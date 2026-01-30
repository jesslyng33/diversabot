# from app import app 
# from utils.utils import random_disappointed_greeting, DiversaSpot

# @app.message("diversabot flag")
# def flag_spot(message, client, logger):
#     flagger = message['user']
#     channel_id = message["channel"]
#     reply: str

#     if 'thread_ts' not in message:
#         logger.info(f"User {flagger} attempted to flag a spot without replying in a thread.")
#         reply = f"{random_disappointed_greeting()} <@{flagger}>, to flag a spot, " + \
#             "you have to reply 'diversaspot flag' in the thread of the spot that you'd like to flag."
#         message_ts = message['ts']

#     # User is flagging a thread
#     else:
#         message_ts = message['thread_ts'] # Should be threaded under the original DiversaSpot.

#         with Session(engine) as session:
#             try:
#                 diversaspot = session.query(DiversaSpot).filter_by(timestamp=message_ts).one()
#             except NoResultFound:
#                 logger.info(*f"User {flagger} attempted to flag a spot that doesn't exist.")
#                 reply = f"{random_disappointed_greeting()} <@{flagger}>, this is not a valid DiversaSpot to flag!"
#             except MultipleResultsFound:
#                 logger.error(f"Multiple DiversaSpots found with timestamp {message_ts}.")
#                 reply = "Critical error occured. Muiltiple DiversaSpots found with the same timestamp. " + \
#                         "Please contact the DiversaBot team."

#             if diversaspot.flagged == True:
#                 logger.info(f"User {flagger} attempted to flag a spot that was already flagged.")
#                 reply = f"{random_disappointed_greeting()} <@{flagger}>, this DiversaSpot has already been flagged!"
#             else:
#                 # Valid diversaspot to flag. Commit the operation.
#                 diversaspot.flagged = True
#                 session.commit()

#             reply = f"{random_disappointed_greeting()} <@{diversaspot.spotter}>, this spot has been flagged by <@{flagger}> as they believe it is in violation of the official DiversaSpotting rules and regulations. If you would like to review the official DiversaSpotting rules and regulations, you can type 'diversabot rules'. If you would like to dispute this flag, please @ Thomas Wang or Clara Tu in this thread with a relevant explanation."


#     client.chat_postMessage(
#         channel=channel_id,
#         thread_ts=message_ts,
#         text=reply
#     )


# @app.message("diversabot unflag")
# def unflag_spot(message, client, logger):
#     flagger = message['user']
#     channel_id = message["channel"]
#     reply: str

#     if 'thread_ts' not in message:
#         logger.info(f"User {flagger} attempted to unflag a spot without replying in a thread.")
#         reply = f"{random_disappointed_greeting()} <@{flagger}>, to unflag a spot, " + \
#             "you have to reply 'diversaspot unflag' in the thread of the spot that you'd like to unflag."
#         message_ts = message['ts']

#     # User is unflagging a thread
#     else:
#         message_ts = message['thread_ts'] # Should be threaded under the original DiversaSpot.

#         with Session(engine) as session:
#             try:
#                 diversaspot = session.query(DiversaSpot).filter_by(timestamp=message_ts).one()
#             except NoResultFound:
#                 logger.info(*f"User {flagger} attempted to unflag a spot that doesn't exist.")
#                 reply = f"{random_disappointed_greeting()} <@{flagger}>, this is not a valid DiversaSpot to unflag!"
#             except MultipleResultsFound:
#                 logger.error(f"Multiple DiversaSpots found with timestamp {message_ts}.")
#                 reply = "Critical error occured. Muiltiple DiversaSpots found with the same timestamp. " + \
#                         "Please contact the DiversaBot team."

#             if diversaspot.flagged == False:
#                 logger.info(f"User {flagger} attempted to unflag a spot that's not flagged.")
#                 reply = f"{random_disappointed_greeting()} <@{flagger}>, this DiversaSpot has not been flagged!"
#             else:
#                 # Valid diversaspot to unflag. Commit the operation.
#                 diversaspot.flagged = False
#                 session.commit()

#             reply = f"{random_disappointed_greeting()} <@{diversaspot.spotter}>, this spot has been unflagged by <@{flagger}>."


#     client.chat_postMessage(
#         channel=channel_id,
#         thread_ts=message_ts,
#         text=reply
#     )
