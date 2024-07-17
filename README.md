# decentSamplerBoilerplate
A python script to generate decentSamper patches from a folder of wav files

This python script will
a) generate a dictionary of pitch to MIDI note mappings
b) read all .wav files from a directory
c) create all the opcode mapping where pitch text (i.e. A4) is detected
d) write opcodes for the note group
e) write an entire decentSampelr boilerplate with low pass filter, reverb, and chorus effects

A user will still need to add/remove additional effects and edit the pitch high and low notes


