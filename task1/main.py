
import time     
import random

n = 1000000     # value of iterstions
hist = [0]*10   # size of histogram
work_time = [0]*100     # list of 100 work times

def initListWithRandomNumbers():    
    rand_list = []
    for i in range(n):
        rand_list.append(random.randint(0,999))
    return rand_list

def calcHist(tdata):    # calculation of hist
    for i in range(n):
        hist[(tdata[i] // 100)] += 1


def workHundredTimes(): # func 

    for i in range(100):
        rand = initListWithRandomNumbers() # init of rand list
        start = time.time()     # start time
        calcHist(rand)      # calcultion of hist
        end = time.time()      # end time

        work_time[i] = end - start  # put time of work

    work_time.sort() # sort work time ASC


if __name__ == '__main__':
    workHundredTimes()
    #print(work_time) 
    print(str(round(work_time[49], 3)) + " s") # average work time


