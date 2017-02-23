"""API layer - allow user to query oldest artists & move them."""

import argparse
import psycopg2
import psycopg2.extras


def main():
    """Main."""
    action = 's'
    while(action != 'q'):
        print("Artist Queue Menu:")
        print("\tg - get artists you haven't listened to in a while")
        print("\tq - get out")
        action = input('> ')
        print()

        if action == 'q':
            print("Bye then")
        elif action == 'g':
            print("How many artists would you like to be reminded of?")
            n = input('> ')
            print()
            print("""\tHere are your %s artists:""" % n)
            get_least_recently_played_artists(int(n))
            print()
        else:
            print("Hmmm, something seems to have gone awry. Please enter one of the menu options:")
            print()
            action = 's'


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
        print("""- %s \t(last listen: %s)"""
              % (row['artist'], row['last_scrobble_date']))


if __name__ == "__main__":
    main()
