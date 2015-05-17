"""Manage the challenges from r/dailyprogrammer
"""
from bs4 import BeautifulSoup
import requests

from api import RedditAPIAdapter


def get_challenges():
    """Retrieve the challenges from reddit
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
    html = wiki_response.json()['data']['content_html']
    # ugly hack to load escaped html
    escaped_soup = BeautifulSoup(html)
    soup = BeautifulSoup(escaped_soup.text)
    # table of challenges
    # format: [easy, intermediate, hard, extra]
    challenges = [[], [], [], []]
    challenges_table = soup.tbody
    for ind, cell in enumerate(challenges_table.find_all('td')):
        if not cell.a:
            # Cell is empty
            continue
        link = cell.a.get('href')
        if link.startswith('/'):
            link = 'http://www.reddit.com' + link
        title = cell.a.get_text(strip=True)
        challenge = (title, link)
        challenges[ind % 4].append(challenge)
    return challenges


def update_challenges():
    """Check for updates to challenges.
    """
    pass


if __name__ == '__main__':
    print get_challenges()
