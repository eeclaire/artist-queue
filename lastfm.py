"""Script to get the latest music from lastfm."""

import json
import requests
import time
import os.path
from keys import *


# TODO: Add to a local artists storage that is cleaned up once a week
def save_tracks_to_daily(tracks):
    """Get the artists and their frequency from recent songs."""
    track_list = []
    for track in tracks:
        track_artist = track["artist"]["#text"]
        track_name = track["name"]
        track_list.append((track_artist, track_name))

    daily_tracks_filename = 'daily.csv'

    # Add these tracks to the daily track list
    if os.path.isfile(daily_tracks_filename):
        with open(daily_tracks_filename, 'a+') as fileout:
            for track in track_list:
                fileout.write('{"%s": "%s"}\n' % (track[0], track[1]))

    else:
        with open(daily_tracks_filename, 'w') as fileout:
            for track in track_list:
                fileout.write('{"%s": "%s"}\n' % (track[0], track[1]))


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
