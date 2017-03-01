# I hate new music

I don't actually hate new music. I like to listen to music when I'm coding, but I prefer music I already know so that I don't get distracted by the novelty of a cool new song. Unfortunately, I often end up stuck in a rut, listening to the same 4 artists over and over. 

What's *great* is when I remember a band or artist I loved several months ago, but that I'd since forgotten about. 

The problem with that is that brains and memory don't always work how you want them to, and I can't just rememeber something I'd forgotten about on command. However, computers are pretty good at memory, if you set them up right. I decided to do future-me a favor, and keep track of what music I'm listening to using the [last.fm API](http://www.last.fm/api), where last.fm is synced up to my Spotify and YouTube accounts. The idea is to run a cronjob every hour or so to see what music I've been listening to, then push artists that I tend to listen to more than once to a queue. Every time I listen to that artist, they should get pushed back to the bottom of the queue. What should happen, is that artists that I haven't listened to in a while should bubble up to the top of that queue. If I'm ever feeling sick of listening to the same artists over and over, I should be able to pull up the top X artists in the queue - the X artists I haven't listened to in the longest time, and that presumably I've forgotten about.


## Requirements
If you want to use this, you're going to need to do a little setup first:
1. Make sure you have Python3. Because of time manipulations, this setup isn't backwards compatible.
2. You're going to need to have a last.fm account. If you don't already have one, you can sign up [here](https://www.last.fm/join). _Make sure you switch the 'user' field in `lastfm.py` to *your* username._
3. If you don't listen to music on last.fm directly, you're going to want to set yourself up to [scrobble](https://www.last.fm/about/trackmymusic) music to your account. This just means last.fm will capture songs you listen to on other mediums, like Spotify or Youtube, and list them in your last.fm music profile.
..* If you're using Spotify, make sure you set up scrobbling for each platform you use to listen to Spotify (mobile, desktop, web, etc...). Last.fm has instructions for each platform [here](https://support.spotify.com/us/account_payment_help/account_settings/scrobble-to-last-fm/)
..* YouTube doesn't officially support scrobbling, but there are some browser extensions that will scrobble music from YouTube to last.fm for you [listed here](https://getsatisfaction.com/lastfm/topics/youtube-scrobbling).
4. You'll need to install PostgreSQL and the [psycopg2](https://pypi.python.org/pypi/psycopg2) library and setup up a few tables. I'll go into more detail on that [here](#PostgreSQL)
5. [Set up a cron job](#Cron) that will run the `hourly-cron.sh` script every hour or so.

### PostgreSQL
Run ```pip install psycopg2``` (use pip3 if your default python isn't python 3)  
You'll need to create a local PostgreSQL database called 'artistqdb'. In that database, you should also create four tables:

#### scrobbles

| Column        | Type                        | Modifiers                                              |
|---------------|:----------------------------|:-------------------------------------------------------|
| id            | integer                     |  not null default nextval('scrobbles_id_seq'::regclass)|
| artist        | text                        |                                 					   |
| song          | text                        |                                 					   |
| scrobble_date | timestamp without time zone |                                                        |

#### artist_queue
| Column             | Type                        | Modifiers                                                  |
|--------------------|:----------------------------|:-----------------------------------------------------------|
| id                 | integer                     |  not null default nextval('artist_queue_id_seq'::regclass) |
| artist             | text                        |                                                            |
| last_scrobble_date | timestamp without time zone |                                                            |

#### confirmed_artists
| Column   | Type    | Modifiers                                                       |
|----------|---------|-----------------------------------------------------------------|
| id       | integer |  not null default nextval('confirmed_artists_id_seq'::regclass) |
| artist   | text    |                                                                 |

#### rundaily
| Column   | Type                        | Modifiers                                              |
|----------|-----------------------------|--------------------------------------------------------|
| id       | integer                     |  not null default nextval('rundaily_id_seq'::regclass) |
| last_run | timestamp without time zone |                                                        |



### Cron
Add the command that runs the query on your recent last.fm listens to your crontab. In Linux, you can do this by entering `crontab -e` into your terminal. I wrote a shell script called `hourly-cron.sh` to change directories into my current one (instead of the default home) and run the python script that queries last.fm. My crontab line to run this command every hour looks like
```
0 * * * * * . ~/Projects/artistQ/hourly-cron.sh
```




