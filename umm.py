#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  UMM.py - Universal Music Manager, a tool for managing your Google Play Music account. And more.
#  
#  Copyright 2013 Francesco Guarneri <Black_Ram>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 

from gmusicapi.utils import utils
from gmusicapi import Musicmanager
from gmusicapi import Mobileclient
from getpass import getpass
from uuid import getnode as get_mac
from lxml import etree
import gmusicapi.clients
import time
import os
import sys
import re
import socket
import string
import webbrowser
import urllib2
import StringIO
import pwd

class UMM:
	
	
##################################################### LYRICS ###########################################################

	
	def lyrics_from_track(self):
		artist = raw_input('Artist: ')
		title = raw_input('Title: ')
		
		artist_split = ''.join(artist.split())
		title_split = ''.join(title.split())
		
		generate_url = 'http://azlyrics.com/lyrics/' + artist_split + '/' + title_split + '.html'
		
		try:
			response = urllib2.urlopen(generate_url)
		except urllib2.HTTPError:
			print "Lyrics doesn't exist. Please try again."
			time.sleep(0.75)
			UMM.lyrics_from_track()
			
		read_lyrics = response.read()
			
		#Parsing HTML file containing lyrics
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO.StringIO(read_lyrics), parser)
		lyrics = tree.xpath("//div[@style='margin-left:10px;margin-right:10px;']/text()")
		
		print ''
		print  '\033[32m-----------------------------------------\033[0m' 
		
		for words in lyrics:
			print str(words).strip()
		
		print  '\033[32m-----------------------------------------\033[0m'
		
		print ''
		save = raw_input("Do you want to save this lyrics in a txt file in current working directory? [Y/N] ")
		if save == 'y' or save == 'Y':
			f = open(artist + '_' + title + '.txt', 'w')
			f.write("\n".join(lyrics).strip())
			f.close()
			print 'Return to main menu.'
			time.sleep(0.75)
			UMM.read_information()
		
		elif save == 'n' or save == 'N':
			print 'Return to main menu.'
			time.sleep(0.75)
			os.system('clear')
			UMM.read_information()
		
		else:
			print 'Incorrect choice.'
			time.sleep(0.75)
			UMM.lyrics_from_track()
		
					
		
##################################################### UPLOADER ###################################################################

	def songs_uploader(self):
		ip = urllib2.urlopen('http://ip.42.pl/raw').read() #Obtain your public IP address
		mac_binary = str(get_mac()) #Obtain binary MAC address
		temp = mac_binary.replace(':', '').replace('-', '').replace('.', '').upper()
		mac_h3x = temp[:2] + ":" + ":".join([temp[i] + temp[i+1] for i in range(2,12,2)]) #Convert MAC from 48bit int to hexadecimal string
		user = pwd.getpwuid(os.getuid())[0] #Get your system's username
		
		api = Musicmanager()
		hostname = '<' + ip + '>' + '' + '(gmusicapi-{2.0.0})'
		Musicmanager.perform_oauth(storage_filepath='/home/' + user + '/.config/gmusicapi/oauth.cred', open_browser=False)
		api.login(oauth_credentials='/home/' + user + '/.config/gmusicapi/oauth.cred', uploader_id=mac_h3x, uploader_name=hostname)
		gmusicapi.clients.Musicmanager(debug_logging=True, validate=True)
		
		#newWorkingDirectory = '../home'
		#os.path.join(os.path.abspath(sys.path[0]), newWorkingDirectory) #Change the working directory
		filepath = '/home/blackram/Scrivania/BRES_/UMM/ciao.mp3'
		uploading = api.upload(filepath, transcode_quality=3, enable_matching=False)
		print 'Uploading...'
		f = open('uploading.txt','w') #log
		f.write(str(uploading))
		f.close()
		
		final = re.search("GetUploadSession error 200: this song is already uploaded", open('uploading.txt','r').read())
		if final is None:
			print '\033[32mTrack uploaded!\033[0m'
		else:
			print '\033[31mTrack already exists in your library!\033[0m'
		
		choice = raw_input("Exit from uploader? [Y/N] ")
		if choice == 'y' or choice == 'Y':
			print 'Return to main menu.'
			Musicmanager.logout(revoke_oauth=False)
			UMM.read_information()
		elif choice == 'n' or choice == 'N':
			print 'Okay.'
			UMM.songs_uploader()
		
		

#################################################### PLAYLIST DOWNLOADER (not working) ####################################################################
	
	def download_songs(self):
		api = Musicmanager()
		ip = urllib2.urlopen('http://ip.42.pl/raw').read() #Obtain your public IP address
		mac_binary = str(get_mac()) #Obtain binary MAC address
		temp = mac_binary.replace(':', '').replace('-', '').replace('.', '').upper()
		mac_h3x = temp[:2] + ":" + ":".join([temp[i] + temp[i+1] for i in range(2,12,2)]) #Convert MAC from 48bit int to hexadecimal string
		user = pwd.getpwuid(os.getuid())[0] #Get your system's username
		hostname = '<' + ip + '>' + '' + '(gmusicapi-{2.0.0})'
		Musicmanager.perform_oauth(storage_filepath='/home/' + user + '/.config/gmusicapi/oauth.cred', open_browser=False)
		api.login(oauth_credentials='/home/' + user + '/.config/gmusicapi/oauth.cred', uploader_id=mac_h3x, uploader_name=hostname)
		gmusicapi.clients.Musicmanager(debug_logging=True, validate=True)		
		playlist_id = raw_input("insert id: ")
		
		api_ = Mobileclient()
		api_.login(self.email, self.password)
		playlist_method = api_.get_all_playlists()
		
		#Obtain ID
		#Analize songs of this ID
		#Take song's IDs
		#Download from ID
		
		
##################################################### PLAYLIST MANAGER ###########################################################

	
	def playlist_manager(self):
		#Get playlist's ID
		all_playlists = self.api.get_all_playlists(incremental=False, include_deleted=False)		
		f = open('all_playlists.txt','w')
		f.write(str(all_playlists))
		f.close()
		playlist_id = re.findall("u'id': u'(.*?)'", open('all_playlists.txt','r').read())
		playlist_name = re.findall("u'name': u'(.*?)'", open('all_playlists.txt','r').read())
		
		print ''
		print '\033[31mPlaylist ID - Playlist name\033[0m'
		
		#Print all playlists with their ID and name
		for a, b in zip(playlist_id, playlist_name):
			print a + ' ' + '-' + ' ' + b
			
		
		print ''
		
		print '1. Create a playlist.'
		print '2. Add songs to playlist.'
		choice = input("Insert number: ")
				
		
		if choice == 1:
			playlist_name = raw_input("Insert playlist's name: ")
			playlist_id = self.api.create_playlist(playlist_name)
			print 'Playlist created!'
			time.sleep(0.75)
			UMM.login()
		
		elif choice == 2:
			playlist_id = raw_input("Insert playlist ID: ")
			print '1. Insert Artist.'
			print '2. Insert Album.'
			second_choice = input("Insert number: ")
			
			#Add discography of an artist in a playlist
			if second_choice == 1:
				library = self.api.get_all_songs()
				artist = raw_input("Insert Artist: ")
				tracks = [track for track in library if track['artist'] == artist]
				songs = re.findall("u'id': u'(.*?)'", str(tracks))
				number = len(songs)
				self.api.add_songs_to_playlist(playlist_id, songs[0:int(number)])
				print 'Songs added!'
				time.sleep(0.75)
				UMM.login()
				
			#Add album in a playlist
			if second_choice == 2:
				library = self.api.get_all_songs()
				album = raw_input("Insert Album: ")
				tracks = [track for track in library if track['album'] == album ]
				album = re.findall("u'id': u'(.*?)'",  str(tracks))
				number = len(album)
				self.api.add_songs_to_playlist(playlist_id, album[0:int(number)])
				print 'Album added!'
	

##################################################### ARTIST & ALBUM INFO ###########################################################


	def artist_album_info(self):
		os.system('clear')
		library = self.api.get_all_songs()
		choice = raw_input("[A]rtist or [a]lbum? ")
		
		if choice == 'a':
			for_album_no_capitalize = raw_input("Insert album: ")
			for_album = string.capwords(for_album_no_capitalize)
			tracks_for_album = [track for track in library if track['album'] == for_album]
			
			tracks = re.findall("u'title': u'(.*?)'", str(tracks_for_album))
			
			print ''
			print '--------------------------'
			
			for track in tracks:
				print track
			
			print '--------------------------'
		
		
		elif choice == 'A':
			#Print album of an artist
			for_artist_no_capitalize = raw_input("Insert artist: ")
			for_artist = string.capwords(for_artist_no_capitalize)
			
			tracks_for_artist = [track for track in library if track['artist'] == for_artist]
			
			print ''
			albums = re.findall("u'album': u'(.*?)'", str(tracks_for_artist))
			
			print ''
			print '---------------------------'
			
			a = []
			
			for c in albums:
				if c not in a:
					a.append(c)
			for d in a:
				print d
			
			print '---------------------------'

			
##################################################### LOGIN ###########################################################

	
	def login(self):
		#API with MobileClient
		while not self.logged_in and self.attempts < 3:
			self.logged_in = self.api.login(self.email, self.password)
			self.attempts += 1
		
		os.system('clear')
		if self.logged_in == True:
			library = self.api.get_all_songs()
			print '\033[32mHey there! You have ' + str(len(library)) + ' songs in your library.\033[0m'
		elif self.logged_in == False:
			if self.email == None:
				print "\033[31mYou don't logged in GMusic service.\033[0m"
				pass
			else:
				data = raw_input('\033[31mIncorrect login data. Please login. [Y/N] (N if you want to use only lyrics)\033[0m')
				if data == 'y' or data == 'Y':
					UMM.read_information()
				elif data == 'n' or data == 'N':
					os.system('clear')
					pass
			
			
		print '1. Upload songs.'
		print '2. Playlist downloader (NOT WORKING).'
		print '3. Artist & Album info.'
		print '4. Playlist manager.'
		print '5. Lyrics.'

		print ''
		print '6. Erase login data.'
		print '7. Quit.'
		
		try:
			choice = input('Insert number: ')
			if choice == 1:
				self.api.logout()
				UMM.songs_uploader()
			elif choice == 2:
				UMM.download_songs()
			elif choice == 3:
				UMM.artist_album_info()
			elif choice == 4:
				UMM.playlist_manager()
			elif choice == 5:
				UMM.lyrics_from_track()
			elif choice == 6:
				UMM.clear_login_data()
			elif choice == 7:
				print 'Bye Bye!'
				time.sleep(0.75)
				sys.exit()
		
		except EOFError:
			sys.exit()
					
	
	#Erase your 'login.txt' file containing your credentials for login in this service.		
	def clear_login_data(self):
		f = open('login.txt', 'r+')
		f.truncate()
		print 'Login data erased successfully.'
		os.system('clear')
		UMM.read_information()
		
		

##################################################### INIT ###########################################################


	
	def read_information(self):
		#API with MobileClient
		self.api = Mobileclient()
		self.logged_in = False
		self.attempts = 0
		self.login_data = raw_input("Are you already logged in? [Y/N] | Continue without login [W] | Exit [Q] -> ")
		print ''
		print '\033[31mREADME: this login is reported to MobileClient API, not MusicManager (upload!)\033[0m'
		time.sleep(0.85)
		
		if self.login_data == 'y' or self.login_data == 'Y': #Beta function to save you credentials in a txt file. Sometimes It doesn't work.
			f = open('login.txt','r')
			try:
				read = f.readlines()[0]
				split = read.split()
				self.email = split[0]
				self.password = split[1]
			except:
				print 'Login file empty!'
				UMM.read_information()
			finally:
				f.close()
				UMM.login()
			
		
		elif self.login_data == 'n' or self.login_data == 'N':
			self.email = raw_input("Insert email: ")
			self.password = getpass("Insert password: ")
			f = open('login.txt','w')
			f.write(self.email + ' ')
			f.close()
			f = open('login.txt','a')
			f.write(self.password)
			UMM.login()
		
		elif self.login_data == 'q' or self.login_data == 'Q':
			print 'Bye bye!'
			time.sleep(0.50)
			sys.exit()
		
		elif self.login_data == 'w' or self.login_data == 'W':
			self.email = None
			self.password = None
			self.logged_in = False
			UMM.login()
		
		else:
			print 'Not a valid choice. Please re-insert.'
			time.sleep(0.50)
			os.system('clear')
			UMM.read_information()
		

		
if __name__ == '__main__':
	UMM = UMM()
	UMM.read_information()
