#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
from os import path
import math
import os
import glob
import random
import time
import datetime
import urllib3
import re
import calendar

#youtube-dl -f 22 --output "/mnt/mydisk/trailers/%(title)s.%(ext)s" 4PdTapNIr-k

text_file = open("/home/pi/Output.txt", "w")
text_file.write("test")
text_file.close()

drive = '/mnt/mydisk/'

next_video_to_play = None
last_video_played = ''

commercials = []
trailers = []
policy = []
countdowns = []
films = []
trivia = []
preview = []
feature = []
sound = []

def get_videos_from_dir(dir):
	results = glob.glob(os.path.join(dir, '*.mp4'))
	results.extend(glob.glob(os.path.join(dir, '*.avi')))
	results.extend(glob.glob(os.path.join(dir, '*.mkv')))
	results.extend(glob.glob(os.path.join(dir, '*.mov')))
	results.extend(glob.glob(os.path.join(dir, '*.flv')))
	results.extend(glob.glob(os.path.join(dir, '*.wmv')))
	
	return results

def preload_videos():
	global drive
	global commercials
	global trailers
	global policy
	global countdowns
	global films
	global trivia
	global sound
	global feature
	global preview

	preview = []
	feature = []
	sound = []
	commercials = []
	trailers = []
	policy = []
	countdowns = []	
	films = []
	trivia = []
	
	preview = get_videos_from_dir(drive + "preview/")
	feature = get_videos_from_dir(drive + "feature/")
	sound = get_videos_from_dir(drive + "sound/")
	commercials = get_videos_from_dir(drive + "commercials/")
	trailers = get_videos_from_dir(drive + "trailers/")
	policy = get_videos_from_dir(drive + "policy/")
	countdowns = get_videos_from_dir(drive + "countdowns/")
	films = get_videos_from_dir(drive + "films/")
	trivia = get_videos_from_dir(drive + "trivia/")

def play_video(source, position):
	if source==None:
		return
	
	if position==None:
		position=0

	#os.system("killall -9 omxplayer");
	try:
		global next_video_to_play
		global last_video_played
		
		err_pos = -1.0
		
		#if next_video_to_play=='':
		
		next_video_to_play=''
		
		err_pos = 0.0

		print('Main video file:' + source)
		err_pos = 0.21
		#contents = urllib2.urlopen("http://127.0.0.1/?current_video=" + urllib.quote_plus(source)).read()
		err_pos = 0.23
		player = OMXPlayer(source, args=['--no-osd', '--blank'], dbus_name="omxplayer.player0")
		err_pos = 0.3
		player.set_aspect_mode('fill');
		err_pos = 0.32
		sleep(1)
		err_pos = 1.0
		player.pause()
		err_pos = 1.1
		strSubtitles = player.list_subtitles()
		if(strSubtitles):
			player.hide_subtitles()
		err_pos = 1.2
		if position!=0:
			player.set_position(position)
		err_pos = 1.22
		player.play()
		err_pos = 1.3
		lt = 0
		while (1):
			err_pos = 2.0
			try:
				position = player.position()
				print(position)
			except:
				break
				
			#check if it's a movie and if it is, save the position in case we need to resume the movie
			if source.find("/films/")>=0:
				set_resume(position, source)
			sleep(1)

		err_pos = 7.0
		player.hide_video()
		sleep(0.5)
		
	except Exception as e:
		#contents = urllib2.urlopen("http://127.0.0.1/?error=MAIN_" + str(err_pos) + "_" + urllib.quote_plus(str(e))).read()
		print("error main (" + str(err_pos) + ") " + str(e))
	
	err_pos = 7.1
	try:
		player.quit()
	except Exception as exx:
		#contents = urllib2.urlopen("http://127.0.0.1/?error=PLAYER_" + str(err_pos) + "_" + urllib.quote_plus(str(exx))).read()
		print("error player quit " + str(exx))
	
	return


preload_videos()

def get_movie_start():
	global drive
	
	if os.path.isfile(drive + 'movie.txt')!=True:
		return [0,None]

	movie_time = open(drive + 'movie.txt', 'r') 
	mlines = movie_time.readlines() 
	movie_time.close()

	ts = int(mlines[0].strip()) - (60*4*60)
	movie_file = mlines[1].strip()
	
	local_time = (time.time()-(60*4*60))
	time_diff = ts - local_time
	return [time_diff, movie_file]

def rem_play_file():
	if os.path.isfile(drive + 'play.txt')!=True:
		return None
	os.remove(drive + 'play.txt')
	
def get_play_file():
	if os.path.isfile(drive + 'play.txt')!=True:
		return None

	movie_time = open(drive + 'play.txt', 'r') 
	mlines = movie_time.readlines() 
	movie_time.close()
	print(mlines[0].strip())
	ts = float(mlines[0].strip())
	movie_file = mlines[1].strip()
	
	return [ts, movie_file]
	
def set_resume(position, movie_file):
	f = open(drive + 'resume.txt', "w")
	f.write(str(position) + "\n" + str(movie_file))
	f.close()
	
movie_state = -1

last_tricom = ''
last_trailer = ''

while(1):

	source = None

	movie_start = get_movie_start()
	
	if movie_state==-1:
		if movie_start[0]<0 or movie_start[0]>(10 * 60):
			print("Playing trivia/commercial")
			#movie hasn't been scheduled or is more than 10 minutes before show time
			#show trivia and commercials
			source = random.choice(trivia + commercials)

			#make sure we don't play the same video back to back
			while(source == last_tricom):
				source = random.choice(trivia + commercials)
			last_tricom = source
		else:
			print("Countdown Started!")
			#10 minutes to showtime, start countdown
			source = random.choice(countdowns)
			#also start the movie countdown
			movie_state = 0

	if movie_state==1:
		#play policy
		print("Playing the theater's policy")
		source = random.choice(policy)
	elif movie_state>1 and movie_state<6:
		#play a coming attractions roll
		#and then play trailers
		if movie_state==2:
			#play preview preroll
			print("Playing the previews preroll")
			source = random.choice(preview)
		else:
			#play 3 trailers
			print("Playing a trailer")
			source = random.choice(trailers)
			#make sure we don't play the same video back to back
			while(source == last_trailer):
				source = random.choice(trailers)
			last_trailer = source
		
	elif movie_state==6:
		#play feature
		print("Playing feature preroll")
		source = random.choice(feature)
	elif movie_state==7:
		#play sound
		print("Playing sound type")
		source = random.choice(sound)
	elif movie_state==8:
		#play movie
		print("Playing feature presentation")
		source = movie_start[1]

	position = 0
	
	gpf = get_play_file()
	if gpf!=None:
		#just play a movie
		position = gpf[0]
		source = gpf[1]
		rem_play_file()
		movie_state=-1
		
		

	print(source)	
	if source==None:
		print("ERROR NO SOURCE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	else:
		play_video(source, position)
	
	if movie_state>=0:
		#if movie_state == -1, it means nothing is scheduled or is more than 10 minutes before showtime
		#				>= 0, less than 10 minutes before show time (playing the countdown, trailers, etc)
		#				== 8, movie has played and it's now time to clean up and restart the whole process
		if movie_state==8:
			movie_state=-1
			last_tricom = ''
			last_trailer = ''
		else:
			movie_state = movie_state + 1
	
	sleep(1)





#play trivia and commercials until 10 minutes before show time
#at 10 minutes start countdown
#play preview
#play 2 or 3 trailers
#play policy
#play feature
#play sound
#play movie






#player = OMXPlayer(VIDEO_PATH, args='--aspect-mode fill', dbus_name='org.mpris.MediaPlayer1.omxplayer1')
#i=0
#while i<=100:
#	print(player.position())
#	sleep(1)
#	i = i + 1
#
#	now = datetime.now()
#	current_time = now.strftime("%H:%M:%S")
#	print("Current Time =", current_time)

#player.quit()