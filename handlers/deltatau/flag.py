from boltapp import app
from utils.utils import random_disappointed_greeting, random_excited_greeting
from db.deltatau import get_deltatau_by_ts, flag_deltatau, unflag_deltatau
from datetime import datetime, timezone


@app.message("deltatau flag")
def flag_challenge(message, client, logger):
    flagger = message['user']
    channel_id = message["channel"]

    DELTATAU_TEST_CHANNEL_ID = 'C0A9D9U5LQG'
    DELTATAU_CHANNEL_ID = 'C32NG7H2T'

    if channel_id != DELTATAU_TEST_CHANNEL_ID and channel_id != DELTATAU_CHANNEL_ID:
        return

    if 'thread_ts' not in message:
        reply = (
            f"{random_disappointed_greeting()} <@{flagger}>, to flag a challenge, "
            "you have to reply 'deltatau flag' in the thread of the challenge you'd like to flag."
        )
        client.chat_postMessage(channel=channel_id, thread_ts=message['ts'], text=reply)
        return

    thread_ts = message['thread_ts']
    ts = datetime.fromtimestamp(float(thread_ts), tz=timezone.utc).isoformat()

    entry = get_deltatau_by_ts(ts)
    if entry is None:
        reply = f"{random_disappointed_greeting()} <@{flagger}>, this is not a valid DeltaTau challenge to flag!"
        client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)
        return

    if entry.get('flagged'):
        reply = f"{random_disappointed_greeting()} <@{flagger}>, this challenge has already been flagged!"
        client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)
        return

    flag_deltatau(ts)
    reply = (
        f"{random_disappointed_greeting()} <@{entry['new_mem']}>, this challenge has been flagged by "
        f"<@{flagger}>. If you believe this is a mistake, please reach out to a board member."
    )
    client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)


@app.message("deltatau unflag")
def unflag_challenge(message, client, logger):
    flagger = message['user']
    channel_id = message["channel"]

    DELTATAU_TEST_CHANNEL_ID = 'C0A9D9U5LQG'
    DELTATAU_CHANNEL_ID = 'C32NG7H2T'

    if channel_id != DELTATAU_TEST_CHANNEL_ID and channel_id != DELTATAU_CHANNEL_ID:
        return

    if 'thread_ts' not in message:
        reply = (
            f"{random_disappointed_greeting()} <@{flagger}>, to unflag a challenge, "
            "you have to reply 'deltatau unflag' in the thread of the challenge you'd like to unflag."
        )
        client.chat_postMessage(channel=channel_id, thread_ts=message['ts'], text=reply)
        return

    thread_ts = message['thread_ts']
    ts = datetime.fromtimestamp(float(thread_ts), tz=timezone.utc).isoformat()

    entry = get_deltatau_by_ts(ts)
    if entry is None:
        reply = f"{random_disappointed_greeting()} <@{flagger}>, this is not a valid DeltaTau challenge to unflag!"
        client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)
        return

    if not entry.get('flagged'):
        reply = f"{random_disappointed_greeting()} <@{flagger}>, this challenge has not been flagged!"
        client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)
        return

    unflag_deltatau(ts)
    reply = (
        f"{random_excited_greeting()} <@{entry['new_mem']}>, this challenge has been unflagged by "
        f"<@{flagger}>. Your points have been restored!"
    )
    client.chat_postMessage(channel=channel_id, thread_ts=thread_ts, text=reply)
