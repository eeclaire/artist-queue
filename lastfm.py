"""Script to get the latest music from lastfm."""

import json
import requests
import time
import os.path
import psycopg2
from keys import *


def save_tracks_to_daily(tracks):
    """Get the artists and their frequency from recent songs."""

    # Connect to existing postgres db
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")

    # Set up cursor to perform db operations
    cur = conn.cursor()

    # Check that artist exists in confirmed_artists table
    track_list = []
    for track in tracks:

        track_artist = track["artist"]["#text"]
        track_name = track["name"]

        cur.execute("select artist from confirmed_artists where artist like '%s'" % (track_name.replace("'", "''")))
        if cur.fetchone() is not None:
            track_artist = track['name']
            track_name = track['artist']['#text']

        cur.execute("insert into scrobbles (artist, song, scrobble_date) " +
            "values ('%s', '%s', now())" % (track_artist.replace("'", "''"), track_name.replace("'", "''")))

    # Make changes to the db and close communications
    conn.commit()
    cur.close()
    conn.close()


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


def get_most_recent_track_time():
    """Get the time of the most recently scrobbled track."""

    # Connect to existing postgres db
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")

    # Set up cursor to perform db operations
    cur = conn.cursor()

    cur.execute("select scrobble_date from scrobbles order by scrobble_date desc")
    most_recent_push_time = cur.fetchone())

    # Make changes to the db and close communications
    cur.close()
    conn.close()

    return(most_recent_push_time)
