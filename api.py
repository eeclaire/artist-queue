"""API layer - allow user to query oldest artists & move them."""

import argparse
import psycopg2
import psycopg2.extras


def main():
    """Main."""
    get_least_recently_played_artists()


def get_least_recently_played_artists(n=5):
    """Get the n least recently played artists. Defaults to 5."""
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""SELECT *
                   FROM artist_queue
                   ORDER BY last_scrobble_date
                   LIMIT %s""", str(n))

    data = cur.fetchall()
    for row in data:
        print("""You haven't listened to %s since %s"""
              % (row['artist'], row['last_scrobble_date']))
        print(type(row['last_scrobble_date']))


if __name__ == "__main__":
    main()
