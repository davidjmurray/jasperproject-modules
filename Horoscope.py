# -*- coding: utf-8-*-
'''
    Copyright 2015 David J Murray
    License: MIT
'''

# Python Library imports
import feedparser
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

WORDS = ["HOROSCOPE", ]
PRIORITY = 1


def getDailyHoroscope(zodiacSign):
    '''
       Get horoscope from astrology.com rss feed.

       Arguments:
       zodiacSign -- text of zodiac sign

       Returns:
       horoscope text -- text
    '''

    DAILY_RSS_URL = "http://www.astrology.com/horoscopes/daily-horoscope.rss"

# Cut down on extra work of parser by disabling Relative URI's Resolution
    feedparser.RESOLVE_RELATIVE_URIS = 0
    feed = feedparser.parse(DAILY_RSS_URL)

# Check for well-formed feed
    if feed.bozo == 1:
        logger.error("Not a well formed feed. Not using it.")
        text = "No horoscope found today."
        return text

# <rss><channel><item><title>[zodiac sign] Daily Horoscope for [date %b %d, %Y]</title>
# <rss><channel><item><description><p>[Text is here]</p></description>

    for item in feed['items']:
        if zodiacSign in item["title"]:

            text = item["description"]  # Horoscope in <description>
            break
    else:
        logger.info(zodiacSign + " not found in feed.")
        text = "No horoscope found today."
        return text

# The horoscope text is in the first paragraph <p></p>
    textStart = text.find("<p>") + 3
    textEnd = text.find("</p>", textStart)

    return text[textStart:textEnd]


def getZodiac(birthDate):
    '''
        Calculate the zodiac or star sign from a date.

        Arguments:
        date -- user-input, the birthdate

        Return:
        text -- zodiac sign

        The code was based on:
        https://stackoverflow.com
        /questions/3274597
        /how-would-i-determine-zodiac-astrological-star-sign-from-a-birthday-in-python
    '''

    ZODIACS = [(120, 'Capricorn'), (218, 'Aquarius'), (320, 'Pisces'),
               (420, 'Aries'), (521, 'Taurus'), (621, 'Gemini'),
               (722, 'Cancer'), (823, 'Leo'), (923, 'Virgo'),
               (1023, 'Libra'), (1122, 'Scorpio'), (1222, 'Sagittarius'),
               (1231, 'Capricorn')]

    dateNumber = birthDate.date().month * 100 + birthDate.date().day

    for zodiac in ZODIACS:
        if dateNumber < zodiac[0]:
            return zodiac[1]
    else:
        logger.info("No zodiac sign for date {birthDate}".format(birthDate=birthDate))
        return ""


def handle(text, mic, profile):
    '''
        Read todays horoscope from ycombiner.
        Responds to or handles user-input, typically speech text.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)

        Requires:
        birth_date: 01 Jan 2001
        in profile.yml
    '''

    firstName = profile["first_name"]

    try:
        birthDate = profile["birth_date"]
    except KeyError:
        logger.info("No birth_date in profile.yml.")
        mic.say("Please add your birth_date to the profile, so I can get your horoscope.")
        return

    if birthDate is None:
        logger.info("Blank birth_date in profile.yml")
        mic.say("Please check your birth_date to the profile, so I can get your horoscope.")
        return

    birthDate = datetime.strptime(birthDate, "%d %b %Y")

    zodiacSign = getZodiac(birthDate)
    mic.say("{firstName}, your zodiac or star sign is {zodiacSign}. and "
            .format(zodiacSign=zodiacSign, firstName=firstName))

    text = getDailyHoroscope(zodiacSign)
    mic.say("your horoscope states that " + text)

    return


def isValid(text):
    '''
        Returns True if the input is related to this modules.

        Arguments:
        text -- user-input, typically transcribed speech
    '''

    return bool(re.search(r'\bhoroscope\b',
                          text, re.IGNORECASE))
