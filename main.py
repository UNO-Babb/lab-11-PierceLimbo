#GroceryStoreSim.py
#Name: Pierce Limbo
#Date: 11/30/2025
#Assignment: Lab 11

import simpy
import random
eventLog = []           
waitingShoppers = []      
idleTime = 0            

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 20)
    shoppingTime = items * 0.5
    shoppingTime *= random.uniform(0.9, 1.1)
    yield env.timeout(shoppingTime)
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime

    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1)
        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items / 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((
            customer[0],   
            customer[1],   
            customer[2],   
            customer[3],   
            env.now        
        ))

def customerArrival(env):
    customerNumber = 0

    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2)

def processResults():
    totalWait = 0
    totalShopping = 0
    totalItems = 0
    maxWait = 0
    for e in eventLog:
        waitTime = e[4] - e[3]        
        shoppingTime = e[3] - e[2]    
        items = e[1]

        totalWait += waitTime
        totalShopping += shoppingTime
        totalItems += items
        maxWait = max(maxWait, waitTime)
    totalShoppers = len(eventLog)

    print("\n----- Simulation Results -----")
    print(f"Total shoppers checked out: {totalShoppers}")
    print(f"Average items purchased: {totalItems / totalShoppers:.2f}")
    print(f"Average shopping time: {totalShopping / totalShoppers:.2f} minutes")
    print(f"Average wait time: {totalWait / totalShoppers:.2f} minutes")
    print(f"Max wait time: {maxWait:.2f} minutes")
    print(f"Total idle time across checkers: {idleTime} minutes")

def main():
    numberCheckers = 5
    runtime = 180   
    env = simpy.Environment()
    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))
    env.run(until=runtime)
    processResults()


if __name__ == '__main__':
    main()
