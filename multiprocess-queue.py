import multiprocessing as mp
import sys
import os
import time
sem = mp.Semaphore(2)

b1 = int(0)
b2 = int(0)

def worker(num1, num2, q_receive, q_transmit, mem):
    global b1,b2
    while True:
        print("Process {0}  PID : {1}".format(num1, os.getpid()))
        sem.acquire()
        q_transmit.put(1)
        print("send data to Procsess {0}".format(num2))
        print("Process {0} Adder".format(num1))
        temp = int(q_receive.get())
        sem.release()
        if num1 == 1:
            b1 += temp
            print("b1 result : "+ str(b1))
        else:
            b2 +=temp
            print("b2 result : "+ str(b2))
        print()
        time.sleep(1)
    

if __name__ == '__main__':
    q1 = mp.Queue()
    q2 = mp.Queue()
    # lock = mp.Lock()
    event = mp.Event()

    try:
        p1 = mp.Process(target=worker, args=(1,2,q1,q2,b1))
        p2 = mp.Process(target=worker, args=(2,1,q2,q1,b2))

        p1.daemon = True
        p2.daemon = True

        p1.start()
        p2.start()

        p1.join()
        p2.join()

        event.wait()
        while True:
            pass

    except KeyboardInterrupt:
        event.set()
        q1.close()
        q2.close()
        sys.exit(1)