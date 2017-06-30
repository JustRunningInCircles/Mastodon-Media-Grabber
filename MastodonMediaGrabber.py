#!/usr/bin/python

#    Copyright 2017 Iain Berwick

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Very alpha and flaky :-)
# You will need BeautifulSoup installed see here https://www.crummy.com/software/BeautifulSoup/
# I do NOT have any Windows environments to test on so YMMV. It *should* work.
# I do NO sanity checking of the URLs or locations, 
# so give it something sensible or it WILL break.

#-----------------------------------------------------------------------------
import sys
import urllib.request
import os
from bs4 import BeautifulSoup


#-----------------------------------------------------------------------------
# Default environment if we get nothing passed - set up for me...
# Change this unless you want a load of random pictures :-)
# But if that is your preference, you'd be better off following me.

# You can:
# 1) Change these in the file here 
# 2) Call the program like this: ./MastodonMediaGrabber.py https://my.instance/@myProfile saveDirectory 
# 3) Let it prompt you for changes
config = {
    "profileURL" : "https://social.tchncs.de/@RunningInCircles",
    "downloadLocation" : "./RetrievedFiles"
    }

#-----------------------------------------------------------------------------
# Grabs the media files identified by getPageOfToots()
def getMedia(datestamp, mediaURL, directory):
    foldername = datestamp[:10:] # Grab just the date portion YYYY-MM-DD
    filename = mediaURL.split("?")[0].split("/")[-1] # Grab filename.ext portion
    # Create a dated folder if there is not one already
    if not os.path.exists(os.path.join(config["downloadLocation"],"Media", foldername)):
        os.makedirs(os.path.join(config["downloadLocation"], "Media", foldername))
    fileLocation = os.path.join(config["downloadLocation"], "Media", foldername, filename)
    # Check if we have already downloaded a file
    if not os.path.exists(fileLocation):
        # We haven't so let's try and get it
        response = urllib.request.urlopen(mediaURL)
        if response is not None:
            mediaData = response.read()
            saveFile = open(fileLocation, "wb") # Write as bytes
            saveFile.write(mediaData)
            print("Downloaded", mediaURL)
            saveFile.close()
    
#-----------------------------------------------------------------------------
# Starts with a page of toots and finds yours, then identifies media attachments
def getPageOfToots(url, directory):
    response = urllib.request.urlopen(url)
    if response is not None:
        pageData = response.read()
        parsedHTML = BeautifulSoup(pageData, "lxml")
        # Filter out boosts - looking only for your entries
        toots = parsedHTML.body.findAll("div", attrs={"class":"entry h-entry"})
        for number,toot in enumerate(toots):
            tootTime = toot.find("time")
            tootMedia = toot.findAll("div", attrs={"class":"media-item"})
            for num, mediaItem in enumerate(tootMedia):
                # Use the profile to build a full not relative URL
                mediaURL = config["profileURL"].split("@")[0]+mediaItem.find("a")["href"][1::] # Strip preceding slash using slices
                #Download media
                getMedia(tootTime["datetime"], mediaURL, directory)
            # Find the subsequent page
        nextPage = parsedHTML.body.find("div", attrs={"class":"pagination"})
        if nextPage.find("a"):
            nextPage = nextPage.find("a")["href"]
            getPageOfToots(nextPage, config["downloadLocation"])
    else:
        print("Could not open ", url)

def getConfig(url, location):
    print("OK, we are starting with...")
    print("OK, we now have...")
    print("Profile  = ",url)
    print("Storage  = ",location)
    print("Run with these options")
    while input("OK? y/n ").upper() != "Y":
        url = input("URL of the profile page i.e https://my.instance/@myProfile ")
        location = input("Directory where you want the media files stored ")
        print("OK, we now have...")
        print("Profile  = ",url)
        print("Storage  = ",location)
    return url, location


#-----------------------------------------------------------------------------
# Detect if we got something else to work with or run with the defaults

if len(sys.argv)==1:    
    config["profileURL"], config["downloadLocation"] = getConfig(config["profileURL"],config["downloadLocation"])
elif len(sys.argv)==2:
    config["profileURL"], config["downloadLocation"] = getConfig(sys.argv[1], config["downloadLocation"])
elif len(sys.argv)>2:
    config["profileURL"], config["downloadLocation"] = getConfig(sys.argv[1],sys.argv[2])

#-----------------------------------------------------------------------------
# OK lets go ahead and try a connection to the profile before we proceed
try:
    response = urllib.request.urlopen(config["profileURL"])
except:
    print("Couldn't get to the profile:", config["profileURL"])
    print("Got:",response)
# Now let's set up the downloadLocation
if not os.path.exists(config["downloadLocation"]):
    os.makedirs(config["downloadLocation"]) # Create a directory if needed


#-----------------------------------------------------------------------------
# OK lets go ahead and start downloading media
getPageOfToots(config["profileURL"], config["downloadLocation"])

