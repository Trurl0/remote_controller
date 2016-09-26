import socket
import random
import time
import win32api, win32con, win32gui
import threading
import sys
import datetime

class Server():
    #Server with an unique client

    def __init__(self, Adress=("",5001), MaxClient=1):
    
      #Create shocket
      self.mySocket = socket.socket()
      #self.mySocket.settimeout(10000)
      self.mySocket.bind(Adress)
      self.mySocket.listen(MaxClient)
      
      #Get screen size for relative mouse positioning
      self.width = win32api.GetSystemMetrics(0)
      self.height = win32api.GetSystemMetrics(1)
      self.client_width = win32api.GetSystemMetrics(0) #Initialise equal by default, client should update this
      self.client_height = win32api.GetSystemMetrics(1) #Initialise equal by default, client should update this
        
      self.paused = False
     
    def waitForConnection(self):
      self.myClient, self.Adr = (self.mySocket.accept())
      print('Got a connection from: '+str(self.myClient)+'.')

    def getMsg(self):
      return self.myClient.recv(2048)

    def send(self, msg):
       self.myClient.send(msg)

    def left_click(self, x, y):
        corrected_x = int(x * self.width/self.client_width)
        corrected_y = int(y * self.height/self.client_height)
        
        win32api.SetCursorPos((corrected_x,corrected_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,corrected_x,corrected_y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,corrected_x,corrected_y,0,0)

    def left_click_down(self, x, y):
        corrected_x = int(x * self.width/self.client_width)
        corrected_y = int(y * self.height/self.client_height)
        
        win32api.SetCursorPos((corrected_x,corrected_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,corrected_x,corrected_y,0,0)
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,corrected_x,corrected_y,0,0)

    def left_click_up(self, x, y):
        corrected_x = int(x * self.width/self.client_width)
        corrected_y = int(y * self.height/self.client_height)
        
        win32api.SetCursorPos((corrected_x,corrected_y))
        #win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,corrected_x,corrected_y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,corrected_x,corrected_y,0,0)

    def right_click(self, x, y):
        corrected_x = int(x * self.width/self.client_width)
        corrected_y = int(y * self.height/self.client_height)
        
        win32api.SetCursorPos((corrected_x,corrected_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,corrected_x,corrected_y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,corrected_x,corrected_y,0,0)

    def keyPress(self, key):
        win32api.keybd_event(key,0,1,0)#Down
        win32api.keybd_event(key,0,2,0)#Up

    def move(self, x,y):
        corrected_x = int(x * self.width/self.client_width)
        corrected_y = int(y * self.height/self.client_height)
        
        win32api.SetCursorPos((corrected_x,corrected_y))
            
            
    def delayedPrint(self, *myargs):
        #For delay testing
        print "delayedPrint args:" +str(myargs)

    def setDelayedAction(self, delay_min, delay_max, action, *myargs):
        #Call the parameter function after a delay
        print "setDelayedAction args: " + str(myargs)
        delay = random.uniform(delay_min, delay_max)
        print "delay: " + str(delay)
        
        myThread = threading.Timer(delay, action, args = myargs)
        myThread.start()
        #myThread.join()#Don't close program with living thread
        
        
    def listen(self):
            
        msg = ""
        x=0
        y=0
            
        while msg != "exit" and  msg != "close":
        
            #get last message or wait for one
            msg = self.getMsg()
            #print msg
            
            try:
                #Dont take any actions if paused, still answer each msg with ack
                if self.paused:
                
                    #Check unpause
                    if msg == "pause":
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True
                        print "paused"
                        
                else:
                    #Do stuff based on message
                    if "screen_size" in msg:
                        self.client_width = int(msg.split(":")[1].split(",")[0])
                        self.client_height = int(msg.split(":")[1].split(",")[1])
                        
                    #PAUSE
                    elif msg == "pause":
                        if self.paused:
                            self.paused = False
                        else:
                            self.paused = True
                        print "paused"
                        
                    #CLICKS
                    elif msg == "left_click_down":
                        self.left_click_down(int(x), int(y))
                        print "left_click_down"
                    
                    elif msg == "left_click_up":
                        self.left_click_up(int(x), int(y))
                        print "left_click_up"
                    
                    elif msg == "right_click":
                        self.right_click(int(x), int(y))
                        print "right_click"
                        
                    elif "delayed_left_click" in msg:
                        myargs = (int(x), int(y))
                        try:
                            delay_min = float(msg.split(" ")[1])
                            delay_max = float(msg.split(" ")[2])
                            self.setDelayedAction(delay_min, delay_max, self.left_click, *myargs)
                            print "delayed_left_click"
                        except Exception:
                            pass#avoid buffered joint messages
                            
                    #KEYBOARD
                    elif msg == "enter":
                        self.keyPress(0x0D)
                        print msg
                    elif msg == "backspace":
                        self.keyPress(0x08)
                        print msg
                    elif msg == "0":
                        self.keyPress(ord("0"))
                        print msg
                    elif msg == "1":
                        self.keyPress(ord("1"))
                        print msg
                    elif msg == "2":
                        self.keyPress(ord("2"))
                        print msg
                    elif msg == "3":
                        self.keyPress(ord("3"))
                        print msg
                    elif msg == "4":
                        self.keyPress(ord("4"))
                        print msg
                    elif msg == "5":
                        self.keyPress(ord("5"))
                        print msg
                    elif msg == "6":
                        self.keyPress(ord("6"))
                        print msg
                    elif msg == "7":
                        self.keyPress(ord("7"))
                        print msg
                    elif msg == "8":
                        self.keyPress(ord("8"))
                        print msg
                    elif msg == "9":
                        self.keyPress(ord("9"))
                        print msg
                        
                    #MOUSE POSITION
                    elif "," in msg:
                        x = msg.split(",")[0]
                        y = msg.split(",")[1]
                        self.move(int(x), int(y))
                    
                    #Any key
                    else:
                        if(len(msg) == 1):
                            self.keyPress(ord(msg))
                            print msg
                        
                #Send ack after each message recieved from client (even if paused)
                self.send("ack")
                
            except Exception:
                "Error: " + msg
        #return las message to check close instruction
        return msg
        
if __name__=="__main__":
    
    #Trial period protection
    day_limit = 30
    start_day = datetime.date(2016, 9, 23)
    today = datetime.date.today()
    delta = today - start_day
    if delta.days < day_limit:
        
        if len(sys.argv) > 1:
            #Specify port, IP is empty (accept all connections)
            ser=Server(Adress=("", int(sys.argv[1])))
            
        else:
            #Default IP and port "", 5001
            ser=Server()

        while True:
            print "Waiting for connection"
            ser.waitForConnection()
        
            #Keep listening to client until socket is closed
            check = ser.listen()
            print "\nConnection closed"
            if check == "exit":
                break
        
    else:
        print "Sorry, the trial period is over" 
        