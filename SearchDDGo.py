# -*- coding: utf-8-*-
'''
    Copyright 2015 David J Murray
    License: MIT

'''

# Python Library imports
import logging
import random
import re

# Jasper utils
# from client import jasperpath
# from client.app_utils import isPositive
# from client.app_utils import isNegative

logger = logging.getLogger(__name__)

# Other Python Library imports
# requires - sudo pip install duckduckgo
try:
    import duckduckgo
except:
    logger.error("Cannot import duckduckgo. Please 'sudo pip install duckduckgo'")
    raise

WORDS = ["SEARCH", "DUCK", "DUCKDUCKGO", "DDG"]
PRIORITY = 10


def handle(text, mic, profile):
    '''
        Responds to or handles user-input, for searching
        Duck Duck Go. Uses the abstract.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    '''
    # Randomly selected prompt phrase.
    messages = ["What would you like to know?",
                "What are you looking for?",
                "What do you want to Duck Duck Go?"]

    message = random.choice(messages)
    mic.say(message)

# Ask for search terms
    question(mic.activeListen(), mic, profile)

    return


def question(text, mic, profile):
    '''
        Ask for search terms.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- mic function
        profile
    '''

    mic.say("Searching for {SearchTerms}.".format(SearchTerms=text))

    response = duckduckgo.query(text)

# Abstract provides the DDG instant answer
    answerText = response.abstract.text

    if len(answerText) > 0:

        answerSource = response.abstract.source
        mic.say("From {answerSource}: {answerText}"
                .format(answerSource=answerSource, answerText=answerText))
    else:
        mic.say("Sorry, Could you be more specific?")

    return


def isValid(text):
    '''
        Returns True if the input is related to this modules.

        Arguments:
        text -- user-input, typically transcribed speech
    '''

    return bool(re.search(r'\bsearch|duck|duckduckgo|DDG|duck duck go\b',
                          text, re.IGNORECASE))
