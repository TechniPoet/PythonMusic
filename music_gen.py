#!/usr/bin/python

import pysynth
from pysynth_b import *
import random
import copy

RHYTHM = [2, 2,  4, 4, 4, 8, 8]
FASTRHYTHM = [8, 16]
THIRDRHYTHM = [3, 6, 9]
SEVENRHYTHM = [7]
IMPOSSRHYTHM = [32, 64]

TEMPO = [220, 160, 140, 180]

SCALE = ['a3', 'a#3', 'b3', 'c3', 'c#3', 'd3', 'd#3', 'e3', 'f3', 'f#3', 'g3', 'g#3',
	'a', 'a#', 'b', 'c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#',
	'a5', 'a#5', 'b5', 'c5', 'c#5', 'd5', 'd#5', 'e5', 'f5', 'f#5', 'g5', 'g#5',]

c = ['c3', 'd3', 'e3', 'f3', 'g3', 'a3', 'b3',
	'c', 'd', 'e', 'f', 'g', 'a', 'b',
	'c5', 'd5', 'e5', 'f5', 'g5', 'a5', 'b5']

cBasic = ['c', 'd', 'e', 'f', 'g', 'a', 'b']

g = ['g3', 'a3', 'b3', 'c3', 'd3', 'e3', 'f#3',
	'g', 'a', 'b', 'c', 'd', 'e', 'f#',
	'g5', 'a5', 'b5', 'c5', 'd5', 'e5', 'f#5']

gBasic = ['g', 'a', 'b', 'c', 'd', 'e', 'f#']

d = ['d3', 'e3', 'f#3', 'g3', 'a3', 'b3', 'c#3',
	'd', 'e', 'f#', 'g', 'a', 'b', 'c#',
	'd5', 'e5', 'f#5', 'g5', 'a5', 'b5', 'c#5']
dBasic = ['d', 'e', 'f#', 'g', 'a', 'b', 'c#']

a = ['a3', 'b3', 'c#3','d3', 'e3', 'f#3', 'g#3',
	'a', 'b', 'c#','d', 'e', 'f#', 'g#',
	'a5', 'b5', 'c#5','d5', 'e5', 'f#5', 'g#5']
aBasic = ['a', 'b', 'c#','d', 'e', 'f#', 'g#']

e = ['e3', 'f#3', 'g#3', 'a3', 'b3', 'c#3','d#3',
	'e', 'f#', 'g#', 'a', 'b', 'c#','d#',
	'e5', 'f#5', 'g#5', 'a5', 'b5', 'c#5','d#5']
eBasic = ['e', 'f#', 'g#', 'a', 'b', 'c#','d#']

b = ['b3', 'c#3','d3', 'e3', 'f#3', 'g#3', 'a#3',
	'b', 'c#','d', 'e', 'f#', 'g#', 'a#',
	'b5', 'c#5','d5', 'e5', 'f#5', 'g#5', 'a#5']
bBasic = ['b', 'c#','d', 'e', 'f#', 'g#', 'a#']

KEYMAP = ['a', 'b', 'c', 'd', 'e', 'g']
KEYS = [a, b, c, d, e, g]

PROG1 = [0,3,4,0]
PROG2 = [0,3]
PROG3 = [0,3,0,4]
CHORDPROGS = [PROG1,PROG2,PROG3]
CHOSENPROG = -1

NOTESPACE = 4

GOALMEASURES = 15
TOTALMEASURES = 0
MEASURE = 0
accident = False
ACCIDENT_NUM = 0

SEED = "CLASS TIME BUTT"
print SEED
STAC = .5
KEY = c
BASEKEY = cBasic

################HELPER FUNCTIONS#####################
#Returns a rhythm that sticks to the time signiture
def getBeat(rhythmSpace):
	noteLen = random.choice(rhythmSpace)
	while(not beatCheck(noteLen)):
		noteLen = random.choice(rhythmSpace)
	return noteLen

#returns whether or not the given rhythm not will fit signiture
def beatCheck(beat):
	if(MEASURE + float(1/float(beat)) > 1.0):
		return False
	else:
		return True

#Returns the note index in the key based on 
#the mod value 
def getNote(ind, key, mod):
	ind = ind + mod
	if(ind < 0):
		ind = (len(key) - 1) + ind

	if(ind > (len(key) - 1)):
		ind = ind % (len(key) - 1)
		if(ind != 0):
			ind = ind - 1
	return ind

#Returns the note index 1 halfstep down from given index
def flattenNote(note):
	x = SCALE.index(note)
	if (x == 0):
		return SCALE[len(SCALE)-1]
	else:
		return SCALE[x-1]

#appends p2 to p1
def appendPhrase(p1, p2):
	for x in range (len(p2)):
		p1.append(p2[x])

	return p1


##############GENERATORS###########################

#Generate a randombasic melody
def generateMelody(seed, key, mod):
	global MEASURE
	melody = []

	random.seed(seed) #set seed

	while not(MEASURE == 1.0):
		noteLen = getBeat(RHYTHM)
		MEASURE = MEASURE + float(1/float(noteLen))
		melody.append(
			(
				key[
				getNote(
					random.randrange(0, len(key)-1)
					, key, mod)], noteLen))
		print noteLen
		
	MEASURE = 0

	temp = copy.copy(melody)
	melody = appendPhrase(melody, temp)

	return melody



#adds the next note to the melody based on NOTESPACE variation
#small chance of adding an accidental
#if the last note was an accidental then it will be resolved
def generateSmartNxt(melody, key, beat, mod):
	global accident
	global ACCIDENT_NUM
	if(accident): #was the last note an accidental?
		accident = False
		x = flattenNote(melody[len(melody)-1][0]) 

	elif(random.randrange(0, 40) == 15 and not accident and ACCIDENT_NUM < 1):
		#make an accidental note
		print "accident"
		accident = True
		ACCIDENT_NUM = ACCIDENT_NUM + 1;
		x = random.choice(SCALE)
		while x in key:
			x = random.choice(SCALE)
		print x

	elif(random.randrange(0, 100) % 2 != 0): #add random note in NOTESPACE range
		x = key[getNote(key.index(melody[len(melody)-1][0]) + random.randrange(1, NOTESPACE), key, mod)]
		
	else:
		x = key[getNote(key.index(melody[len(melody)-1][0]) - random.randrange(1, NOTESPACE), key, mod)]
		
	melody.append((x, beat))
	return melody


#####################FULL GENERATORS#########################################
def generateSong(seed, key, basicKey, mod):
	global TOTALMEASURES
	global MEASURE
	global GOALMEASURES

	melody = generateMelody(SEED, key, mod)
	TOTALMEASURES = TOTALMEASURES + 1

	while TOTALMEASURES < GOALMEASURES - 1:
		beat = getBeat(RHYTHM)
		melody = generateSmartNxt(melody, key, beat, mod)
		MEASURE = MEASURE + float(1/float(beat))
		if(MEASURE == 1.0):
			MEASURE = 0
			TOTALMEASURES = TOTALMEASURES + 1

	#End with melody with root note for closure
	melody = appendPhrase(melody, generateMelody(SEED, key, mod))
	melody.append((key[0], 4))
	return melody

def generateChords(seed, key, mod):
	global TOTALMEASURES
	global MEASURE
	global GOALMEASURES
	global CHOSENPROG

	if(CHOSENPROG == -1):
		
	
	random.seed(seed)
	song = []
	TOTALMEASURES = 0

	while TOTALMEASURES < GOALMEASURES + 1:
		n = g[getNote(0, g, mod)]
		'''
		if (mod == 2):
			n = flattenNote(n)
			'''
		song.append((n, 4))

		n = c[getNote(0, c, mod)]
		'''
		if (mod == 2):
			n = flattenNote(n)
			'''
		song.append((n ,4))

		n = g[getNote(0, g, mod)]
		'''
		if (mod == 2):
			n = flattenNote(n)
			'''
		song.append((n ,4))

		n = d[getNote(0, d, mod)]
		'''
		if (mod == 2):
			n = flattenNote(n)
			'''
		song.append((n,4))

		TOTALMEASURES = TOTALMEASURES + 1

	return song


#TODO - Make generateChords use different progressions




make_wav(generateSong(SEED, KEY, BASEKEY, 0), 220, transpose=0, fn="GenSongs/test.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  0), 220, transpose=0, fn="GenSongs/chord1.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  2), 220, transpose=0, fn="GenSongs/chord2.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  4), 220, transpose=0, fn="GenSongs/chord3.wav", leg_stac = STAC)

mix_files("GenSongs/chord1.wav", "GenSongs/chord2.wav", "GenSongs/chord12.wav", chann = 1)
mix_files("GenSongs/chord12.wav", "GenSongs/chord3.wav", "GenSongs/chords.wav", chann = 1)
mix_files("GenSongs/chords.wav", "GenSongs/test.wav", "GenSongs/fullSong.wav", chann = 1)