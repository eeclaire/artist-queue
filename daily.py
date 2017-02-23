"""Script to run daily to maintain the postgres arist queue and artist set."""

import psycopg2
import psycopg2.extras


def main():
    """Main."""
    add_frequently_played_artists_to_queue()
    move_recent_srobbles_artist_down_queue()
    update_artist_set()


def add_frequently_played_artists_to_queue():
    """Add artists whose music has been scrobbled often."""
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Determine whether I like an artist enough to add them to my artist queue
    # Heads up, the rules used here are pretty arbitrary
    cur.execute("""insert into artist_queue (artist, last_scrobble_date)
                   SELECT artist,
                          max(scrobble_date)
                   from scrobbles
                   where scrobble_date>now()-interval '30' day
                   GROUP BY artist
                   (having count(*) > 15
                   and count(distinct song) > 10)
                   or (count(distinct song) > 30)""")

    # Delete any older duplicates
    cur.execute("""delete from artist_queue as l
    using artist_queue as r
                   where l.artist = r.artist
                   and l.id < r.id""")

    # Make the changes persistent in the database and end communications
    conn.commit()
    cur.close()
    conn.close()


def move_recent_srobbles_artist_down_queue():
    """Push an artist down the queue if they've been listened to recently."""
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Find artists in queue who were played in the last day
    # insert that artist with that most recent date in the queue
    cur.execute("""insert into artist_queue (artist, last_scrobble_date)
                   select s.artist,
                          max(s.scrobble_date)
                   from scrobbles s
                   join artist_queue q on s.artist = q.artist
                   where s.scrobble_date>now()-interval '1' day
                   group by s.artist""")

    # Delete any older duplicates
    cur.execute("""delete from artist_queue as l
                   using artist_queue as r
                   where l.artist = r.artist
                   and l.id < r.id""")

    # Make the changes persistent in the database and end communications
    conn.commit()
    cur.close()
    conn.close()


def update_artist_set():
    """Look at monthly tracks and add artists with more than 2 unique songs."""
    conn = psycopg2.connect("dbname=artistqdb host=localhost user=postgres")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("""insert into confirmed_artists (artist)
                   select artist
                   from scrobbles
                   group by artist
                   having count(distinct song) > 2""")
    # TODO: Figure out how to not insert duplicates (like, "where not exists")

    # Remove any duplicates
    cur.execute("""delete from confirmed_artists as l
                   using confirmed_artists as r
                   where l.artist = r.artist
                   and l.id > r.id""")


if __name__ == "__main__":
    main()
