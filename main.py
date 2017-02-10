"""Get the recent tracks and get the time a track was most recently played."""

from lastfm import *


def main():
    """Main."""
    tracks = get_tracks_since_last_time()
    most_recent_time = get_most_recent_track_time(tracks)
    #print("number of tracks: %s" % len(tracks))
    #get_artists_from_tracks(tracks)


if __name__ == "__main__":
    main()
