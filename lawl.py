#!/usr/bin/python

import pysynth
from pysynth_b import *
import random
import copy


#documentation is on
#mdoege.github.io/PySynth/


#Possible values
NOTES = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

CMajorWeighted = ['a', 'a', 'b', 'c', 'c', 'd', 'e', 'e', 'f', 'f', 'g', 'a3', 'a3', 'c3', 'c3', 'e3', 'e3']
CMinorBasic = ['a', 'b', 'db', 'd', 'eb', 'e', 'g']
CMinor = ['a3', 'b3', 'db3', 'd3', 'eb3', 'e3', 'g3','a', 'b', 'db', 'd', 'eb', 'e', 'g','a4', 'b4', 'db4', 'd4', 'eb4', 'e4', 'g4']

ARPG = ['a', 'c', 'e', 'f']

RHYTHM = [2, 2,  4, 4, 4, 8, 8, -2]
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

def appendPhrase(p1, p2):
	for x in range (len(p2)):
		p1.append(p2[x])

	return p1


#Generate basic melody
def generateMelody(seed, key, mod):
	
	melody = []

	random.seed(seed)

	for x in range(4):
		melody.append(
			(
				key[
				getNote(
					random.randrange(0, len(key)-1)
					, key, mod)], random.choice(RHYTHM)))

	temp = copy.copy(melody)
	melody = appendPhrase(melody, temp)

	return melody

#Wat doe s
def generateComposite(melody, beat):
	
	for x in range (random.randrange(8, 24)):
		melody.append(random.choice(melody))
		if(x % (random.randrange(2, 4)) == 0):
			melody.append((random.choice(CMinor), random.choice(beat)))	

	return melody

def generateSmartNxt(melody, key, beat, mod):
	if(random.randrange(0, 100) % 3 != 0):
		x = getNote(key.index(melody[len(melody)-1][0]) + random.randrange(1, 3), key, mod)
		
	else:
		x = getNote(key.index(melody[len(melody)-1][0]) - random.randrange(1, 3), key, mod)
		
	melody.append((key[x], random.choice(beat)))
	return melody


def generateSmart(SEED, mod, length):
	melody = generateMelody(SEED, CMinorBasic, mod)
	for x in range (length/4):
		melody = generateSmartNxt(melody, CMinor, RHYTHM, mod)
	melody = generateComposite(generateMelody(SEED, CMinorBasic, mod), RHYTHM)
	for x in range (length/4):
		melody = generateSmartNxt(melody, CMinor, RHYTHM, mod)
	for x in range (length/2):
		melody = generateSmartNxt(melody, CMinor, FASTRHYTHM, mod)

	melody = appendPhrase(melody, generateMelody(SEED, CMinorBasic, mod))
	melody.append(('r', 1))
	melody.append(('r', 1))
	melody.append(('r', 1))
	melody = appendPhrase(melody, generateMelody(SEED, CMinorBasic, mod))
	return melody


#Expand on basic melody
#Add compliment? Harmony?

#Develop 'chorus' based off of melody

#Add transition?

def getNote(ind, key, mod):
	ind = ind + mod
	if(ind < 0):
		ind = (len(key) - 1) + ind

	if(ind > (len(key) - 1)):
		ind = ind % (len(key) - 1)
		if(ind != 0):
			ind = ind - 1
	return ind


def generateSong(SEED):
	melody = generateMelody(SEED)
	comp = generateComposite(generateMelody(SEED), RHYTHM)
	comp2 = generateComposite(comp, RHYTHM)
	comp3 = generateComposite(generateMelody(SEED), FASTRHYTHM)
	song = appendPhrase(melody, comp2)
	song = appendPhrase(song, generateMelody(SEED))
	song = appendPhrase(song, comp3)
	song = appendPhrase(song, generateMelody(SEED))

	return song


SEED = "yolo"
print SEED
STAC = .5
KEY = c
def chords(mod):
	song = []
	for x in range(4):
		n = g[getNote(0, g, mod)]
		if (mod == 2):
			n = flattenNote(n)
		song.append((n ,4))

	for x in range(4):
		n = d[getNote(0, d, mod)]
		if (mod == 2):
			n = flattenNote(n)
		song.append((n ,4))

	for x in range(4):
		n = a[getNote(0, a, mod)]
		if (mod == 2):
			n = flattenNote(n)
		song.append((n ,4))

	for x in range(4):
		n = c[getNote(0, c, mod)]
		if (mod == 2):
			n = flattenNote(n)
		song.append((n,4))

	return song


def flattenNote(note):
	x = SCALE.index(note)
	if (x == 0):
		return SCALE[len(SCALE)-1]
	else:
		return SCALE[x-1]


make_wav(chords(0), 220, transpose=0, fn="Songs/chord1.wav", leg_stac = STAC)
make_wav(chords(2), 220, transpose=0, fn="Songs/chord2.wav", leg_stac = STAC)
make_wav(chords(4), 220, transpose=0, fn="Songs/chord3.wav", leg_stac = STAC)
make_wav(generateSmart(SEED, 0, 16), 220, transpose=0, fn="Songs/melody.wav", leg_stac = STAC)

mix_files("Songs/chord1.wav", "Songs/chord2.wav", "Songs/chord12.wav", chann = 1)
mix_files("Songs/chord12.wav", "Songs/chord3.wav", "Songs/chords.wav", chann = 1)
mix_files("Songs/chords.wav", "Songs/melody.wav", "Songs/topkek.wav", chann = 1)
#mix_files("Songs/topkek0.wav", "Songs/topkek3.wav", "Songs/topkek.wav", chann = 1)


#make_wav(generateSmart(SEED, 0, 60), 220, transpose=1, fn="Songs/topkek1.wav", leg_stac = STAC)
#make_wav(generateSmart(SEED, 2), 220, transpose=1, fn="Songs/topkek2.wav", leg_stac = STAC)
#make_wav(generateSmart(SEED, 4), 220, transpose=1, fn="Songs/topkek4.wav", leg_stac = STAC)
#leg_stac is staccato
#make_wav(generateSong("yolo"), 220, transpose=0, fn="Songs/topkek1.wav", leg_stac = random.random())


#make_wav(generateSong("swag"), 220, transpose=0, fn="Songs/topkek2.wav", leg_stac = random.random())

#mix_files("Songs/topkek1.wav", "Songs/topkek2.wav", "Songs/topkek3.wav")
#mix_files("Songs/topkek1.wav", "Songs/topkek4.wav", "Songs/topkek0.wav")
#mix_files("Songs/topkek0.wav", "Songs/topkek3.wav", "Songs/topkek.wav")


print "hello world"
