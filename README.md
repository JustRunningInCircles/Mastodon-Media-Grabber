# Mastodon-Media-Grabber
Trawls *original* posts of your profile and downloads any media you uploaded in your toots.
This means only toots you have initiated.
Not boosts or indeed at the moment replies

The intent is to provide a way of taking a local backup of your media in case your instance goes down.

Run it by:
1) python MastodonMediaGrabber.py https://my.instance/@myProfile saveDirectory 
2) Calling the script and working interactively with it

What you will get is a Media folder in the saveDirectory you specify.
Within that will be a directory for each day you tooted some media, containing that media.
Subsequent runs with the same settings will only download new media (though it will crawl the whole timeline to check).

You will need BeautifulSoup installed see here https://www.crummy.com/software/BeautifulSoup/
I do NOT have any Windows environments to test on so YMMV. It *should* work.
I do NO sanity checking of the URLs or locations, so give it something sensible or it WILL break.

I am not a Python Programmer by trade, so it was written to refresh my Python knowledge and there may be *much* better ways of achieving this (API etc...)
