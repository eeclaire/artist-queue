"""Get the recent tracks and get the time a track was most recently played."""

from lastfm import *
import time


def main():
    """Main."""
    most_recent_time = get_most_recent_track_time()
    posix_time = most_recent_time.timestamp()   # convert datetime to posix

    tracks = get_tracks_since_last_time(posix_time)
    save_tracks_to_daily(tracks)


if __name__ == "__main__":
    main()
