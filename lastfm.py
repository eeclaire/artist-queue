"""Script to get the latest music from lastfm."""

import json
import requests

from keys import *


def get_tracks_since_last_time(last_time=None):
    """Query lastfm for the tracks played since the specified time."""
    user = 'eeclaire'
    base_url = 'http://ws.audioscrobbler.com/2.0/'
    method = '?method=user.getrecenttracks'

    options = '&user=%s&from=%s&api_key=%s&limit=200&format=json' % (
        user, last_time, key)

    url = base_url + method + options
    header = {'user-agent': 'eeclaire/artistq'}

    r = requests.get(url, headers=header)

    parsed = json.loads(r.content.decode("utf-8"))
    tracks = parsed["recenttracks"]["track"]

    return(tracks)
