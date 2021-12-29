from threading import Thread, Lock
from time import sleep

counter = 0

def increase(by, lock):
    global counter

    # acquire lock before access to counter variable
    lock.acquire()

    local_counter = counter
    local_counter += by

    sleep(0.1)

    counter = local_counter
    print('counter={}'.format(counter))

    #release lock after updating the new value
    lock.release()

# lock() instance
lock = Lock()

# create threads
t1 = Thread(target=increase, args=(10, lock))
t2 = Thread(target=increase, args=(20, lock))

# start the threads
t1.start()
t2.start()


# wait for the threads to complete
t1.join()
t2.join()


print('The final counter is {}'.format(counter))