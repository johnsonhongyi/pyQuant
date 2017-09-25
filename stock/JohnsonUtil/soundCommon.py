#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-20 17:44:29
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave
import sys
import os
import time
CHUNK = 2048
# http://people.csail.mit.edu/hubert/pyaudio/docs/
def play_msg_warning(retry = 1,fpn='busy.wav'):
    fp = '/Users/Johnson/Downloads/MacQuant/PythonStockMd-master/wav'+os.sep+fpn
    pyaudio.paCoreAudio = 5
    for x in range(retry):
        wf = wave.open(fp, 'rb')
        data = wf.readframes(CHUNK)
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()
        p.terminate()
        wf.close

def play_msg_warning_call(fname='busy.wav',retry=1):
    fp = '/Users/Johnson/Downloads/MacQuant/PythonStockMd-master/wav'+os.sep+fname
    # fp = fname
    print fname
    # pyaudio.paCoreAudio = 5
    for x in range(retry):
        print "run:%s"%(x)
        wf = wave.open(fp, 'rb')
        p = pyaudio.PyAudio()

        # define callback (2)
        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        # start the stream (4)
        stream.start_stream()

        # wait for stream to finish (5)
        while stream.is_active():
            time.sleep(0.05)

        # stop stream (6)
        stream.stop_stream()
        stream.close()
        wf.close()

        # close PyAudio (7)
        p.terminate()
# play_msg_warning(retry=1)
play_msg_warning_call()