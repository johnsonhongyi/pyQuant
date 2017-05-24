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

'''tell application "Terminal" --activate;get the count of window end tell '''

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

exit_terminal = '''osascript -e "tell application "Terminal"" 
    -e "do script "exit()" in tab 1 of front window" 
    -e "end tell" '''


'''
osascript \
    -e "tell application \"Terminal\"" \
    -e "do script \"exit()\" in tab 1 of front window" \
    -e "end tell"
'''

'''
osascript -e
 "tell application "System Events"
        tell process "Terminal"
            keystroke "w" using {command down}
        end tell
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
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open singleAnalyseUtil.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Monitor.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Market-DurationUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Monitor-Market-LH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Market-DurationCXDN.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Market-DurationSH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open LinePower.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
open sina_Market-DurationDnUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 5;
'''

cmdRun = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
open sina_Market-DurationDn.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open singleAnalyseUtil.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Monitor.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Monitor-Market-LH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 15;
open sina_Market-DurationUP.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Market-DurationCXDN.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open sina_Market-DurationSH.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
open LinePower.py;
sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 1;
'''

# cmdRun = '''cd /Users/Johnson/Documents/Quant/pyQuant/stock;
# open singleAnalyseUtil.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Monitor.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Monitor-GOLD.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Monitor-Market.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Monitor-Market-New.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Monitor-Market-LH.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Market-DurationUp.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Market-DurationDn.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open sina_Market-DurationSH.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 25;
# open LinePower.py;
# sleep 0.1;osascript -e 'tell application "Python Launcher" to quit';sleep 5;
# '''
closeLaunch ='''osascript -e 'tell application "Python Launcher" to quit';sleep 0.1;'''
closeterminalw = '''osascript -e 'tell application "Terminal" to close windows %s' '''
closeterminal_window = '''osascript -e 'tell application "Terminal" to close windows %s saving no' '''
activate_terminal = '''  osascript -e 'tell application "Terminal" to activate (every window whose name contains "%s")' '''
activate_terminal_argc = '''  osascript -e 'tell application "Terminal" to %s (every window whose name contains "%s")' '''

def doScript(scriptn):
    proc = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    stdout_output = proc.communicate(scriptn)[0]
    # print stdout_output, type(proc)
    return stdout_output

def getPosition(cmd=None, position=None,close=False):
    count = doScript(scriptcount)
    if count > 0:
        for n in xrange(1, int(count)+1):
            title = doScript(scriptname % ('get', str(object=n)))
            # if close:
                # print "close:%s"%(title),
            if title.lower().find(cmd.lower()) >= 0:
                # print "win:%s get_title:%s "%(n,title)
                # print "get:%s"%(n)
                # position = doScript(
                    # script_set_position % ('set', str(n), positionKey[key]))
                position=doScript(script_get_position % ('get', str(n)))
                # position = doScript(scriptposition % ('get', str(n)))
                if close:
                    # print ("close:%s %s"%(n,title))
                    os.system(closeterminalw%(n))
                return position

def setPosition(cmd=None, position=None):
    count = doScript(scriptcount)
    # print count
    if int(count) > 3:
        doScript(scriptquit)
        for n in xrange(1, int(count)+1):
            # print "n:%s"%(n)
            title = doScript(scriptname % ('get', str(object=n)))
            for key in positionKey:
                # print "key:%s"%(key)
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
        os.system(closeLaunch) 
        # getPosition('Johnson@',close=True)
        # getPosition('/Users/Johnson/Documents',close=True)
        # getPosition('Johnson — bash',close=True)
        # getPosition('Johnson — python',close=True)
# count = doScript(scriptcount        
# os.system(cmdRun)
# getPosition('Johnson@',close=True)


count = doScript(scriptcount)
# print count
# count = 2
if int(count) > 3:
    # print getPosition('Johnson@bogon',close=True)
    # print getPosition('cd \'/Users/Johnson/Documents/Quant/pyQuant/stock/\'')
    # print getPosition('cd \'/Users/Johnson/Documents')
    # print getPosition('cd \'/Users/Johnson/Documents',close=True)
    print getPosition('singleAnalyseUtil.py')
    print getPosition('sina_Market-DurationDn.py')
    print getPosition('sina_Monitor-Market-LH.py')
    print getPosition('sina_Market-DurationUP.py')
    print getPosition('sina_Market-DurationSH.py')
    print getPosition('sina_Market-DurationCXDN.py')
    print getPosition('sina_Market-DurationCXUP.py')
    print getPosition('sina_Market-DurationDnUP.py')
    print getPosition('sina_Monitor-GOLD.py')
    print getPosition('sina_Monitor.py')
    print getPosition('LinePower.py')
    getPosition('Johnson@',close=True)
    getPosition('/Users/Johnson/Documents',close=True)
    
setPosition(cmd=None, position=None)

getPosition('Johnson — bash',close=True)
# getPosition('Johnson — python',close=True)
getPosition('Johnson — osasc',close=True)

'''

https://stackoverflow.com/questions/8798641/close-terminal-window-from-within-shell-script-unix

How do I quit the Terminal application without invoking a save dialog?

Hello, I am trying to write an AppleScript that will allow me to close the application Terminal without invoking a dialog box. In my situation I have just run a Python script on Terminal and when I try to quit the Terminal application I am always presented with a "Do you want to close this window?" dialog box. I wrote a simple AppleScript where I specify that I do not want to save when quitting but I am still presented with the dialog box. Does anybody know how to exit the Terminal application with an AppleScript that does not require any user interaction beyond initiating the AppleScript? Here is the simple script I wrote:

tell application "Terminal"
quit saving no
end tell


Then at the end of the script, use:

osascript -e 'tell application "Terminal" to close (every window whose name contains "My Window Name")' &

closeWindow() {
    /usr/bin/osascript << _OSACLOSE_
    tell application "Terminal"
        close (every window whose name contains "YourScriptName")
    end tell
    delay 0.3
    tell application "System Events" to click UI element "Close" of sheet 1 of window 1 of application process "Terminal"
_OSACLOSE_
}


This works for me:

#!/bin/sh

{your script here}

osascript -e 'tell application "Terminal" to close (every window whose name contains ".command")' &
exit


I find the best solution for this is to use Automator to create a true OSX application which will work the same way regardless of how your system is configured. You can have the Automator run your shell script, or you can embed the shell script itself in Automator.

Here is how you do it:

Run Automator (in Applications).
Choose "New Document" and when it asks "Choose a type for your document" choose "Application"
In the left panel, select "Utilities" then "Run Shell Script".
Type in your script commands in the workflow item in the right panel. You can either call another shell script, or just put your commands in their directly.
Save the Application, which will be a full-fledged Mac App. You can even cut-and-paste icons from other apps to give your script some personality.


'''

'''
Even doing a kill or killall without the -9 is abrupt. It doesn't allow Terminal.app to do it's normal checking of whether there are processes still running that you may care about. Why not tell the terminal to quit a a more appleish way? Use AppleEvents.

alias quit='/usr/bin/osascript -e "tell application \"terminal\" to quit"'
If you want something that you can always run when you're done with a window, which will quit Terminal.app in the event it was the last window, a larger script might be in order. First create this AppleScript:
tell application "Terminal"
    if (count of (every window whose visible is true)) <= 1 then
        quit
    else
        close window 1
    end if
end tell
Then just alias it to whatever command you want and add osascript to the list of ignored processes under the Processes section of the window settings.
---

jon

Just 'trap' it
Authored by: apparissus on May 05, '04 11:42:52PM
If you don't want to remember to type "quit" instead of "exit", and you're using bash, just add the following to your .bashrc or other shell startup script:
trap '/usr/bin/osascript -e "tell application \"terminal\" to quit"' 0
What's it do? When the shell receives signal 0 (zero), that is, told to exit, it will execute this command as the last thing it does. This allows your shell, etc, to exit gracefully, and asking Terminal.app to exit via applescript makes sure it does the same. In other words, type 'exit', and your shell exits, then Terminal quits, all cleanly and the way nature intended.

Note:You'll need to add login, bash, and osascript to the exclude list under "Prompt before closing window" or terminal will whine at you before exiting. Or you could just choose "Never". 

Something similar is surely possible with tcsh...but I have no idea how.
'''

'''
https://superuser.com/questions/526624/how-do-i-close-a-window-from-an-application-passing-the-file-name
Closing a window from an application

1) By window index or name of the window

The command to close a window of any named application would be something like this:

tell application "Preview" to close window 1
… or if you want to close a named document window, e.g. foo.jpg:

tell application "Preview" to close (every window whose name is "foo.jpg")
So, in your shell script that'd be:

#!/bin/sh
osascript <<EOF
tell application "Preview"
  close (every window whose name is "$1")
end tell
EOF
Here, the first argument passed to the script is the name of the window you want to close, e.g. ./quit.sh foo.jpg. Note that if your file contains spaces, you have to quote the filename, e.g. ./quit.sh "foo bar.jpg".

Or if you want to close arbitrary windows from any application, use this:

#!/bin/sh
osascript <<EOF
tell application "$1"
  close (every window whose name is "$2")
end tell
EOF
Here, you'd use ./quit.sh Preview foo.jpg for example.

2) By file name

If you want to close a window that belongs to a certain document, but supplying the file name, you need something else. This is because a multi-page PDF could be displayed as foo.pdf (Page 1 of 42), but you'd just want to pass foo.pdf to the AppleScript.

Here we iterate through the windows and compare the filenames against the argument passed to the script:

osascript <<EOF
tell application "Preview"
    set windowCount to number of windows
    repeat with x from 1 to windowCount
        set docName to (name of document of window x)
        if (docName is equal to "$1") then
            close window x
        end if
    end repeat
end tell
EOF
Now you can simply call ./quit.sh foo.pdf. In a generalized fashion, for all apps with named document windows, that'd be:

osascript <<EOF
tell application "$1"
    set windowCount to number of windows
    repeat with x from 1 to windowCount
        set docName to (name of document of window x)
        if (docName is equal to "$2") then
            close window x
        end if
    end repeat
end tell
EOF


Caveat: Auto-closing Preview.app

Preview.app is one of these applications that automatically quits once its last document window is closed. It does that in order to save memory and "clean up". To disable this behavior, run the following:

defaults write -g NSDisableAutomaticTermination -bool TRUE
Of course, to undo that, change TRUE to FALSE.



Using functions instead of scripts

Finally, I'd suggest putting your scripts into a function that is always available in your shell. To do this, add the scripts to your ~/.bash_profile. Create this file if it doesn't exist.

cw() {
osascript <<EOF
tell application "$1"
    set windowCount to number of windows
    repeat with x from 1 to windowCount
        set docName to (name of document of window x)
        if (docName is equal to "$2") then
            close window x
        end if
    end repeat
end tell
EOF
}
Once you save your bash profile and restart the shell, you can call cw Preview foo.pdf from everywhere.
'''
