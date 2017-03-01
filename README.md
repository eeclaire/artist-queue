# I hate new music

I don't actually hate new music, but it _is_ harder for me to focus on work when I'm listening to something that isn't familiar. Either I dig it and I'm distracted by its cool novelty, or I don't like it and it doesn't put me in a produtive mood. Usually I just listen to bands that I already know, but I often end up stuck in a rut, listening to the same 4 artists over and over. 

The _real_ jackpot is when I remember a band or artist I loved several months ago, but that I'd since forgotten about. 

The problem with that is that brains and memory don't always work how you want them to, and I can't just rememeber something I'd forgotten about on command. However, sometimes you can get computers to work how you want them to. I decided to do future-me a favor, and keep track of what music I'm listening to using the last.fm API, where last.fm is synced up to my Spotify and YouTube accounts. The idea is to run a cronjob every hour or so to see what music I've been listening to, then push artists that I tend to listen to more than once to a queue. Every time I listen to that artist, they should get pushed back to the bottom of the queue. What should happen, is that artists that I haven't listened to in a while should bubble up to the top of that queue. If I'm ever feeling sick of listening to the same artists over and over, I should be able to pull up the top X artists in the queue - the X artists I haven't listened to in the longest time, and that presumably I've forgotten about.

## Cron
Add the command that runs the query on your recent last.fm listens to your crontab. In Linux, you can do this by entering `crontab -e` into your terminal. I wrote a shell script called `get-music-cron.sh` to change directories into my current one (instead of the default home) and run the python script that queries last.fm. My crontab line to run this command every hour looks like
```
0 * * * * * . ~/Projects/artistQ/get-music-cron.sh
```

Next I will create a cronjob that will run daily in order to go through all of the music I've listened to that day, and add it to my monthly listens. 

## How to use
"But Claire" you might say, "this sounds cool and all, but how do _I_ do that?"  
Luckily for you, a lot of 



