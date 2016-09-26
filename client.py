import socket
import random
import time
import win32api, win32con, win32gui
import sys
import datetime
import getpass

class Client():
    def __init__(self, Adress=("127.0.0.1",5001)):#"192.168.20.40", "127.0.0.1"

        #Connect to server shocket (must exist)
        self.mysocket = socket.socket()
        #self.mySocket.settimeout(10000)
        self.mysocket.connect(Adress)
   
        #Get screen size for relative mouse positioning
        self.width = win32api.GetSystemMetrics(0)
        self.height = win32api.GetSystemMetrics(1)

    def sendMsg(self, msg):
        #Send string to server
        self.mysocket.send(msg)
        
      
    def sendMousePos(self):
        #Send relative mouse position
        x, y = win32api.GetCursorPos()
        self.mysocket.send(str(x) + "," + str(y))
      
    def listen(self):
        return self.mysocket.recv(2048)

    def forward(self):
        
        #Send screen size to server
        self.sendMsg("screen_size:"+str(cli.width) + "," +str(cli.height))
        
        time.sleep(0.1)
        
        #Only one message sent per state change
        delayed_left_click_once = True
        letter_once = True
        left_once = True
        left_once_up = True
        right_once = True
        enter_once = True
        backspace_once = True
        pause_once = True
        zero_once = True
        one_once = True
        two_once = True
        three_once = True
        four_once = True
        five_once = True
        six_once = True
        seven_once = True
        eight_once = True
        nine_once = True
        
        #Press Esc or 'E' to break 
        while True:
            
            
            #Close connection ESC (0x1B is Esc key)
            if win32api.GetAsyncKeyState(0x1B)  != 0:
            #or win32api.GetAsyncKeyState(ord('E')) != 0:  #Esc key
                self.sendMsg("exit")
                #self.sendMsg("close")
                break
                
            #Close connection and shutdown server
            if win32api.GetAsyncKeyState(ord('C')) != 0: 
                self.sendMsg("close")
                break
            
            
            #PAUSE
            if win32api.GetAsyncKeyState(ord('P')) != 0: 
                if pause_once:
                    self.sendMsg("pause")
                    pause_once = False
            else:
                pause_once = True
            
            #Letters
            if win32api.GetAsyncKeyState(ord('O')) != 0: 
                if letter_once:
                    self.sendMsg("O")
                    letter_once = False
            elif win32api.GetAsyncKeyState(ord('I')) != 0: 
                if letter_once:
                    self.sendMsg("I")
                    letter_once = False
            else:
                letter_once = True
            
            
            #MOUSE POSITION
            self.sendMousePos()
            
            
            #CLICKS
            if win32api.GetAsyncKeyState(0x01) != 0:
                if left_once:
                    self.sendMsg("left_click_down")
                    left_once = False
            else:
                left_once = True
                
            #print "GetAsyncKeyState: " + str(win32api.GetAsyncKeyState(0x01)) + " GetKeyState: " + str(win32api.GetKeyState(0x01))
            if win32api.GetAsyncKeyState(0x01) == 0:
                if left_once_up:
                    self.sendMsg("left_click_up")
                    left_once_up = False
            else:
                left_once_up = True
                                              
            if win32api.GetAsyncKeyState(0x02) != 0:
                if right_once:
                    self.sendMsg("right_click")
                    right_once = False
            else:
                right_once = True
                
            #Single left click with random delay (1, 3)
            if win32api.GetAsyncKeyState(ord("D")) == 0:
                if delayed_left_click_once:
                    self.sendMsg("delayed_left_click 1 3")
                    delayed_left_click_once = False
            else:
                delayed_left_click_once = True
                
                
            #ENTER (0x0D)
            if win32api.GetAsyncKeyState(0x0D) != 0:
                if enter_once:
                    self.sendMsg("enter")
                    enter_once = False
            else:
                enter_once = True
                
            #BACKSPACE (0x08)
            if win32api.GetAsyncKeyState(0x08) != 0:
                if backspace_once:
                    self.sendMsg("backspace")
                    backspace_once = False
            else:
                backspace_once = True
                
                
            #NUMBERS
            if win32api.GetAsyncKeyState(ord('0')) != 0:
                if zero_once:
                    self.sendMsg("0")
                    zero_once = False
            else:
                zero_once = True
                
            if win32api.GetAsyncKeyState(ord('1')) != 0:
                if one_once:
                    self.sendMsg("1")
                    one_once = False
            else:
                one_once = True
                
            if win32api.GetAsyncKeyState(ord('2')) != 0:
                if two_once:
                    self.sendMsg("2")
                    two_once = False
            else:
                two_once = True
                
            if win32api.GetAsyncKeyState(ord('3')) != 0:
                if three_once:
                    self.sendMsg("3")
                    three_once = False
            else:
                three_once = True
                
            if win32api.GetAsyncKeyState(ord('4')) != 0:
                if four_once:
                    self.sendMsg("4")
                    four_once = False
            else:
                four_once = True
                
            if win32api.GetAsyncKeyState(ord('5')) != 0:
                if five_once:
                    self.sendMsg("5")
                    five_once = False
            else:
                five_once = True
                
            if win32api.GetAsyncKeyState(ord('6')) != 0:
                if six_once:
                    self.sendMsg("6")
                    six_once = False
            else:
                six_once = True
                
            if win32api.GetAsyncKeyState(ord('7')) != 0:
                if seven_once:
                    self.sendMsg("7")
                    seven_once = False
            else:
                seven_once = True
                
            if win32api.GetAsyncKeyState(ord('8')) != 0:
                if eight_once:
                    self.sendMsg("8")
                    eight_once = False
            else:
                eight_once = True
                
            if win32api.GetAsyncKeyState(ord('9')) != 0:
                if nine_once:
                    self.sendMsg("9")
                    nine_once = False
            else:
                nine_once = True
                
                
            #Chill a bit
            time.sleep(0.01)
            
            #Wait for ack from server
            self.listen()#print self.listen()
            
        
        #Just in case
        self.sendMsg("end")
        
    
        
        
if __name__=="__main__":

    #Trial period protection
    #day_limit = 30
    #start_day = datetime.date(2016, 9, 23)
    #today = datetime.date.today()
    #delta = today - start_day
    #if delta.days < day_limit:
    
        #password = getpass.getpass("Pasword:")
        #while password != "":
        #    print "Incorrect, try again"
        #    password = getpass.getpass("Pasword:")
        #print "Ok"
            
        if len(sys.argv) > 2:
            #Specify IP and Port
            cli=Client(Adress=(sys.argv[1], int(sys.argv[2])))
            
        elif len(sys.argv) > 1:
            #Specify IP, defalt port is 5001
            cli=Client(Adress=(sys.argv[1],5001))
            
        else:
            #Default IP and port "127.0.0.1", 5001
            cli=Client()
            
        print "Connection established"
        cli.forward()
        
    #else:
        #print "Sorry, the trial period is over" 
        