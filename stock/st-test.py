import stackless
import urllib2
def output():
    while 1:
        url=chan.receive()
        print url
        f=urllib2.urlopen(url)
        #print f.read()
        print stackless.getcurrent()
     
def input():
    f=open('url.txt')
    l=f.readlines()
    for i in l:
        chan.send(i)
chan=stackless.channel()
[stackless.tasklet(output)() for i in xrange(10)]
stackless.tasklet(input)()
stackless.run()