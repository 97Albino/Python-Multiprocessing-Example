import time
import sys
import multiprocessing as process
import os

i = 0
j = 0
sem = process.Semaphore(2)

def Worker(num):
    global i,j
    while True:
        sem.acquire()
        pi = i
        i += num
        print('PID ' + str(os.getpid()) + ' : ' + str(pi) +' + '+ str(num) +' : ' + str(i))
        sem.release()

        sem.acquire()
        pj = j
        j -= num
        print('PID ' + str(os.getpid()) + ' : ' + str(pi) +' + '+ str(num) +' : ' + str(i))
        sem.release()

        print('PID ' + str(os.getpid()) + ' Parent PID : '+ str(os.getppid()))

        time.sleep(0.01)
    # process.currentProcess().getName()

if __name__ == '__main__':
    try:
        event = process.Event()

        t1 = process.Process(target=Worker, args=(1,))
        t2 = process.Process(target=Worker, args=(2,))
        

        t1.daemon = True
        t2.daemon = True

        t1.start()
        t2.start()
        
        event.wait()
        while True:
            pass

    except KeyboardInterrupt:
        event.set()
        sys.exit(1)
