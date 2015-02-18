#!/usr/bin/python

import pysynth
from pysynth_b import *
import random
import copy
import sys
import os

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

f = ['f3', 'g3', 'a3', 'b3', 'c3', 'd3', 'e3',
     'f', 'g', 'a', 'b', 'c', 'd', 'e',
     'f5', 'g5', 'a5', 'b5', 'c5', 'd5', 'e5']
fBasic = ['f', 'g', 'a', 'b', 'c', 'd', 'e']

KEYMAP = ['a', 'b', 'c', 'd', 'e', 'g', 'f']
KEYS = [a, b, c, d, e, g, f]
BASEKEYS = [aBasic, bBasic, cBasic, dBasic, eBasic, dBasic, eBasic, gBasic, fBasic]

PROG1 = [0,3,4,0]
PROG2 = [0,3]
PROG3 = [0,3,0,4]
CHORDPROGS = [PROG1,PROG2,PROG3,PROG3]
CHOSENPROG = -1

NOTESPACE = 8

GOALMEASURES = 15
TOTALMEASURES = 0
MEASURE = 0
accident = False
ACCIDENT_NUM = 0
TOTAL_ACCIDENTS = 0

SEED = "test!"
STAC = .5
KEY = c
BASEKEY = cBasic



################HELPER FUNCTIONS#####################
#Returns a rhythm that sticks to the time signiture
#Rhythm is one of (FASTRHYTHM, RHYTHM, etc.)
def getBeat(rhythmSpace):
    #grab a random beat
    noteLen = random.choice(rhythmSpace)
    
    while(not beatCheck(noteLen)):
        noteLen = random.choice(rhythmSpace)
    return noteLen

#verifies if a beat will fit in current measure
#(ex if we have 4 beats per measure, and we are currently at 3, we would not add 2 more)
def beatCheck(beat):
    if(MEASURE + float(1/float(beat)) > 1.0):
        return False
    else:
        return True

#Returns a valid note from the key/index, based off of mod
def getNote(ind, key, mod):    
    #NOTE
    #we are essentially just wrapping this to make sure
    #that the index does not go out of range of the array
    #Don't worry about the specifics

    ind = ind + mod
    
    if(ind < 0):
        ind = (len(key) - 1) + ind

    if(ind > (len(key) - 1)):
        ind = ind % (len(key) - 1)
        if(ind != 0):
            ind = ind - 1
    
    return ind

#Returns a valid note in key, based off of current scale, resolves accident
#This is the note index, 1 halfstep down from current
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

#TODO WAT
#cleans note
#will be needed in the future
def cleanNote(note):
    return note[0]

##############GENERATORS###########################

#Generate a randombasic melody
def generateMelody(seed, key, mod):
    global MEASURE
    melody = []

    random.seed(seed) #set seed

    while not(MEASURE == 1.0): #1 is full measure
        noteLen = getBeat(RHYTHM)
        MEASURE = MEASURE + float(1/float(noteLen))

        #TODO do something better?
        
        melody.append(
            (key[getNote(random.randrange(0, len(key)-1),\
                 key,\
                 mod)], \
             noteLen))
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
    global TOTAL_ACCIDENTS
     #MAGIC 1
    magic1 = 40;
    #MAGIC 2
    magic2 = 15;

    if(accident): #was the last note an accidental?
        accident = False
        #make sure this note is in key
        x = flattenNote(melody[len(melody)-1][0])
   
    #if the probability is within magic range,
    #and we can allow more accidents,
    #we want to add an accidental note
    elif(random.randrange(0, magic1) == magic2 and \
        not accident and ACCIDENT_NUM < TOTAL_ACCIDENTS):
        
        #make an accidental note
        #print "accident"
        accident = True
        ACCIDENT_NUM = ACCIDENT_NUM + 1;
        x = random.choice(SCALE)

        #keep choosing notes until it is not in the scale
        while x in key:
            x = random.choice(SCALE)
        #print x

    #TODO cleanup?
    #TODO also maybe make this not random?
    #These last two clauses add a random note, up or down 
    elif(random.randrange(0, 100) % 2 != 0): #add random note in NOTESPACE range
        x = key[getNote(key.index(melody[len(melody)-1][0]) + \
            random.randrange(1, NOTESPACE), key, mod)]
    else:
        x = key[getNote(key.index(melody[len(melody)-1][0]) - \
            random.randrange(1, NOTESPACE), key, mod)]
        
    melody.append((x, beat))
    return melody


#####################FULL GENERATORS#########################################

#Takes a seed (used for random)
#key, which has the key of the song
#basic key, which is used for making the melody (no octaves)
#mod, which modifies pitch based off of key

#TODO make more modular??? like before??
def generateSong(seed, key, basicKey, mod):
    global TOTALMEASURES
    global MEASURE
    global GOALMEASURES

    melody = generateMelody(SEED, key, mod)
    #melody is one measure, add + 1
    TOTALMEASURES = TOTALMEASURES + 1


    #TODO sections?
       #maybe add thirds/sevenths?
       #add some type of verse/chorus?
       

    #create the measures
    while TOTALMEASURES < GOALMEASURES - 1:
        

        #TODO make something cool based off of goalmeasures? (like chorus)

        #gets a valid beat
        beat = getBeat(RHYTHM)
        #adds this note (with valid beat) to song
        melody = generateSmartNxt(melody, key, beat, mod)
        
        #adds beat to measure count
        MEASURE = MEASURE + float(1/float(beat))
        
        if(MEASURE == 1.0): #if the measure is complete
            MEASURE = 0 #reset
            TOTALMEASURES = TOTALMEASURES + 1 #add to total measures

    #End with melody with root note for closure
    melody = appendPhrase(melody, generateMelody(SEED, key, mod))
    melody.append((key[0], 4))
    return melody



#TODO revise revise revise
def generateChords(seed, key, mod):
    global TOTALMEASURES
    global MEASURE
    global GOALMEASURES
    global CHOSENPROG
    global CHORDPROGS
    global KEYS
    global KEYMAP

    #Make a random chord progression until we pick a chosen progression
    #This makes sure that all of the generate chords are called on the same proression
    if(CHOSENPROG == -1):
        random.seed(seed)
        CHOSENPROG = random.randrange(0, len(CHORDPROGS)-1)
    
    random.seed(seed)
    song = []
    TOTALMEASURES = 0
    progression = CHORDPROGS[CHOSENPROG]
   
    #print progression
    #print "progression"

    for x in range(0, len(progression)):
        # note base for chord
        chordName = cleanNote(key[progression[x]])
        print str(progression[x])
        # chord key
        chordKey = KEYS[KEYMAP.index(chordName)] 
        print chordKey[getNote(0, chordKey, mod)]
        
        #TODO dafuq, REVISE lawl
        if (len(progression) == 4):
            
            song.append((chordKey[getNote(0, chordKey, mod)], 4)) #quarternote 
        else:
            song.append((chordKey[getNote(0, chordKey, mod)], 2)) #halfnote

    while TOTALMEASURES < GOALMEASURES + 1:
        for x in range(0, len(progression)):
            chordName = cleanNote(key[progression[x]]) # note base for chord
            chordKey = KEYS[KEYMAP.index(chordName)] # chord key
            if (len(progression) == 4):
                song.append((chordKey[getNote(0, chordKey, mod)], 4)) #quaternote
            else:
                song.append((chordKey[getNote(0, chordKey, mod)], 2)) #halfnote 

        TOTALMEASURES = TOTALMEASURES + 1

    return song


#TODO - Make generateChords use different progressions

def main():
    global SEED
    global KEY
    global BASEKEYS
    global KEYMAP
    global KEYS
    global GOALMEASURES
    global TOTAL_ACCIDENTS
    global NOTESPACE

    #grab arguments
    SEED = sys.argv[1]
    print "seed is " + str(sys.argv[1])
    KEY = KEYS[KEYMAP.index(str(sys.argv[2]).lower())]
    print "Key is " + str(sys.argv[2]).lower()
    BASEKEY = BASEKEYS[KEYMAP.index(str(sys.argv[2]).lower())]
    GOALMEASURES = int(sys.argv[3])
    print "Song will be " + str(GOALMEASURES) +" measures long"
    NOTESPACE = int(sys.argv[4])

    #(check to see if accidents is an input value)
    try:
        TOTAL_ACCIDENTS = int(sys.argv[5])
    except:
        TOTAL_ACCIDENTS = 0;


    #creates the song
    make_wav(generateSong(SEED, KEY, BASEKEY, 0), 220, \
        transpose=0, fn="GenSongs/test.wav", leg_stac = STAC)

    #creates first section of chord (mod 0, with same seed)
    #mod is used to create chord values, and we later mix them
    make_wav(generateChords(SEED, KEY,  0), 220, \
        transpose=0, fn="GenSongs/chord1.wav", leg_stac = STAC)
    make_wav(generateChords(SEED, KEY,  2), 220, \
        transpose=0, fn="GenSongs/chord2.wav", leg_stac = STAC)
    make_wav(generateChords(SEED, KEY,  4), 220, \
        transpose=0, fn="GenSongs/chord3.wav", leg_stac = STAC)
    
    mix_files("GenSongs/chord1.wav", "GenSongs/chord2.wav", "GenSongs/chord12.wav", chann = 1)
    mix_files("GenSongs/chord12.wav", "GenSongs/chord3.wav", "GenSongs/chords.wav", chann = 1)
    mix_files("GenSongs/chords.wav", "GenSongs/test.wav", "GenSongs/fullSong.wav", chann = 1)
    
    #cleanup files
    os.remove("GenSongs/chord1.wav");
    os.remove("GenSongs/chord2.wav");
    os.remove("GenSongs/chord3.wav");
    os.remove("GenSongs/chords.wav");
    os.remove("GenSongs/chord12.wav");
    os.remove("GenSongs/test.wav");
main()


#TODO deliverables?
#song structure?
#melody/chorus? based off of measure count?
#harmony with melody?



