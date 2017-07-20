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

CHUNK = 1024
# http://people.csail.mit.edu/hubert/pyaudio/docs/
def play_msg_warning(retry = 1,fp=None):
    fp = '/Users/Johnson/Downloads/MacQuant/PythonStockMd-master/wav/msg.wav'
    # pyaudio.paCoreAudio = 5
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

        print x
        stream.stop_stream()
        stream.close()
        p.terminate()

play_msg_warning(retry=3)
