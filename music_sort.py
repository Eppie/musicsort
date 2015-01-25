import eyed3, os, shutil, time, urllib2, json, urllib, re
from urllib import FancyURLopener

# toplevel = 'E:\Music\To Sort\\'
toplevel = 'D:\_Evan backup\music\\'
remove_table = dict((ord(char), None) for char in '"?\\/*:<|>')


def getExternalIP():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address


def getAlbumArt(album, artist, date, output, dest = ''):
	try:
		print "getting art for album: {0}".format(album)
	except UnicodeEncodeError as e:
		print e
		return
	searchTerm = artist + ' ' + album + ' album cover'
	searchTerm = searchTerm.replace(' ', '%20')
	class MyOpener(FancyURLopener):
			version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
	myopener = MyOpener()
	IP = getExternalIP()
	try:
		url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}&start=0&userip={1}').format(searchTerm, IP)
	except Exception as e:
		print e
		return
	request = urllib2.Request(url, None, {'Referer': 'testing'})
	try:
		response = urllib2.urlopen(request)
	except UnicodeEncodeError as e:
		print e
		return
	# Get results using JSON
	results = json.load(response)
	data = results['responseData']
	dataInfo = data['results']
	if dest == '':
		dest = toplevel + artist + '\(' + date + ') ' + album + '\cover.jpg'
	try:
		if output:
			print dataInfo[0]['unescapedUrl']
		myopener.retrieve(dataInfo[0]['unescapedUrl'], dest)
	except Exception as e:
		print e
	# Sleep for one second to prevent IP blocking from Google
	time.sleep(1)


def sortMusic(art = False, remove = True, output = True):
	for root, dirnames, filenames in os.walk(toplevel):
		for file in filenames:
			fileLower = file.lower()
			ending = fileLower[-4:]
			if ending == '.mp3':
				try:
					audiofile = eyed3.load(root + '\\' + file)
				except Exception as e:
					print e
					continue
				try:
					date = str(audiofile.tag.getBestDate())
					date = unicode(date, "utf-8").strip().translate(remove_table)
				except AttributeError as e:
					print e
				try:
					artist = audiofile.tag.artist
					album = audiofile.tag.album
					artist = artist.strip().translate(remove_table)
					album = album.strip().translate(remove_table)
				except AttributeError:
					try:
						print 'Artist: ' + str(artist)
						print 'Album: ' + str(album)
						print 'Date: ' + date
						print '------------------------------------------'
					except Exception as e:
						print e
					src = os.path.join(root, file)
					destFolder = toplevel + 'Unknown\\'
					if not os.path.exists(destFolder):
						os.makedirs(destFolder)
					shutil.move(src, destFolder + file)
					continue

				if not os.path.exists(toplevel + artist):
					os.makedirs(toplevel + artist)
				if date != None and date != 'None':
					if not os.path.exists(toplevel + artist + '\(' + date + ') ' + album):
						os.makedirs(toplevel + artist + '\(' + date + ') ' + album)
					if not os.path.exists(toplevel + artist + '\(' + date + ') ' + album + '\cover.jpg') and art:
						getAlbumArt(album, artist, date, output)
				else:
					if not os.path.exists(toplevel + artist + '\\' + album):
						os.makedirs(toplevel + artist + '\\' + album)
					if not os.path.exists(toplevel + artist + '\\' + album + '\cover.jpg') and art:
						getAlbumArt(album, artist, date, output, toplevel + artist + '\\' + album + '\cover.jpg')
				src = audiofile.path
				dest = toplevel + artist + '\\'
				if date != None and date != 'None':
					dest += '(' + date + ') '
				try:
					dest += album + '\\' + file
				except Exception as e:
					print e
					continue
				try:
					shutil.move(src, dest)
				except IOError as e:
					print e

			elif ending == '.jpg':
				if file != 'cover.jpg':
					os.remove(os.path.join(root, file))
					print 'DELETED old album art: ' + file
				else:
					print 'SKIPPED cover.jpg'
			elif ending == '.m4a' or ending == '.m4p' or ending == '.mp4' or ending == '.ini' or ending == '.sfv' or ending == '.nfo' or ending == '.wma' or ending == '.wmv' or ending[1:] == '.db' or ending == '.flv' or ending == '.tqd' or ending == '.lnk' or ending == '.m3u' or ending == '.txt' or ending == '.cda' or ending == '.bin' or ending == '.cue' or ending == '.xml':
				filePath = os.path.join(root, file)
				try:
					os.remove(filePath)
					print 'DELETED {0}'.format(filePath)
				except Exception as e:
					print e
			elif fileLower.endswith('.mid') or fileLower.endswith('midi'):
				src = os.path.join(root, file)
				destFolder = toplevel + 'MIDI\\'
				if not os.path.exists(destFolder):
					os.makedirs(destFolder)
				shutil.move(src, destFolder + file)
				print 'MOVED mid file'
			elif fileLower.endswith('.wav'):
				src = os.path.join(root, file)
				destFolder = toplevel + 'WAV\\'
				if not os.path.exists(destFolder):
					os.makedirs(destFolder)
				shutil.move(src, destFolder + file)
				print 'MOVED wav file'
			elif fileLower.endswith('.flac'):
				src = os.path.join(root, file)
				destFolder = toplevel + 'FLAC\\'
				if not os.path.exists(destFolder):
					os.makedirs(destFolder)
				shutil.move(src, destFolder + file)
				print 'MOVED flac file'
			else:
				print 'SKIPPED: ' + file
	if remove:
		removeEmpty()


def removeEmpty():
	for _ in range(5):
		# check for empty directories. len(files) == 0 may be overkill
		for curdir, subdirs, files in os.walk(toplevel):
			if len(subdirs) == 0 and len(files) == 0:
				try:
					os.rmdir(curdir)
					print 'Removed empty directory: {0}'.format(curdir)
				except Exception as e:
					print e


sortMusic(True, True, False)
