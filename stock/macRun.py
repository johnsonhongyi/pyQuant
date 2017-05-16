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
scriptquit = '''tell application "Python Launcher" to quit
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

# positionKey = {'sina_Market-DurationDn.py': '313, 433',
#                'sina_Market-DurationUp.py': '-17, 470',
#                'sina_Market-DurationSH.py': '148, 560',
#                'sina_Monitor-Market-New.py': '-2, 371',
#                'sina_Monitor-Market-LH.py': '440, 293',
#                'sina_Monitor-Market.py': '19, 179',
#                'sina_Monitor-GOLD.py': '43, 80',
#                'sina_Monitor.py': '85, 27',
#                'singleAnalyseUtil.py': '583, 23',
#                'LinePower.py':'767, 527',}
               
# positionKey = {'sina_Market-DurationDn.py': '237, 403',
#                'sina_Market-DurationDnUP.py': '-23, 539',
#                'sina_Market-DurationCXDN': '31, 80',
#                'sina_Market-DurationSH.py': '217, 520',
#                'sina_Monitor-Market-New.py': '-2, 371',
#                'sina_Monitor-Market-LH.py': '341, 263',
#                'sina_Monitor-Market.py': '19, 179',
#                'sina_Monitor-GOLD.py': '-7, 149',
#                'sina_Monitor.py': '69, 22',
#                'singleAnalyseUtil.py': '583, 22',
#                'LinePower.py':'42, 504',}


# positionKeyDnup = {'sina_Market-DurationDn.py': '246, 322',
#                'sina_Market-DurationDnUP.py': '-23, 539',
#                'sina_Market-DurationCXDN': '19, 46',
#                'sina_Market-DurationSH.py': '217, 520',
#                'sina_Market-DurationUP.py': '-15, 112',
#                'sina_Monitor-Market-LH.py': '150, 159',
#                'sina_Monitor-Market.py': '19, 179',
#                'sina_Monitor.py': '83, 22',
#                'singleAnalyseUtil.py': '583, 22',
#                'LinePower.py':'40, 497',}

positionKey = {'sina_Market-DurationDn.py': '217, 520',
               'sina_Market-DurationCXDN': '8, 52',
               'sina_Market-DurationSH.py': '-23, 539',
               'sina_Market-DurationUP.py': '-19, 111',
               'sina_Monitor-Market-LH.py': '184, 239',
               'sina_Monitor-Market.py': '19, 179',
               'sina_Monitor.py': '39, 22',
               'singleAnalyseUtil.py': '620, 22',
               'LinePower.py':'40, 497',}

cmdRun_dnup = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
open sina_Market-DurationDn.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open singleAnalyseUtil.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Monitor.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Monitor-Market-LH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Market-DurationUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Market-DurationCXDN.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Market-DurationSH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open LinePower.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
open sina_Market-DurationDnUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
'''

cmdRun = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
open sina_Market-DurationDn.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open singleAnalyseUtil.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Monitor.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Monitor-Market-LH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Market-DurationCXDN.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open sina_Market-DurationSH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
open LinePower.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
open sina_Market-DurationUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
'''

# cmdRun = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
# open singleAnalyseUtil.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Monitor.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Monitor-GOLD.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Monitor-Market.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Monitor-Market-New.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Monitor-Market-LH.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Market-DurationUp.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Market-DurationDn.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open sina_Market-DurationSH.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 35;
# open LinePower.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 5;
# '''
closeLaunch ='''osascript -e 'tell application "Python Launcher" to quit';sleep 35;'''

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
    if int(count) > 3:
        doScript(scriptquit)
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
        os.system(closeLaunch) 
    else:
        print "run Cmd"
        os.system(cmdRun)
        setPosition(cmd=None, position=None)
# count = doScript(scriptcount        
# os.system(cmdRun)
count = doScript(scriptcount)
# print count
if int(count) > 3:
    print getPosition('singleAnalyseUtil.py')
    print getPosition('sina_Market-DurationDn.py')
    print getPosition('sina_Monitor-Market-LH.py')
    print getPosition('sina_Market-DurationUP.py')
    print getPosition('sina_Market-DurationSH.py')
    print getPosition('sina_Market-DurationCXDN.py')
    print getPosition('sina_Market-DurationCXUP.py')
    print getPosition('sina_Market-DurationDnUP.py')
    # print getPosition('sina_Monitor-GOLD.py')
    print getPosition('sina_Monitor.py')
    print getPosition('LinePower.py')
setPosition(cmd=None, position=None)