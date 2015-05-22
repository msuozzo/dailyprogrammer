"""Manage the challenges from r/dailyprogrammer
"""
import json

from bs4 import BeautifulSoup
import requests

from dailyprogrammer.api import RedditAPIAdapter


def _retrieve_challenge_page():
    """Retrieve the challenge wiki page from reddit
    """
    print "Retrieving access token..."
    api_adapter = RedditAPIAdapter()
    token = api_adapter.get_token()
    print "Sending request..."
    headers = {'Authorization': 'bearer ' + token, 'User-Agent': 'DPClient/0.1 by msuozzo'}
    wiki_url = 'https://oauth.reddit.com/r/dailyprogrammer/wiki/challenges'
    wiki_response = requests.get(wiki_url, headers=headers)
    if wiki_response.status_code != 200:
        raise Exception('Error requesting challenges page')
    print "Parsing challenges..."
    return wiki_response.json()['data']['content_html']


def get_challenges():
    """Retrieve the challenges from reddit.

    Returns the challenges in the form:
        {challenge_difficulty:
                {challenge_title: challenge_url, ..},
         .
         .
        }
    """
    html = _retrieve_challenge_page()
    # ugly hack to load escaped html
    escaped_soup = BeautifulSoup(html)
    soup = BeautifulSoup(escaped_soup.text)
    # aggregate challenges
    difficulty_headers = ("easy", "intermediate", "hard", "extra")
    challenges = {difficulty: {} for difficulty in difficulty_headers}
    challenges_table = soup.tbody
    for ind, cell in enumerate(challenges_table.find_all('td')):
        if not cell.a:
            # Cell is empty
            continue
        link = cell.a.get('href')
        if link.startswith('/'):
            link = 'http://www.reddit.com' + link
        title = cell.a.get_text(strip=True)
        difficulty = difficulty_headers[ind % 4]
        challenges[difficulty][title] = link
    return challenges


def load_challenges(fname):
    """Load the challenges from a file.
    """
    with open(fname) as challenge_file:
        challenges = json.load(challenge_file)
    return challenges


def dump_challenges(challenges, fname):
    """Write the challenges to a file.
    """
    with open(fname, 'w') as challenge_file:
        json.dump(challenges, challenge_file, sort_keys=True, indent=4)


def update_challenges():
    """Check for updates to challenges.
    """
    pass


if __name__ == '__main__':
    print get_challenges()
