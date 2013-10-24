"""
This is a small code that started from here:
http://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
"""

import pyaudio
import math
import struct
import wave
import sys
import os

#Assuming Energy threshold upper than 30 dB
Threshold = 30

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 48000
swidth = 2
Max_Seconds = 30
TimeoutSignal=((RATE / chunk * Max_Seconds) + 2)
silence = True
FileNameTmp = './file.wav'
Time=0

def rms(frame):
        count = len(frame)/swidth
        format = "%dh"%(count)
        shorts = struct.unpack( format, frame )

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n*n
        rms = math.pow(sum_squares/count,0.5);

        return rms * 1000



def WriteSpeech(WriteData):
    #stream.stop_stream()
    #stream.close()
    #p.terminate()
    os.system("rm "+FileNameTmp)
    wf = wave.open(FileNameTmp, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(WriteData)
    wf.close()
    wr = wave.open(FileNameTmp,'rb')
    data = wr.readframes(chunk)
    while data != '':
        stream.write(data)
        data = wr.readframes(chunk)
    wr.close()




def KeepRecord(TimeoutSignal, LastBlock):

    all = []
    all.append(LastBlock)
    tail = 0
    for i in range(0, TimeoutSignal):
        try:
            data = stream.read(chunk)
            rms_value = rms(data)
            #print "RMS is %d and Threshold is %d\n" % (rms_value,Threshold)
            if (rms_value < Threshold):
                tail += 1
                if tail >100: #tune this value to select how long should be silence before stopping recording
                    print "break\n"
                    break
            else:
                #print "tail reset\n"
                tail =0
        except:
            continue
        
	all.append(data)

    data = ''.join(all)
    print "write to File";
    WriteSpeech(data)
    silence = True
    Time=0
    listen(silence,Time)     

def listen(silence,Time):
    print "waiting for Speech"
    while silence:

        try:

            input = stream.read(chunk)

        except:

            continue


        rms_value = rms(input)

        #print "RMS is %d and Threshold is %d\n" % (rms_value,Threshold)

        if (rms_value > Threshold):

            silence=False

            LastBlock=input

            print "hello ederwander I'm Recording...."
            KeepRecord(TimeoutSignal, LastBlock)







p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = chunk,
    input_device_index=3) # if you have more than 1 sound card you have to tune this, use system_info.py to see your index



listen(silence,Time) 
