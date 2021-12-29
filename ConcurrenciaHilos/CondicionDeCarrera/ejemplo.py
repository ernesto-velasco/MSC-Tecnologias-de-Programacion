from threading import Thread
from time import sleep

counter = 0

def increase(by):
    global counter

    local_counter = counter
    local_counter += by

    sleep(0.1)

    counter = local_counter
    print('\tCounter = {}'.format(counter))
    
# create threads
t1 = Thread(target=increase, args=(10,))
t2 = Thread(target=increase, args=(20,))

# start the threads
t1.start()
t2.start()

# wait for the threads to complete
t1.join()
t2.join()


print('\tThe final counter is {}'.format(counter))
