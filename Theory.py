#!/usr/bin/python

#Major keys

SHARP_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLAT_NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
MAJOR_STEPS = [2, 2, 1, 2, 2, 2, 1]
MINOR_STEPS = [2, 1, 2, 2, 1, 2, 2]

def letterShift(note):
    pos = SHARP_NOTES.index(note)
    return SHARP_NOTES[pos:] + SHARP_NOTES[:pos]

def majorAlgo(note):
    seedList  = letterShift(note)
    newList = []
    newString = ''
    for i in range(0, 5, 2):
        newList.append(seedList[i])
    for i in range(5, 12, 2):
        newList.append(seedList [i])
    for i in newList:
        newString += i + ' ' 
    return newString

def letterShift(notes, letter):
    pos = notes.index(letter)
    return notes[pos:] + notes[:pos]

def major():
    return MAJOR_STEPS

def minor():
    return MINOR_STEPS

def litmus(notes):
    newStr = ''
    for i in notes:
            newStr += i.replace('#', '')
    return len(set(notes)) == len(set(newStr))

def createList(seedList, key):
    indice = 0
    returnList = []
    for i in key:
            returnList.append(seedList[indice])
            indice += i
    return returnList

def toFlat(seedList):
    returnList = ['Ab' if note=='G#' else note for note in seedList]
    returnList = ['Bb' if note=='A#' else note for note in returnList]
    returnList = ['Cb' if note=='B#' else note for note in returnList]
    returnList = ['Db' if note=='C#' else note for note in returnList]
    returnList = ['Eb' if note=='D#' else note for note in returnList]
    returnList = ['Gb' if note=='F#' else note for note in returnList]
    return returnList


def toFlatOrSharp(seedList):
    returnList = ['E#' if note=='F' else note for note in seedList] 
    returnList = ['B#' if note=='C' else note for note in returnList]
    return returnList

def makeScale(letter, maj):
    if maj:
        key = major()
    else:
        key = minor()
    if letter not in SHARP_NOTES and letter not in FLAT_NOTES:
        return 'Sorry, {0} does not have a key.'.format(letter)
    if 'b' not in letter:
        returnList = createList(letterShift(SHARP_NOTES, letter), key)
    else:
        returnList = createList(letterShift(FLAT_NOTES, letter), key)
    if litmus(returnList) == False:
        returnList = toFlatOrSharp(returnList)
    if litmus(returnList) == True:
        returnList
    if key == major():
        return toFlat(createList(letterShift(SHARP_NOTES, letter), key))
    if key == minor():
        return toFlat(createList(letterShift(SHARP_NOTES, letter), key))

'''
for i in SHARP_NOTES:
        print(i + ' = ' + str(makeScale(i, minor())))



for i in SHARP_NOTES:
        print(i + ' = ' + str(makeScale(i, major())))


print('a' + ' = ' + str(makeScale('A', major())))
print('a' + ' = ' + str(makeScale('A', minor())))
print makeScale("F", major())
'''