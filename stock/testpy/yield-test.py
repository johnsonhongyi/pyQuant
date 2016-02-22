#-*- encoding: utf-8 -*-
import traceback  
import sys  

def consumer():
    n=0
    print('consumer init')
    while True:
        n=yield n
        if not n:
            return
        n-=1
        print ('消费了1,还剩余 %d'%n)

def produce(c):
    n=0
    next(c)
    while n<6:
        n+=2
        print('生产了2,总共有%d'%n)
        n=c.send(n)
        print ('确认还剩: %d'%n)
    c.close()

# c = consumer()
# produce(c)
def main():
    while 1:
        try:
            status=True
            input=raw_input("input:")
            if input=='q':
                sys.exit(0)
        except (KeyboardInterrupt) as e:
                    # print "key"
                    print "KeyboardInterrupt:", e
                    if not status:
                        input2=raw_input("input:")
                        if input2=='q':
                            sys.exit(0)
        except:
            print "except"
            traceback.print_exc()
            info=sys.exc_info()  
            print info[0],":",info[1]  
            sys.exit(0)

# while 1:
    # print eval(raw_input('DEBUG>>>'))