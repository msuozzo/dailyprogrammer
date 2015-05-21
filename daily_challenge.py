"""Provide the user with a programming problem from r/DailyProgrammer and a
language in which the problem should be solved.
"""
import argparse
import json
from itertools import chain
from random import choice
from datetime import datetime
import os

from challenges import get_challenges


def load_config(fname="config.json"):
    """Load a json config file.
    """
    with open(fname) as config_file:
        return json.load(config_file)


def load_challenge_log(fname='.past_challenges.json'):
    """Load a json challenge log.
    """
    try:
        os.stat(fname)
    except OSError:
        with open(fname, 'w') as log_file:
            json.dump([], log_file, sort_keys=True, indent=4)
    with open(fname) as log_file:
        return json.load(log_file)


def add_to_challenge_log(title, link, fname='.past_challenges.json'):
    """Add an entry to the challenge log.
    """
    log = load_challenge_log()
    log.append({
        'title': title,
        'link': link,
        'time': datetime.now().isoformat()
    })
    with open(fname, 'w') as log_file:
        json.dump(log, log_file, sort_keys=True, indent=4)


def filter_repeats(challenges):
    """Remove the challenges appearing in the challenge log to avoid repeating a challenge.
    """
    log = load_challenge_log()
    used_links = [entry['link'] for entry in log]
    return [(title, link) for title, link in challenges if link not in used_links]


def do_challenge():
    """Provide a random challenge from r/DailyProgrammer to the user along with
    a language in which the language should be completed.
    """
    config = load_config("./config.json")
    languages = config['languages']
    no_repeat_challenges = config['no_repeat_challenge']

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
    challenges = get_challenges()
    valid_challenge_items = (challenge_dict.items()
                                for diff, challenge_dict in challenges.iteritems()
                                if diff in valid_difficulties)
    valid_challenges = list(chain.from_iterable(valid_challenge_items))
    if no_repeat_challenges:
        valid_challenges = filter_repeats(valid_challenges)

    title, link = choice(valid_challenges)
    language = choice(languages)
    print ("  %s  " % title).center(120, '=')
    print "Using %s, complete the challenge found at:\n\t %s" % (language, link)
    add_to_challenge_log(title, link)


if __name__ == "__main__":
    do_challenge()
