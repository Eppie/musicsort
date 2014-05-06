import eyed3
import glob
import os
import shutil
import sys
import time
from urllib import FancyURLopener
import urllib2
import json
toplevel = 'C:\Users\Eppie\Desktop\projects\music\\'

def getAlbumArt(album):
    searchTerm = album + ' album cover'
    searchTerm = searchTerm.replace(' ','%20')
    class MyOpener(FancyURLopener): 
        version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
    myopener = MyOpener()
    url = ('https://ajax.googleapis.com/ajax/services/search/images?' + 'v=1.0&q='+searchTerm+'&start=0&userip=96.245.204.180&imgsz=large|xlarge|xxlarge|huge')
    request = urllib2.Request(url, None, {'Referer': 'testing'})
    response = urllib2.urlopen(request)
    # Get results using JSON
    results = json.load(response)
    data = results['responseData']
    dataInfo = data['results']
    print dataInfo[0]['unescapedUrl']
    myopener.retrieve(dataInfo[0]['unescapedUrl'],toplevel + artist + '\(' + date + ') ' + album + '\cover.jpg')
    # Sleep for one second to prevent IP blocking from Google
    time.sleep(1)
    
for file in glob.glob("*.mp3"):
    print file
    audiofile = eyed3.load(file)
    artist = audiofile.tag.artist
    album = audiofile.tag.album
    title = audiofile.tag.title
    date = str(audiofile.tag.getBestDate())
    artist = artist.strip()
    album = album.strip()
    title = title.strip()
    date = date.strip()
##    print 'Artist: ' + artist
##    print 'Album: ' + album
##    print 'Song Title: ' + title
##    print 'Date: ' + date
##    print '------------------------------------------'
    if not os.path.exists(toplevel + artist):
        os.makedirs(toplevel + artist)
    if not os.path.exists(toplevel + artist + '\(' + date + ') ' + album):
        os.makedirs(toplevel + artist + '\(' + date + ') ' + album)
    if not os.path.exists(toplevel + artist + '\(' + date + ') ' + album + '\cover.jpg'):
        getAlbumArt(album)
    src = audiofile.path
    dest = toplevel + artist + '\(' + date + ') ' + album + '\\' + file
    shutil.move(src,dest)
