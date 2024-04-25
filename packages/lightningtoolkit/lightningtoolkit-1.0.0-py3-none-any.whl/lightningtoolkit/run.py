import math,random
from time import sleep
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
day_ending = ['st','nd','rd'] + 17* ['th'] + ['st','nd','rd'] + 8* ['th']
chancer = 1
chance = 3
chancers = 10 

def logo() :
    print('_____                                           _____                   ______                                                                   ')
    print('|   |                                           |   |                   |    |                                                                    ')
    print('|   |                                           |   |                   |    |                                                                    ')
    print('|   |                                           |   |                   |    |                                                                    ')
    print('|   |                                           |   |                   |    |                                                                    ')
    print('|   |                                           |   |                   |    |                                                                    ')
    print('|   |                _____                      |   |                   |    |                         _____                                      ')
    print('|   |                |   |                      |   |                   |    |                         |   |                                      ')
    print('|   |                |___|                      |   |                   |    |                         |___|                                      ')
    print('|   |                _____  __________________  |   |____________  _____|    |_____  ________________  _____  _______________  ___________________')
    print('|   |                |   |  |                |  |               |  |              |  |              |  |   |  |             |  |                 |')
    print('|   |                |   |  |   __________   |  |   ________    |  |____      ____|  |   ________   |  |   |  |   _______   |  |   __________    |')
    print('|   |                |   |  |   |        |   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |        |    |')
    print('|   |                |   |  |   |        |   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |        |    |')
    print('|   |                |   |  |   |        |   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |        |    |')
    print('|   |                |   |  |   |        |   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |        |    |')
    print('|   |                |   |  |   |        |   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |        |    |')
    print('|   |______________  |   |  |   |________|   |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |   |________|    |')
    print('|                 |  |   |  |                |  |   |       |   |       |    |       |   |      |   |  |   |  |   |     |   |  |                 |')
    print('|_________________|  |___|  |_____________   |  |___|       |___|       |____|       |___|      |___|  |___|  |___|     |___|  |_____________    |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                                         |   |                                                                                               |   |')
    print('                            _____________|   |                                                                                 ______________|   |')
    print('                            |                |                                                                                 |                 |')
    print('                            |________________|                                                                                 |_________________|')

def judge2(interval) :
    while True:
        try:r1_i = int(input('go back?(yes:1, no:2): '));break
        except:print("Enter Error")
    if r1_i == 1 :
        pass
    else :
        interval()

def judge() :
    while True:
        try:program = int(input('''
1_date  2_dice   3_timer(foward)   4_timer(back)   5_calculator   6_exit
please choose program:'''));break
        except:print("Enter Error")
    if program == 1 :
        date()
    elif program == 2 :
        dice()
    elif program == 3 :
        timer2()
    elif program == 4 :
        timer3()
    elif program == 5 :
        calculator()
    elif program == 6 :
        exit()
    else :
        print('No program named %d'%program)

def date() :
    while True:
        try:
            year = input('enter year: ')
            int(year)
            break
        except:print("Enter Error")
    while True:
        try:
            month_int = int(input('enter month: '))
            assert month_int <= 12 and month_int >= 1
            break
        except:print("Enter Error")
    while True:
        try:
            day_int = int(input('enter day: '))
            assert day_int <= 32 and day_int >= 1
            break
        except:print("Enter Error")
    Month = months[month_int -1]
    Day = str(day_int) + day_ending[day_int -1]
    print(Month + ' ' + Day + ' , ' + year)
    judge2(date)

def dice() :
    while True:
        try:
            tti = input('please enter random times: ')
            tt = int(tti)
            break
        except:print("Enter Error")
    while True:
        try:
            ti2 = input("please enter the number of faces on a dice: ")
            t2 = int(ti2)
            break
        except:print("Enter Error")
    ls = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0, 17:0, 18:0, 19:0, 20:0, 21:0, 22:0, 23:0, 24:0, 25:0, 26:0, 27:0, 28:0, 29:0, 30:0, 31:0, 32:0, 33:0, 34:0, 35:0, 36:0, 37:0, 38:0, 39:0, 40:0, 41:0, 42:0, 43:0, 44:0, 45:0, 46:0, 47:0, 48:0, 49:0, 50:0}
    for i in range(tt) :
        dice2 = math.ceil(random.random()*t2)
        ls[dice2] += 1
    print(ls)
    judge2(dice)

def timer2(l = True) :
    if l:
        time2 = input('please enter second(s)(limitless:l): ')
    else:time2 = "l"
    if 'l' in time2 :
        while True:
            try:
                time2_1 = input('please enter the stop inquiry interval(numbers) :')
                time2_3 = int(time2_1)
                break
            except:print("Enter Error")
        time2_2 = 0
        while True :
            for i in range(time2_3) :
                sleep(1)
                time2_2 += 1
                print("%d second(s)"%time2_2)
            while True:
                try:
                    time2_4 = input("stop?(stop:1, don't stop:2): ")
                    time2_5 = int(time2_4)
                    break
                except:print("Enter Error")
            if time2_5 == 1 :
                break
    else :
        while True:
            try:
                time2_6 = int(time2)
                break
            except:
                print("Enter Error")
                time2 = input('please enter second(s)(limitless:l): ')
                if "l" in time2:
                    timer2(False)
        time2_7 = 0
        while time2_7 != time2_6 :
            sleep(1)
            time2_7 += 1
            print("%d second(s)"%time2_7)
    judge2(timer2)

def timer3() :
    while True:
        try:
            time1 = input('please enter seconds(s): ')
            time3 = int(time1)
            break
        except:print("Enter Error")
    print("%d second(s)"%time3)
    while time3 != 0 :
        sleep(1)
        time3 -= 1
        print("%d second(s)"%time3)
    judge2(timer3)

def calculator() :
    while True:
        try:
            print(eval(input('please enter formula: ')))
            break
        except:print("Enter Error")
    judge2(calculator)

def run():
    logo()
    while True:judge()

run()