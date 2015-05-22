#!/usr/bin/python
"""Provide the user with a programming problem from r/DailyProgrammer and a
language in which the problem should be solved.
"""
import argparse
from itertools import chain
from random import choice
from datetime import datetime

from dailyprogrammer.challenges import get_challenges
from dailyprogrammer.utils import JSONFileManager


def _filter_repeats(challenges, log):
    """Remove the challenges appearing in the challenge log to avoid repeating a challenge.
    """
    used_links = [entry['link'] for entry in log]
    return [(title, link) for title, link in challenges if link not in used_links]


def _get_valid_challenges(valid_difficulties):
    """Retrieve and filter challenges by difficulty

    valid_difficulties - an iterable of strings representing acceptable difficulty levels
    """
    challenges = get_challenges()
    valid_challenge_items = (challenge_dict.items()
                                for diff, challenge_dict in challenges.iteritems()
                                if diff in valid_difficulties)
    valid_challenges = list(chain.from_iterable(valid_challenge_items))
    return valid_challenges


def do_challenge():
    """Provide a random challenge from r/DailyProgrammer to the user along with
    a language in which the language should be completed.
    """
    config = JSONFileManager('config.json')
    languages = config.obj['languages']
    no_repeat_challenges = config.obj['no_repeat_challenge']

    parser = argparse.ArgumentParser()
    parser.add_argument('--difficulty', '-d',
                        choices=['easy', 'med', 'hard'], default='hard',
                        dest='difficulty')
    args = parser.parse_args()

    if args.difficulty == 'easy':
        valid_difficulties = ("easy")
    elif args.difficulty == 'med':
        valid_difficulties = ("easy", "intermediate")
    elif args.difficulty == 'hard':
        valid_difficulties = ("easy", "intermediate", "hard", "extra")

    valid_challenges = _get_valid_challenges(valid_difficulties)
    challenge_log = JSONFileManager('.challenge_log.json', default=[])
    if no_repeat_challenges:
        valid_challenges = _filter_repeats(valid_challenges, challenge_log.obj)

    title, link = choice(valid_challenges)
    language = choice(languages)
    print ("  %s  " % title).center(120, '=')
    print "Using %s, complete the challenge found at:\n\t %s" % (language, link)

    # add to challenge log
    challenge_log.obj.append({
        'title': title,
        'link': link,
        'time': datetime.now().isoformat()
    })
    challenge_log.dump()


if __name__ == "__main__":
    do_challenge()
