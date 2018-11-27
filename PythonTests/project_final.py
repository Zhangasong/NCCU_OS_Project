import time
import threading 
import random

wID = 1 # initialize westbound car's ID
eID = 1 # initialize eastbound car's ID

def w_Job():
    while(True):
        global wID
        car = Car('w', wID)
        exp = random.expovariate(1/8)
        time.sleep(exp)
        car.start()
#       next_car = random.uniform(1,2)  # new car created time / float random (3,5)       
        wID += 1

def e_Job():
    while(True):
        global eID
        car = Car('e', eID)
        exp = random.expovariate(1/8)
        time.sleep(exp)
        car.start()
#       next_car = random.uniform(3,5)       
        eID += 1


class Bridge():

    sem = threading.Semaphore(5)
    cond = threading.Condition()
    CarOnBridge = 0


    def __init__(self):
        pass

    def crossBridge(self, Car):


        self.cond.acquire()

        print(Car.name + ' is WAITING to cross the bridge.')

        if(self.CarOnBridge == 0 or self.dir == Car.name[0]):
            self.CarOnBridge += 1
            self.dir = Car.name[0]
            self.cond.release()
        else:
            self.cond.release()
            while(True):

                if(self.CarOnBridge == 0):
                    self.CarOnBridge += 1
                    self.dir = Car.name[0]
                    print('Change the dir: ' + self.dir)
                    break
        
        # Crossing the bridge. 

        self.sem.acquire()

        print(Car.name + ' is CROSSING the bridge!')
        periods = random.uniform(3,5)  
        time.sleep(periods)  # the periods of crossing the bridge            
        print(Car.name + ' has LEFT the bridge.')

        self.CarOnBridge -= 1
        
        print("CarOnBridge = " + str(self.CarOnBridge))

        self.sem.release()
        
        
class Car(threading.Thread):
    
    def __init__(self, name, num):
        threading.Thread.__init__(self)
        self.name = name
        self.num = num

#    def getName(self):
#        return self.name

#    def setName(self):
#        self.name

    def run(self):

        if self.name == 'w':\
        
            self.name = ('Westbound car' + str(self.num))
            print(self.name)
            Bridge.crossBridge(Bridge,self)
        else:
            self.name = ('Eastbound car' + str(self.num)) 
            print(self.name)
            Bridge.crossBridge(Bridge, self)

def main():
    Western = threading.Thread(target = w_Job)
    Eastern = threading.Thread(target = e_Job)
    Western.start()
    Eastern.start()

if __name__=="__main__":
    main()
