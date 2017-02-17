"""Handle saving and reading to and from the biweekly json and the queue."""

import json
import time


def main():
    """Main."""
    monthly_track_file = 'monthly.json'

    with open(monthly_track_file, 'r') as fp:
        monthly_tracks = json.load(fp)
    fp.close()

    # Update the artists
    artists = read_artist_set()
    new_artists_set = update_artist_set(monthly_tracks, artists)

    with open('artists.csv', 'w') as fp:
        for artist in new_artists_set:
            fp.write("%s\n" % artist)
    fp.close()

    tracks_dict = read_todays_tracks(new_artists_set)
    monthly_tracks = add_todays_tracks(tracks_dict, monthly_tracks)

    with open(monthly_track_file, 'w') as fp:
        json.dump(monthly_tracks, fp, sort_keys=True, indent=4)
    fp.close()


def update_artist_set(monthly_tracks, artists_set):
    """Look at monthly tracks and add artists with more than 2 unique songs."""
    for artist in monthly_tracks.keys():
        if len(monthly_tracks[artist]['unique_songs']) > 2:
            artists_set.add(artist)

    return artists_set


def read_artist_set():
    """Read in list of confirmed artists."""
    artists = set()
    with open('artists.csv', 'r') as fp:
        for line in fp:
            artists.add(line.strip('\n'))
    fp.close()
    return(artists)


def read_todays_tracks(artists):
    """Read in today's tracks and re-format for future use."""
    lines = []
    with open('daily.csv', 'r') as fp:
        for line in fp:
            lines.append(clean_up_track(line, artists))
    fp.close()

    return lines


def clean_up_track(line, artists):
    """Turn each track line read in into a dict with artist, song, date."""
    line = line.strip('\n{}')
    artist_song = line.split(': ')
    artist = artist_song[0].strip('"')
    song = artist_song[1].strip('"')

    # Make sure the song name and artist weren't switched
    if song in artists:
        artist_song_dict = {'artist': song, 'song': artist}
    else:
        artist_song_dict = {'artist': artist, 'song': song}

    return artist_song_dict


def add_todays_tracks(todays_tracks_dict, tracks):
    """Add new tracks to the monthly file."""
    date = time.struct_time(time.gmtime(time.time()))
    month = date[1]
    today = date[2]

    for track in todays_tracks_dict:
        artist = track['artist']
        song = track['song']

        # If you already have that artist
        if tracks.get(artist) is not None:
            # Check if you have the song, if you do, update it
            if tracks[artist]['unique_songs'].get(song) is not None:
                # Increment playcounts
                tracks[artist]['playcount'] = tracks[artist]['playcount'] + 1
                new_cnt = tracks[artist]['unique_songs'][song]['playcount'] + 1
                tracks[artist]['unique_songs'][song]['playcount'] = new_cnt
                # Update the most recent date
                tracks[artist]['unique_songs'][song]['most_recent_play']['month'] = month
                tracks[artist]['unique_songs'][song]['most_recent_play']['day'] = today
            else:
                tracks[artist]['playcount'] = tracks[artist]['playcount'] + 1
                tracks[artist]['unique_songs'][song] = {
                    'playcount': 1,
                    'most_recent_play': {
                        'month': month,
                        'day': today
                    }
                }
        else:
            # New artist - initialize
            tracks[artist] = {
                'playcount': 1,
                'unique_songs': {
                    song: {
                        'playcount': 1,
                        'most_recent_play': {
                            'month': month,
                            'day': today
                        }
                    }

                }
            }

    return tracks


def remove_old_tracks():
    """Read in the whole monthly.json and removes old tracks."""
    print("remove old")


def add_tracks_to_biweekly_cache(tracks_dict):
    """Insert artists+song count into dictionary cleaned every 2 weeks."""
    biweekly_cache_filename = 'biweekly.json'

    # get current songs in the biweekly store if they exist
    if os.path.isfile(biweekly_cache_filename):
        with open(biweekly_cache_filename, 'r') as filein:
            tracks = json.load(filein)
    else:
        tracks = {}
    print(tracks)


if __name__ == "__main__":
    main()
