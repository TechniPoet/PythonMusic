#!/usr/bin/python

import pysynth
from pysynth_b import *
import random
import copy


#documentation is on
#mdoege.github.io/PySynth/


#Possible values
NOTES = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

CMajor = ['a', 'a', 'b', 'c', 'c', 'd', 'e', 'e', 'f', 'f', 'g', 'a3', 'a3', 'c3', 'c3', 'e3', 'e3']
CMinor = ['a4', 'b4', 'db4', 'd4', 'eb4', 'e4', 'g4']

ARPG = ['a', 'c', 'e', 'f']

RHYTHM = [2, 2,  4, 4, 4, 8, 8, -2]
FASTRHYTHM = [8, 16]
THIRDRHYTHM = [3, 6, 9]
SEVENRHYTHM = [7]
IMPOSSRHYTHM = [32, 64]


TEMPO = [220, 160, 140, 180]




def appendPhrase(p1, p2):
	for x in range (len(p2)):
		p1.append(p2[x])

	return p1


#Generate basic melody
def generateMelody(seed):
	
	melody = []

	random.seed(seed)

	for x in range(4):
		melody.append((random.choice(CMajor), random.choice(RHYTHM)))

	temp = copy.copy(melody)
	melody = appendPhrase(melody, temp)

	lel = [('c', 4), ('c*', 4), 
  	('e', 4), ('g', 4), ('g*', 2), 
  	('g5', 4), ('g5*', 4), ('r', 4), 
  	('e5', 4), ('e5*', 4), ('r', 4),
  	('c', 4), ('c*', 4), 
 	('e', 4), ('g', 4), ('g*', 2), 
  	('g5', 4), ('g5*', 4), ('r', 4), 
  	('f5', 4), ('f5*', 4)]





	return melody

#Wat doe s
def generateComposite(melody, beat):
	
	for x in range (random.randrange(8, 24)):
		melody.append(random.choice(melody))
		if(x % (random.randrange(2, 4)) == 0):
			melody.append((random.choice(CMajor), random.choice(beat)))	

	return melody



#Expand on basic melody
#Add compliment? Harmony?

#Develop 'chorus' based off of melody

#Add transition?





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





#leg_stac is staccato
make_wav(generateSong("yolo"), 220, transpose=0, fn="Songs/topkek1.wav", leg_stac = random.random())


make_wav(generateSong("swag"), 220, transpose=0, fn="Songs/topkek2.wav", leg_stac = random.random())

mix_files("Songs/topkek1.wav", "Songs/topkek2.wav", "Songs/topkek.wav")

print "hello world"
