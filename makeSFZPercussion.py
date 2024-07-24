# a python script to make an SFZ patch - simple percussion mapping
# Mark Reuter July 2024

#this script ignores the file name and just maps each wav file (alphabetical order) sequencially to the keyboard starting at note 24

# step 1 read in wav files from a directory
# step 2 construct and write the group mapping
# step 3 create and write the final SFZ file

import os, re

#get path, could take this as an arugment or user input
path = "/Users/markreuter/Documents/Abominable_macbookAir/abominableInstruments-main/Cymbals and Rides/samples"


#get all files
dirList = os.listdir(path)
print("All files: " + str(dirList))

#instantiate an empty list
wavFiles = list()

#check for .wav files
for i in dirList:
    #print(str(i.endswith))
    if i.endswith(".wav") == True:
        print(i)
        wavFiles.append(i)

wavFiles = sorted(wavFiles)
print("All wav files: " + str(wavFiles))


print("---xxx--- Pitch regex section ---xxx---")

sfzGroupList = list()


pitchNumber = 24
# generate opcodes
for i in wavFiles:
    print("First search item:" + i)
    #print(i)
    #create the concatenated text
    print(str(pitchNumber))
    #decentSamplerGroupList.append('\t' + '<sample loNote="' + str(pitchNumber) + '" hiNote="' + str(pitchNumber) + '" rootNote="' + str(pitchNumber) + '" seqPosition="1" volume="1" path="../samples/' + i + '"/>')
    sfzGroupList.append('<region> sample=../samples/' + i + ' lokey=' + str(pitchNumber) + ' hikey=' + str(pitchNumber) + ' pitch_keycenter=' + str(pitchNumber) + ' seq_length=1 seq_position=1 lovel=0 hivel=127')
    pitchNumber = pitchNumber + 1
    

print(sfzGroupList)

#get current working directory as a reference
currentWorkingDir = os.getcwd()
print(currentWorkingDir)


#groupOpcode = '<groups attack="0.0" decay="1.0" sustain="1.0" release="3.0" attackCurve="100" releaseCurve="0" volume="0.0dB" pan="0"> \n <group name="myGroup" seqMode="round_robin">'
groupOpcode = """<group>
ampeg_attack=0
ampeg_release=0.5
ampeg_attackcc100=0
ampeg_releasecc103=10"""

#groupOpcodeClose = ' </group>' + "\n" + '</groups>'

sfzGroupList.insert(0,groupOpcode)  
#decentSamplerGroupList.append(groupOpcodeClose)

file = open('sfzGroupOpcodes.txt','w')
for slot in sfzGroupList:
	file.write(slot + "\n")
file.close()

print("Opcodes for samples written")



sfzHeader = """//SFZ sample instrument
//2024-xx-xx
//made with love by Mark

<control>
label_cc100=Attack
label_cc103=Release
set_cc100=0
set_cc103=13

<global> \n"""

sfzFooter = "//end"

file = open('sfzPatchPython.txt','w')
file.write(sfzHeader)
for slot in sfzGroupList:
	file.write(slot + "\n")
file.write(sfzFooter)
file.close()

print("SFZ biolerplate written")



