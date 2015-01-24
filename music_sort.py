import eyed3, os, shutil, time, urllib2, json
from urllib import FancyURLopener

toplevel = 'E:\Music\To Sort\\'

remove_table = dict((ord(char), None) for char in '"?\\/*:<|>')

def getAlbumArt(album, artist, date, dest = ''):
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
	url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + searchTerm + '&start=0&userip=71.185.216.176&imgsz=large|xlarge|xxlarge|huge')
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
		print dataInfo[0]['unescapedUrl']
		myopener.retrieve(dataInfo[0]['unescapedUrl'], dest)
	except Exception as e:
		print e
	# Sleep for one second to prevent IP blocking from Google
	time.sleep(1)

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
				if not os.path.exists(toplevel + artist + '\(' + date + ') ' + album + '\cover.jpg'):
					getAlbumArt(album, artist, date)
			else:
				if not os.path.exists(toplevel + artist + '\\' + album):
					os.makedirs(toplevel + artist + '\\' + album)
				if not os.path.exists(toplevel + artist + '\\' + album + '\cover.jpg'):
					getAlbumArt(album, artist, date, toplevel + artist + '\\' + album + '\cover.jpg')
			src = audiofile.path
			dest = toplevel + artist + '\\'
			if date != None and date != 'None':
				dest += '(' + date + ') '
			try:
				dest += album + '\\' + file
			except:
				continue
			try:
				shutil.move(src, dest)
			except IOError as e:
				print e

		elif ending == '.jpg':
			if file != 'cover.jpg':
				os.remove(os.path.join(root, file))
				print 'deleted old album art: ' + file
			else:
				print 'skipped cover.jpg'
		elif ending == '.m4a' or ending == '.m4p' or ending == '.mp4' or ending == '.ini' or ending == '.sfv' or ending == '.nfo':
			filePath = os.path.join(root, file)
			os.remove(filePath)
			print 'deleted {0}'.format(filePath)
		elif fileLower.endswith('.mid') or fileLower.endswith('midi'):
			src = os.path.join(root, file)
			destFolder = toplevel + 'MIDI\\'
			if not os.path.exists(destFolder):
				os.makedirs(destFolder)
			shutil.move(src, destFolder + file)
			print 'moved mid file'
		elif fileLower.endswith('.wav'):
			src = os.path.join(root, file)
			destFolder = toplevel + 'WAV\\'
			if not os.path.exists(destFolder):
				os.makedirs(destFolder)
			shutil.move(src, destFolder + file)
			print 'moved wav file'
		else:
			print 'SKIPPED: ' + file


for _ in range(5):
	# check for empty directories. len(files) == 0 may be overkill
	for curdir, subdirs, files in os.walk(toplevel):
		if len(subdirs) == 0 and len(files) == 0:
			print 'Removed empty directory: {}'.format(curdir)
			os.rmdir(curdir)
