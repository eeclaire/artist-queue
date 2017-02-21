"""Get the recent tracks and get the time a track was most recently played."""

from lastfm import *
import time


def main():
    """Main."""
    most_recent_time = get_most_recent_track_time()
    # TODO: Convert datetime to epoch before passing to get_tracks

    tracks = get_tracks_since_last_time()
    #print(json.dumps(tracks, sort_keys=True, indent=4))
    #print("number of tracks: %s" % len(tracks))
    save_tracks_to_daily(tracks)


if __name__ == "__main__":
    main()
