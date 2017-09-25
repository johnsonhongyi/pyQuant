import time

def getFibonacci(num):
    res = [0, 1]
    a = 0
    b = 1
    for i in range(0, num):
        if i == a + b:
            res.append(i)
            a, b = b, a + b
    return res

# nduration=fib1

# high_p
# close_p


if __name__ == '__main__':
    n = 40

    time_s = time.time()
    res = getFibonacci(300)
    print(res)
    print("fib1-t:%s" % (time.time() - time_s))
