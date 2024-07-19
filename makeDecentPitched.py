# a python script to make a decentSampler patch
# Mark Reuter July 2024

# step 1 ceate a dictionary for pitch to MIDI note mapping
# step 2 read in wav files from a directory
# step 3 construct and write the group mapping
# step 4 create and write the final file complete with GUI (a user could choose effects - TODO)

import os, re


#START - create dictionary

print("---xxx--- Pitch dictionary section ---xxx---")

#add variables for creating pitch dictionary
notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
pitches = [0,1,2,3,4,5,6,7]
pitchStart = 12

#intantiate empty dictionary
mappingDictionary = {}

#loop through notes AND pitches to create dictionary
for i in pitches:
    for j in notes:
        noteName = str(j) + str(i)
        #print(noteName + "=" + str(pitchStart))
        mappingDictionary.update({noteName:pitchStart})
        pitchStart += 1
    
print(mappingDictionary)

#END - Dictionary

#get path, could take this as an arugment or user input
path = "/Users/markreuter/Documents/Abominable_macbookAir/abominableInstruments-main/Brassando/samples"

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

print("All wav files: " + str(wavFiles))


print("---xxx--- Pitch regex section ---xxx---")

decentSamplerGroupList = list()

# construct a regex to find, for example A4
pitchregex = re.compile(r'[ABCDEFG]+[1234567]')

# generate opcodes
for i in wavFiles:
    print("First search item:" + i)
    #print(i)
    p = pitchregex.search(wavFiles[0])
    #print(p)
    matchedString = p.group()
    print("Matched string is: " + str(matchedString))
    if matchedString in mappingDictionary:
        print("True")
        mappingValue = mappingDictionary.get(matchedString)
        print(str(mappingValue))
    else:
        print("False")
    #create the concatenated text
    decentSamplerGroupList.append('\t' + '<sample loNote="' + str(mappingValue) + '" hiNote="' + str(mappingValue) + '" rootNote="' + str(mappingValue) + '" seqPosition="1" volume="1" path="../samples/' + i + '"/>')

print(decentSamplerGroupList)

#get current working directory as a reference
currentWorkingDir = os.getcwd()
print(currentWorkingDir)


groupOpcode = '<groups attack="0.1" decay="1.0" sustain="1.0" release="3.0" attackCurve="100" releaseCurve="0" volume="0.0dB" pan="0"> \n <group name="myGroup" seqMode="round_robin">'
groupOpcodeClose = ' </group>' + "\n" + '</groups>'

decentSamplerGroupList.insert(0,groupOpcode)  
decentSamplerGroupList.append(groupOpcodeClose)

file = open('decentSamplerGroupOpcodes.txt','w')
for slot in decentSamplerGroupList:
	file.write(slot + "\n")
file.close()

print("Opcodes for samples written")

decentSamplerHeader = """<?xml version="1.0" encoding="UTF-8"?>
<DecentSampler>
  <ui bgImage="../resources/someArt.png" width="812" height="375" layoutMode="relative"
      bgMode="top_left">
    <tab name="main">
      <labeled-knob x="710" y="100" label="Tone" type="float" minValue="60" maxValue="22000"
                    textColor="FFfff5ee" textSize="30" value="22000.0" trackForegroundColor="FF2E7D32" trackBackgroundColor="FF424242">
        <binding type="effect" level="instrument" position="0" parameter="FX_FILTER_FREQUENCY"/>
      </labeled-knob>

      <!-- reverb -->
      <labeled-knob x="710" y="1" label="Reverb" type="percent" minValue="0" maxValue="100"
                    textColor="FFfff5ee" textSize="30" value="20.0" trackForegroundColor="FF0097A7" trackBackgroundColor="FF424242">  
        <binding type="effect" level="instrument" position="1" parameter="FX_REVERB_WET_LEVEL"
                 factor="0.01"/>
      </labeled-knob>

      <!-- chorus -->

      <labeled-knob x="500" y="100" label="Chorus Mix" type="float" minValue="0.0" maxValue="1" value="0" 
                    textSize="28" textColor="FFfff5ee" trackForegroundColor="FF66A58C" trackBackgroundColor="FF424242">
        <binding type="effect" level="instrument" position="2" parameter="FX_MIX" />
      </labeled-knob>

      <labeled-knob x="550" y="130" width="90" height="90" label="Depth" type="float" minValue="0.0" maxValue="1.0" value="0.4" 
                    textSize="28" textColor="FFfff5ee" trackForegroundColor="FF66A58C" trackBackgroundColor="FF424242">
        <binding type="effect" level="instrument" position="2" parameter="FX_MOD_DEPTH" />
      </labeled-knob>

      <labeled-knob x="630" y="130" width="90" height="90" label="Rate" type="float" minValue="0.0" maxValue="1.0" value="0.4" 
                    textSize="28" textColor="FFfff5ee" trackForegroundColor="FF66A58C" trackBackgroundColor="FF424242">
        <binding type="effect" level="instrument" position="2" parameter="FX_MOD_RATE" />
      </labeled-knob>

      <!-- amp env -->

      <labeled-knob x="5" y="1" label="Attack" type="float" minValue="0.0" maxValue="3.0"
                    textColor="FFfff5ee" textSize="30" value="0.1" trackForegroundColor="FFEF6C00" trackBackgroundColor="FF424242">
        <binding type="amp" level="instrument" position="1" parameter="ENV_ATTACK"/>
      </labeled-knob>

      <labeled-knob x="5" y="100" label="Release" type="float" minValue="0.0" maxValue="3.0"
                    textColor="FFfff5ee" textSize="30" value="1.0" trackForegroundColor="FFEF6C00" trackBackgroundColor="FF424242">
        <binding type="amp" level="instrument" position="1" parameter="ENV_RELEASE"/>
      </labeled-knob>

    </tab>
  </ui> \n"""
decentSamplerFooter = """<effects> <effect type="lowpass_4pl" frequency="22000.0"/>
    <effect type="reverb" wetLevel="0.5"/>
    <effect type="chorus" mix="0.0" modDepth="0.4" modRate="0.4"/>'
  </effects>
</DecentSampler>"""

file = open('decentSamplerPatchPython.txt','w')
file.write(decentSamplerHeader)
for slot in decentSamplerGroupList:
	file.write(slot + "\n")
file.write(decentSamplerFooter)
file.close()

print("decentSampler biolerplate written")



