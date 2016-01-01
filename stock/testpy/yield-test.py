#-*- encoding: utf-8 -*-


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

c = consumer()
produce(c)