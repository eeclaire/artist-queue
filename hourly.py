"""Script to run hourly to maintain the postgres scrobbles table."""

from lastfm import *
import time
import psycopg2
import psycopg2.extras


def main():
    """Main."""
    most_recent_time = get_most_recent_track_time()
    posix_time = most_recent_time.timestamp()   # convert datetime to posix

    tracks = get_tracks_since_last_time(posix_time)
    save_tracks_to_daily(tracks)


def get_most_recent_track_time():
    """Get the time of the most recently scrobbled track."""
    # Connect to existing postgres db and set up cursor
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")
    cur = conn.cursor()

    cur.execute("""select scrobble_date
                   from scrobbles
                   order by scrobble_date desc""")
    result = cur.fetchone()
    most_recent_push_time = result[0]

    # Make changes to the db and close communications
    cur.close()
    conn.close()

    return(most_recent_push_time)


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

        # If the track name exists in the list of confirmed artists,
        # the scrobbler probably mixed up the artist and song name.
        # They should be flipped before insertion into scrobble table.
        cur.execute("""select artist
                       from confirmed_artists
                       where artist like %s""", [track_name.replace("'", "'")])
        if cur.fetchone() is not None:
            track_artist = track['name']
            track_name = track['artist']['#text']

        # Insert the artist, song name and scrobble date into scrobble table
        cur.execute("""insert into scrobbles (artist, song, scrobble_date)
                                              values (%s, %s, now())""",
                    [track_artist.replace("'", "'"),
                     track_name.replace("'", "'")])

    # Make changes to the db and close communications
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
