# encoding: utf-8
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import itchat

"""set itchat to login in wechat"""
itchat.auto_login(hotReload=True)
rooms = itchat.get_chatrooms(update=True)
rooms = itchat.search_chatrooms(name='aaa')
if rooms is not None:
    username = rooms[0]['UserName']
else:
    username = 'filehelper'
    
"""set GPIO"""
GPIO.setmode(GPIO.BCM)
R,G,Y = 20,21,16
FIRE = 22
SMOKE = 27
FMQ = 4
def afmq():
    GPIO.setup(FMQ,GPIO.OUT)
    GPIO.output(FMQ,GPIO.HIGH)

def bfmq():
    GPIO.setup(FMQ,GPIO.OUT)
    GPIO.output(FMQ,GPIO.LOW)
if __name__ == '__main__':
    #itchat.run()
    c = 4
    try:
        while (True):
            GPIO.setup(SMOKE,GPIO.IN)
            GPIO.setup(FIRE,GPIO.IN)
            GPIO.setup(R,GPIO.OUT)
            GPIO.setup(G,GPIO.OUT)
            GPIO.setup(Y,GPIO.OUT)
            #GPIO.setup(FMQ,GPIO.OUT)
            #f = GPIO.input(FIRE)
            #y = GPIO.input(SMOKE)
            if GPIO.input(SMOKE) == GPIO.LOW:
                #GPIO.output(FMQ,GPIO.HIGH)
                afmq()
                GPIO.output(G,GPIO.LOW)
                GPIO.output(Y,GPIO.HIGH)
                u = "检测到有害气体！"
                m = 1
                if GPIO.input(FIRE) == GPIO.LOW:
                    #GPIO.output(FMQ,GPIO.HIGH)
                    afmq()
                    GPIO.output(R,GPIO.HIGH)
                    u = "检测到有害气体和火焰！"
                    m = 3
                if GPIO.input(FIRE) == GPIO.HIGH:
                    GPIO.output(R,GPIO.LOW)

            if GPIO.input(SMOKE) == GPIO.HIGH:
                GPIO.output(Y,GPIO.LOW)
                if GPIO.input(FIRE) == GPIO.LOW:
                    #GPIO.output(FMQ,GPIO.HIGH)
                    afmq()
                    GPIO.output(G,GPIO.LOW)
                    GPIO.output(R,GPIO.HIGH)
                    u = "检测到火焰！"
                    m = 2
                if GPIO.input(FIRE) == GPIO.HIGH:
                    #GPIO.output(FMQ,GPIO.LOW)
                    bfmq()
                    GPIO.output(R,GPIO.LOW)
                    GPIO.output(G,GPIO.HIGH)
                    u = "无异常~"
                    m = 4
                    
            if m != c:
                if m == 1:
                    #if rooms is not None:
                        #username = rooms[0]['UserName']
                        itchat.send(str(u),toUserName=username)
                        c = 1
                        continue
                if m == 2:
                    #if rooms is not None:
                        #username = rooms[0]['UserName']
                        itchat.send(str(u),toUserName=username)
                        c = 2
                        continue
                if m == 3:
                    #if rooms is not None:
                        #username = rooms[0]['UserName']
                        itchat.send(str(u),toUserName=username)
                        c = 3
                        continue
                if m == 4:
                        itchat.send(str(u),toUserName=username)
                        c = 4
            else:
                continue
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        GPIO.cleanup()
