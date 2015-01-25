import eyed3, os, shutil, time, urllib2, json, urllib, re

toplevel = 'D:\_Evan backup\music\\'
toplevel = 'E:\Music\Sorted\\'
removeCharacters = dict((ord(char), None) for char in '"?\\/*:<|>')
removeFileTypes = ['.m4a', '.m4v', '.m4p', '.mp4', '.ini', '.sfv', '.nfo', '.rar', '.rtf', '.doc', '.wma', '.wmv', '.flv', '.tqd', '.lnk', '.m3u', '.txt', '.cda', '.bin', '.cue', '.xml', '.pdf', '.zip', '.sfk', '.dat', 'mp3#', '.url', '.avi', '.mpg', 'mpeg', '.wpl', '.vob', 'toc2', '.ape', 'html', '.rmi', '.exe', '.inf', '.rx2', '.sfz', '.sxt', '.fxp', '.exs', '.nki', '.m2v', '.fpl']

class MyOpener(urllib.FancyURLopener):
			version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'


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
				continue
				try:
					audiofile = eyed3.load(root + '\\' + file)
				except Exception as e:
					print e
					continue
				try:
					date = str(audiofile.tag.getBestDate())
					date = unicode(date, "utf-8").strip().translate(removeCharacters)
				except AttributeError as e:
					print e
				try:
					artist = audiofile.tag.artist
					album = audiofile.tag.album
					artist = artist.strip().translate(removeCharacters)
					album = album.strip().translate(removeCharacters)
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

			elif ending == '.jpg' or ending == '.png' or ending == 'jpeg' or ending == '.bmp' or ending == '.gif' or ending == '.tif':
				if file != 'cover.jpg':
					try:
						os.remove(os.path.join(root, file))
						print 'DELETED old album art: ' + file
					except Exception as e:
						print e
				else:
					pass
					# print 'SKIPPED cover.jpg'
			elif ending in removeFileTypes:
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
			elif ending[1:] == '.db':
				filePath = os.path.join(root, file)
				try:
					os.remove(filePath)
					print 'DELETED {0}'.format(filePath)
				except Exception as e:
					print e
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


sortMusic(False, True, False)
