"""
Miscellaneous utility functions.
"""

import random
import re
from typing import Iterator
from slack_bolt import App


def find_all_mentions(msg: str) -> list[str]:
    """Returns all user_ids mentioned in msg"""
    member_ids = re.findall(r'<@([\w]+)>', msg, re.MULTILINE)
    return member_ids

def get_name_from_user_id(user_id : str, client):
    """ Gets name from user id."""
    return client.users_info(user=user_id)['user']['real_name']


def random_excited_greeting() -> str:
    """Returns a random excited greeting"""
    greetings = [
        "Hey",
        "Hi",
        "What's schlaying",
        "What's poppin'",
        "Greetings",
        "DiversaHi",
        "Attention",
        "DiversaSLAY",
        "Howdy"
    ]
    return random.choice(greetings)

def random_disappointed_greeting() -> str:
    """Returns a random disappointed greeting"""
    greetings = [
        "Oh no",
        "Whoops",
        "Stupid",
    ]
    return random.choice(greetings)
