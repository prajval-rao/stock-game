import os
import random
import time
import threading
import matplotlib.pyplot as plt
global stock, hold_status, bought_price, sold_price, account, lock, scale, income, profit, x_axis, y_axis, plotstart, change
# Initial stock price
stock = 1000.00
# To check if the user bought a stock or not
hold_status = False
# Progress trackers
account, bought_price, sold_price = 2000, 0, 0
scale = 1
income = 0
profit = 0
# To ensure that values are updated correctly without interference of other functions
lock = threading.Lock()
# Graph plotting
x_axis = [0]
y_axis = [1000]
plotstart = 0
change = 0
os.system("cls")

def clear_screen(): # Command-line output live updating
    os.system("cls")

def stock_price():
    # To ensure smooth flow of the program, there are delays put in-place
    time.sleep(7)
    global stock, hold_status, bought_price, sold_price, account, lock, scale, income, profit, x_axis, y_axis, plotstart, change
    while True:
        with lock:
            clear_screen()
            plotstart += 1
            # Coarse randomiser (determines to what extent stock should change)
            scope = random.randint(1,100)
            if scale >= 1.01 and scale <= 2.5:
                scale = scale * 1.001
            if scale >= 2.5:
                scale = scale * 0.997
            # Fine randomisers (determines exact stock change)
            # Low change
            if scale < 0.5:
                scale = scale * 11
                stock += 100
            if scope >= 1 and scope <= 8: # 1-8
                change = random.randint(-175, 160)
                if change < 0:
                    scale = scale * 0.95 # inactive
                if change > 0:
                    scale = scale * 1.05
            # Lower-middle change
            elif scope > 8 and scope <= 35: # 8-35
                change = random.randint(-350, 300) * scale
                if change < 0:
                    scale = scale * 0.997
                if change > 0:
                    scale = scale * 1.003
            # Middle change
            elif scope > 35 and scope <= 71: # 40-71
                change = random.randint(-580, 520) * scale
                if change < 0:
                    scale = scale * 0.9958
                if change > 0:
                    scale = scale * 1.0042
            # Upper-middle change
            elif scope > 71 and scope <= 92: # 71-92
                change = random.randint(-640, 600) * scale * scale
                if change < 0:
                    scale = scale * 0.994
                if change > 0:
                    scale = scale * 1.006
            # Upper change
            else:
                change = random.randint(-950, 1250) * scale #95-100
                if change < 0:
                    scale = scale * 0.9905
                if change > 0:
                    scale = scale * 1.0095 #inactive
            if stock + change < 0:
                stock = scale*50
            else: # stock change here
                stock += change
            if stock < 200:
                stock += scale * 500
            if stock > 10000:
                scale = scale * 0.6
            # Command-line display output
            print("Stock price: ", end = "")
            # Determine if stock went up or down from last iteration
            if change > 0:
                print(f" {stock:.2f} 🔼")
            elif change < 0:
                print(f" {stock:.2f} 🔽")
            else:
                print(f" {stock:.2f} —")
            # Display of progress
            print(f"Last bought price: {bought_price:.2f}")
            if hold_status == False: # To see last profit when interacting with stock
                print(f"Last sold price:  {sold_price:.2f}")
                print(f"Last profit: {(sold_price - bought_price):.2f}")
            print(f"Account balance: {account:.2f}")
            print(f"Regular income gains: {income:.2f}")
            print(f"Regular income gain this time: {(80 * scale):.2f}")
            if hold_status == False: # To see if profit made from latest buy of stock
                print(f"Stock profit: {profit:.2f}")
            # Adds regular income to overall total (account is overall total (stock profit + regular income))
            account += 80 * scale
            # Adds regular income to total earnt from regular income excluding stock profit
            income += 80 * scale
            # For plotting
            x_axis.append(plotstart)
            y_axis.append(stock)  # plt.show() alternative
            # Graph plot limiter, to only display latest 20 stock changes
            if len(x_axis) == 20:
                x_axis = x_axis[1:]
                y_axis = y_axis[1:]
            time.sleep(2)

def user_input():
    # To ensure smooth flow of the program, there are delays put in-place
    time.sleep(7)
    global stock, hold_status, bought_price, sold_price, account, lock, scale, income, profit, x_axis, y_axis, plotstart, change
    while True:
        # Decision to buy or sell
        decision = input("\n")
        if hold_status:
            sold_price = stock
            account += sold_price
            profit += (sold_price - bought_price)
        else:
            if stock > account:
                print("Not enough cash. ")
            else:
                bought_price = stock
                account -= bought_price
        hold_status = not hold_status
        
# daemon used as user interaction not involved
thread1 = threading.Thread(target = stock_price, daemon = True)
thread2 = threading.Thread(target = user_input)
thread1.start()
thread2.start()
x_axis.append(plotstart)
y_axis.append(stock)
plt.ion()
plt.figure()
while True:
    plt.clf()
    if hold_status: # Displays colours based on profit made
        if bought_price < stock:
            plt.plot(x_axis, y_axis, color = "green")  
        elif bought_price > stock:
            plt.plot(x_axis, y_axis, color = "red")
        else:
            plt.plot(x_axis, y_axis, color = "gray")
    else: # Displays colours based on change from last stock price
        if change > 0:
            plt.plot(x_axis, y_axis, color = "green")
        elif change < 0:
            plt.plot(x_axis, y_axis, color = "red")
        else:
            plt.plot(x_axis, y_axis, color = "gray")
    if max(y_axis) > 100000:
        plt.ylim([0, max(y_axis) + (max(y_axis))/200]) 
    elif max(y_axis) > 10000:
        plt.ylim([0, max(y_axis) + (max(y_axis))/20]) 
    else:
        plt.ylim([0, max(y_axis) + (max(y_axis))/2]) 
    plt.pause(0.1) # plt.show() alternative but doesn't work
    time.sleep(0.1)
    


