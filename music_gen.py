#!/usr/bin/python

import pysynth
from pysynth_b import *
import random
from random import randrange 
import copy
import sys
import os


#===KEYS===#    
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
   
#===Chord Progressions===#
PROG1 = [0,3,4,0]
PROG2 = [3,4]
PROG3 = [0,3,0,4]
PROG4 = [4,3,3,0]
CHORDPROGS = [PROG1,PROG2,PROG3,PROG4]

#==Rhythms===#
RHYTHM = [2, 2,  4, 4, 4, 8, 8]
FASTRHYTHM = [8]
THIRDRHYTHM = [3, 6, 9]
SEVENRHYTHM = [7]
IMPOSSRHYTHM = [32, 64]
 
#===Tempos===#   
TEMPO = [220, 140, 180, 100, 260]

#Staccato (how long/fluid individual notes are)
STACSPACE = [.1, .3, .5, .7]




##############GENERATORS###########################

class Song:
    SEED = "asdf"
    
    tempo = 220
    
    KEY = KEYS[0]
    BASEKEY = BASEKEYS[0]

    CHOSENPROG = -1
    CHOSENCHORUSPROG = -1    
    
    #The maximum distance allowed between two notes in note creation
    NOTESPACE = 2
    
    #===Measures===# 
    GOALMEASURES = 16
    MEASURE = 0

    #===Accidentals===#
    #State representing if the last note was an self.ACCIDENT
    ACCIDENT = False
    #The current number of self.ACCIDENTs
    ACCIDENT_NUM = 0
    #The total number of self.ACCIDENTs
    TOTAL_ACCIDENTS = 0

    STAC = .5
    
    #Constructor
    def __init__(self, seed):
        self.SEED = seed

        random.seed(self.SEED)
    
        keyIndex = randrange(len(KEYS) - 1)
        self.KEY = KEYS[keyIndex]
        self.BASEKEY = BASEKEYS[keyIndex]
    
        self.GOALMEASURES = randrange(8,16)
   
        self.NOTESPACE = 3 #TODO?? 
        self.TOTAL_ACCIDENTS = 0 #TODO

        self.tempo = random.choice(TEMPO)
        self.STAC = random.choice(STACSPACE)
        TOTAL_MEASURES = 0
        
        print "\n"
        print "Seed is " + str(seed)
        print "Song will be " + str(self.GOALMEASURES) +" measures long"
        print "Key is " + str(self.BASEKEY[0])
        print "Tempo is " + str(self.tempo)
        print "Staccato is " + str(self.STAC) + " out of 1.0"
        print "\n"

    #Returns a valid note from the key/index, based off of mod
    #NOTE This primarily makes sure that index wraps, 
    #     and we don't get an out of bounds
    def getNote(self, key, ind, mod):    
        ind = ind + mod
        
        if(ind < 0):
            ind = (len(key) - 1) + ind
        ind = ind % (len(key))
            
        return key[ind]

    #Takes a key,
    #Generates an appropriate note based off of last note
    #Can also add an self.ACCIDENTal note
    #if the last note was an self.ACCIDENTal then it will be resolved
    def generateSmartNxt(self, melody, key, mod):    
        resolved = False
        n = self.processAccidental(resolved)
        
        if(not(self.ACCIDENT or resolved)):
            #add the note
            refIndex = key.index(melody[len(melody)-1][0]) + \
             random.randrange(-self.NOTESPACE, self.NOTESPACE) 

            n = self.getNote(key, refIndex, mod)
        return n

    def arpeggiateNote(self, melody, key, mod):
        
        lastNoteIndex = key.index(melody[len(melody)-1][0])
        lastNoteIndex2 = key.index(melody[len(melody)-1][0])
    
        arpChoice = [2, 3] #TODO?
        num = random.choice(arpChoice)
        refIndex = lastNoteIndex
        if(lastNoteIndex - lastNoteIndex2 >= 0):
            refIndex = lastNoteIndex + num
        else:
            refIndex = lastNoteIndex - num
        n = self.getNote(self.BASEKEY, refIndex, mod)

        #arpegiate?
        return n


    #Adds an self.ACCIDENTal with low probability, if not, processes previous self.ACCIDENTal
    def processAccidental(self, resolved):
        if(self.ACCIDENT): #was the last note an self.ACCIDENTal?
            self.ACCIDENT = False
            #make sure the last note is in key
            resolved = True
            return(self.flattenNote(melody[len(melody)-1][0]))
                 
        #Add an self.ACCIDENTal note if we can
        else:
            #MAGIC 1
            magic1 = 42;
            #MAGIC 2
            magic2 = 8;

            #Low chance of returning a self.ACCIDENTal
            probabilityClause = (random.randrange(0, magic1) == magic2)

            allowedAccidents = ((not self.ACCIDENT) and self.ACCIDENT_NUM < self.TOTAL_ACCIDENTS)

            if(probabilityClause and allowedAccidents):
                n = random.choice(SCALE)
               
                #keep choosing notes until it is not in the scale
                while n in key:
                    n = random.choice(SCALE)

                self.ACCIDENT = True
                self.ACCIDENT_NUM = self.ACCIDENT_NUM + 1;
                return n

    #Generate a randombasic melody
    def generateMelody(self, seed, key, mod):
        
        melody = []
    
        random.seed(seed) #set seed
    
        while not(self.MEASURE == 1.0): #1 is full measure
            noteLen = self.getBeat(RHYTHM)
            self.MEASURE = self.MEASURE + float(1/float(noteLen))
            
            #TODO do something better?
            
            melody.append(
                (self.getNote(
                    key, 
                    random.randrange(0, len(key)-1), 
                    mod), 
                 noteLen))
    
        self.MEASURE = 0
        temp = copy.copy(melody)
        melody = self.appendPhrase(melody, temp)
    
        return melody

    #####################FULL GENERATORS#########################################
    
    #Takes a seed (used for random)
    #key, which has the key of the song
    #basic key, which is used for making the melody (no octaves)
    #mod, which modifies pitch based off of key
    
    #TODO make more modular??? like before??
    def generateSong(self, mod):
        random.seed(self.SEED)

        totalMeasures = 0 #TODO do we need a global?

        song = []
        melody = self.generateMelody(self.SEED, self.BASEKEY, mod)
        self.appendPhrase(song, copy.copy(melody))
        #melody is one measure, add + 1
        totalMeasures = totalMeasures + 2
    
        #TODO sections?
           #maybe add thirds/sevenths?
           #add some type of verse/chorus?
           
        #create the measures
        while totalMeasures < self.GOALMEASURES - 1:
    
            #TODO make something cool based off of goalmeasures? (like chorus)
    
            #gets a valid beat
            chorus = totalMeasures > self.GOALMEASURES / 2 and \
               totalMeasures < (self.GOALMEASURES / 2 + self.GOALMEASURES / 3)
    
            #adds this note (with valid beat) to song
            if(chorus):
                self.ACCIDENT = False
                beat = self.getBeat(FASTRHYTHM)
                song.append((self.arpeggiateNote(song, self.KEY, mod), beat))
            else:
                beat = self.getBeat(RHYTHM)
                song.append((self.generateSmartNxt(song, self.KEY, mod),beat))
            
            #adds beat to measure count
            self.MEASURE = self.MEASURE + float(1/float(beat))
            
            if(self.MEASURE == 1.0): #if the measure is complete
                self.MEASURE = 0 #reset
                totalMeasures = totalMeasures + 1 #add to total measures
    
        #End with melody with root note for closure
        song = self.appendPhrase(song, self.generateMelody(self.SEED, self.KEY, mod))
        song.append((self.KEY[0], 4))
        return song
    
    def generateChords(self, mod):
        totalMeasures=0

        #Make a random chord progression until we pick a chosen progression
        #This makes sure that all of the generate chords are called on the same proression
        if(self.CHOSENPROG == -1):
            random.seed(self.SEED)
            self.CHOSENPROG = random.randrange(0, len(CHORDPROGS)-1)
            self.CHOSENCHORUSPROG = random.randrange(0, len(CHORDPROGS)-1)
            while self.CHOSENCHORUSPROG == self.CHOSENPROG:
                self.CHOSENCHORUSPROG = random.randrange(0, len(CHORDPROGS)-1)

        
        random.seed(self.SEED)
        song = []
        chorus = []
        totalMeasures = 0
        progression = CHORDPROGS[self.CHOSENPROG]
        chorusProgression = CHORDPROGS[self.CHOSENCHORUSPROG]
       
        while totalMeasures < self.GOALMEASURES + 1:

            chorus = totalMeasures > self.GOALMEASURES / 2 and \
               totalMeasures < (self.GOALMEASURES / 2 + self.GOALMEASURES / 3)

            prog = chorusProgression if chorus else progression

            for x in range(0, len(prog)):
                chordName = self.cleanNote(self.KEY[prog[x]]) # note base for chord
                chordKey = KEYS[KEYMAP.index(chordName)] # chord key
                if (len(prog) == 4):
                    song.append((self.getNote(chordKey, 0, mod), 4)) #quaternote
                else:
                    song.append((self.getNote(chordKey, 0, mod), 2)) #halfnote 
    
            totalMeasures = totalMeasures + 1
        return song

    #generates a copy of the melody with the last note changed
    def generateModMelody(self, melody, key, mod) :
        #copy melody so that original isn't affected
        oldMelody = copy.copy(melody) 

        #changes the last note in melody
        refIndex = key.index(melody[len(melody)-1][0]) + \
             random.randrange(-self.NOTESPACE, self.NOTESPACE) 

        oldMelody[len(oldMelody)-1] = (self.getNote(key, refIndex, mod), melody[len(melody)-1][1])
        return oldMelody

    ################HELPER FUNCTIONS#####################
    #Returns a rhythm that sticks to the time signiture
    #Rhythm is one of (FASTRHYTHM, RHYTHM, etc.)
    def getBeat(self, rhythmSpace):
        #grab a random beat
        noteLen = random.choice(rhythmSpace)
        
        while(not self.beatCheck(noteLen)):
            noteLen = random.choice(rhythmSpace)
        return noteLen
    
    #verifies if a beat will fit in current measure
    #(ex if we have 4 beats per measure, and we are currently at 3, we would not add 2 more)
    def beatCheck(self, beat):
        if(self.MEASURE + float(1/float(beat)) > 1.0):
            return False
        else:
            return True
    
    
    
    #Returns a valid note in key, based off of current scale, resolves self.ACCIDENT
    #This is the note index, 1 halfstep down from current
    def flattenNote(self, note):
        x = SCALE.index(note)
        if (x == 0):
            return SCALE[len(SCALE)-1]
        else:
            return SCALE[x-1]
    
    #appends p2 to p1
    def appendPhrase(self, p1, p2):
        for x in range (len(p2)):
            p1.append(p2[x])
    
        return p1
    
    #TODO WAT
    #cleans note
    #will be needed in the future
    def cleanNote(self, note):
        return note[0]

def main():
        
    #===PROCESS INPUT===#
    song = Song(sys.argv[1])

    #creates the song
    make_wav(song.generateSong(0), 
        song.tempo,
        transpose=0, 
        fn="GenSongs/song.wav", 
        leg_stac = song.STAC)

    make_wav(song.generateSong(2), 
        song.tempo,
        transpose=0, 
        fn="GenSongs/harmony.wav", 
        leg_stac = song.STAC)
    #creates first section of chord (mod 0, with same seed)
    #mod is used to create chord values, and we later mix them
    
    make_wav(song.generateChords(0), song.tempo, \
        transpose=0, fn="GenSongs/chord1.wav", leg_stac = song.STAC)
    make_wav(song.generateChords(2), song.tempo, \
        transpose=0, fn="GenSongs/chord2.wav", leg_stac = song.STAC)
    make_wav(song.generateChords(4), song.tempo, \
        transpose=0, fn="GenSongs/chord3.wav", leg_stac = song.STAC)
    
    mix_files("GenSongs/chord1.wav", "GenSongs/chord2.wav", "GenSongs/chord12.wav", chann = 1)
    mix_files("GenSongs/chord12.wav", "GenSongs/chord3.wav", "GenSongs/chords.wav", chann = 1)
    mix_files("GenSongs/chords.wav", "GenSongs/song.wav", "GenSongs/noharm.wav", chann = 1)
    
    #create the final song
    mix_files("GenSongs/noharm.wav", 
        "GenSongs/harmony.wav", 
        "GenSongs/" + str(song.SEED) + ".wav", 
        chann = 1)

    #cleanup files
    os.remove("GenSongs/chord1.wav");
    os.remove("GenSongs/chord2.wav");
    os.remove("GenSongs/chord3.wav");
    os.remove("GenSongs/chords.wav");
    os.remove("GenSongs/chord12.wav");
    os.remove("GenSongs/song.wav");
    os.remove("GenSongs/harmony.wav");
    os.remove("GenSongs/noharm.wav");

#Execute the program
main()

