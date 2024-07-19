# a python script to make a decentSampler patch - simple percussion mapping
# Mark Reuter July 2024

#this script ignores the file name and just maps each wav file (alphabetical order) sequencially to the keyboard starting at note 24

# step 1 read in wav files from a directory
# step 2 construct and write the group mapping
# step 3 create and write the final file complete with GUI (a user could choose effects - TODO)

import os, re

#get path, could take this as an arugment or user input
path = "/Users/markreuter/Documents/Abominable_macbookAir/abominableInstruments-main/FAT BUDDHA DRUMS/samples"

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

decentSamplerGroupList = list()


pitchNumber = 24
# generate opcodes
for i in wavFiles:
    print("First search item:" + i)
    #print(i)
    #create the concatenated text
    print(str(pitchNumber))
    decentSamplerGroupList.append('\t' + '<sample loNote="' + str(pitchNumber) + '" hiNote="' + str(pitchNumber) + '" rootNote="' + str(pitchNumber) + '" seqPosition="1" volume="1" path="../samples/' + i + '"/>')
    pitchNumber = pitchNumber + 1
    

print(decentSamplerGroupList)

#get current working directory as a reference
currentWorkingDir = os.getcwd()
print(currentWorkingDir)


groupOpcode = '<groups attack="0.0" decay="1.0" sustain="1.0" release="3.0" attackCurve="100" releaseCurve="0" volume="0.0dB" pan="0"> \n <group name="myGroup" seqMode="round_robin">'
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

      <!-- Gain -->
      <labeled-knob x="600" y="100" label="Gain" type="float" minValue="-6" maxValue="16"
                    textColor="FF910000" textSize="30" value="4" trackForegroundColor="FF0097A7" trackBackgroundColor="FF424242">  
        <binding type="effect" level="instrument" position="2" parameter="LEVEL"/>
      </labeled-knob>

      <!-- amp env -->

      <labeled-knob x="5" y="1" label="Attack" type="float" minValue="0.0" maxValue="3.0"
                    textColor="FFfff5ee" textSize="30" value="0.0" trackForegroundColor="FFEF6C00" trackBackgroundColor="FF424242">
        <binding type="amp" level="instrument" position="1" parameter="ENV_ATTACK"/>
      </labeled-knob>

      <labeled-knob x="5" y="100" label="Release" type="float" minValue="0.0" maxValue="3.0"
                    textColor="FFfff5ee" textSize="30" value="1.0" trackForegroundColor="FFEF6C00" trackBackgroundColor="FF424242">
        <binding type="amp" level="instrument" position="1" parameter="ENV_RELEASE"/>
      </labeled-knob>

    </tab>
  </ui> \n"""
decentSamplerFooter = """<effects>
 <effect type="lowpass_4pl" frequency="22000.0"/>
    <effect type="reverb" wetLevel="0.5"/>
    <effect type="gain" level="-6" />
  </effects>
</DecentSampler>"""

file = open('decentSamplerPatchPython.txt','w')
file.write(decentSamplerHeader)
for slot in decentSamplerGroupList:
	file.write(slot + "\n")
file.write(decentSamplerFooter)
file.close()

print("decentSampler biolerplate written")



