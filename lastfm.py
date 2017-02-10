"""Script to get the latest music from lastfm."""

import json
import requests
import time
from keys import *


def get_artists_from_tracks(tracks):
    """Get the artists and their frequency from recent songs."""
    artist_dict = {}
    for track in tracks:
        print("artist: %s \t\t song: %s" % (
            track["artist"]["#text"], track["name"]))


def get_tracks_since_last_time(last_time=None):
    """Get the tracks played since the specified time."""
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


def get_most_recent_track_time(tracks):
    """Get the time of the most recently scrobbled track."""
    if tracks[0].get("date") is not None:
        most_recent_time = tracks[0]["date"]["uts"]
    else:
        most_recent_time = time.time()

    return(most_recent_time)
