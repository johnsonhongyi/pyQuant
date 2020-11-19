import matplotlib.pyplot
import time
import threading

# Super Hacky Way of Getting input() to work in Spyder with Matplotlib open
# No efforts made towards thread saftey!

prompt = False
promptText = ""
done = False
waiting = False
response = ""

regular_input = input

def threadfunc():
    global prompt
    global done
    global waiting
    global response

    while not done:   
        if prompt:   
            prompt = False
            response = regular_input(promptText)
            waiting = True
        time.sleep(0.1)

def input(text):
    global waiting
    global prompt
    global promptText

    promptText = text
    prompt = True

    while not waiting:
        matplotlib.pyplot.pause(0.01)
    waiting = False

    return response

def start():
    thread = threading.Thread(target = threadfunc)
    thread.start()

def finish():
    global done
    done = True

start()
finish()
input('abc')  #what ????????????