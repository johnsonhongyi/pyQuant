# -*- coding:utf-8 -*-
# !/usr/bin/env python
import subprocess
import os,time
script = '''tell application "System Events"
    activate
    display dialog "Hello Cocoa!" with title "Sample Cocoa Dialog" default button 2
end tell
'''
scriptcount = '''tell application "Terminal"
    --activate
    get the count of window
end tell
'''

scriptname = '''tell application "Terminal"
    --activate
    %s the name of window %s
end tell
'''
script_get_position = '''tell application "Terminal"
    --activate
    %s position of window %s 
end tell
'''
script_set_position = '''tell application "Terminal"
    --activate
    %s position of window %s to {%s}
end tell
'''

positionKey = {'sina_Market-DurationDn.py': '267, 448',
               'sina_Market-DurationUp.py': '0, 490',
               'sina_Monitor-Market-New.py': '-2, 371',
               'sina_Monitor-Market-LH.py': '440, 293',
               'sina_Monitor-Market.py': '19, 179',
               'sina_Monitor-GOLD.py': '43, 80',
               'sina_Monitor.py': '85, 27',
               'singleAnalyseUtil.py': '583, 23',
               'LinePower.py':'675, 526',}

cmdRun = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
open singleAnalyseUtil.py;
sleep 16;
open sina_Monitor.py;
sleep 16;
open sina_Monitor-GOLD.py;
sleep 16;
open sina_Monitor-Market.py;
sleep 16;
open sina_Monitor-Market-New.py;
sleep 16;
open sina_Monitor-Market-LH.py;
sleep 16;
open sina_Market-DurationUp.py;
sleep 36;
open sina_Market-DurationDn.py;
sleep 16;
rem cd JSONData;
open LinePower.py;
sleep 5;
'''


def doScript(scriptn):
    proc = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    stdout_output = proc.communicate(scriptn)[0]
    # print stdout_output, type(proc)
    return stdout_output

def getPosition(cmd=None, position=None):
    count = doScript(scriptcount)
    if count > 1:
        for n in xrange(1, int(count)):
            # print n
            title = doScript(scriptname % ('get', str(object=n)))
            if title.lower().find(cmd.lower()) > 0:
                print title
                # position = doScript(
                    # script_set_position % ('set', str(n), positionKey[key]))
                position=doScript(script_get_position % ('get', str(n)))
                # position = doScript(scriptposition % ('get', str(n)))
                return position

def setPosition(cmd=None, position=None):
    count = doScript(scriptcount)
    # print count
    if int(count) > 2:
        for n in xrange(1, int(count)):
            # print n
            title = doScript(scriptname % ('get', str(object=n)))
            for key in positionKey:
                # print key
                if title.lower().find(key.lower()) > 0:
                    # print title, positionKey[key]
                    position = doScript(
                        script_set_position % ('set', str(n), positionKey[key]))
                    # print doScript(script_get_position % ('get', str(n)))
            # position = doScript(scriptposition % ('get', str(n)))
            # print positio
    else:
        print "run Cmd"
        os.system(cmdRun)
        setPosition(cmd=None, position=None)
# count = doScript(scriptcount        
# os.system(cmdRun)
print getPosition('sina_Monitor.py')
print getPosition('sina_Market-DurationDn.py')
print getPosition('powerCompute.py')
setPosition(cmd=None, position=None)