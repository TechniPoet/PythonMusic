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



NOTESPACE = 9

GOALMEASURES = 17
TOTALMEASURES = 0
MEASURE = 0
accident = False

################HELPER FUNCTIONS#####################

def getBeat(rhythmSpace):
	noteLen = random.choice(rhythmSpace)
	while(not beatCheck(noteLen)):
		noteLen = random.choice(rhythmSpace)
	return noteLen

def beatCheck(beat):
	if(MEASURE + float(1/float(beat)) > 1.0):
		return False
	else:
		return True

def getNote(ind, key, mod):
	ind = ind + mod
	if(ind < 0):
		ind = (len(key) - 1) + ind

	if(ind > (len(key) - 1)):
		ind = ind % (len(key) - 1)
		if(ind != 0):
			ind = ind - 1
	return ind

def flattenNote(note):
	x = SCALE.index(note)
	if (x == 0):
		return SCALE[len(SCALE)-1]
	else:
		return SCALE[x-1]

def appendPhrase(p1, p2):
	for x in range (len(p2)):
		p1.append(p2[x])

	return p1


##############GENERATORS###########################

#Generate basic melody
def generateMelody(seed, key, mod):
	global MEASURE
	melody = []

	random.seed(seed)


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




def generateSmartNxt(melody, key, beat, mod):
	global accident

	if(accident):
		accident = False
		x = flattenNote(melody[len(melody)-1][0]) 

	elif(random.randrange(0, 20) == 15 and not accident):
		print "accident"
		accident = True
		x = random.choice(SCALE)
		while x in key:
			x = random.choice(SCALE)
		print x

	elif(random.randrange(0, 100) % 2 != 0):
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

SEED = "fun"
print SEED
STAC = .5
KEY = c
BASEKEY = cBasic


make_wav(generateSong(SEED, KEY, BASEKEY, 0), 220, transpose=0, fn="GenSongs/test.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  0), 220, transpose=0, fn="GenSongs/chord1.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  2), 220, transpose=0, fn="GenSongs/chord2.wav", leg_stac = STAC)
make_wav(generateChords(SEED, KEY,  4), 220, transpose=0, fn="GenSongs/chord3.wav", leg_stac = STAC)

mix_files("GenSongs/chord1.wav", "GenSongs/chord2.wav", "GenSongs/chord12.wav", chann = 1)
mix_files("GenSongs/chord12.wav", "GenSongs/chord3.wav", "GenSongs/chords.wav", chann = 1)
mix_files("GenSongs/chords.wav", "GenSongs/test.wav", "GenSongs/fullSong.wav", chann = 1)