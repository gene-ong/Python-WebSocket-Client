import websocket
import time
import cv2
import mss
import numpy
import websocket
import threading
from time import sleep
from pynput.mouse import Listener

startx = 0
starty = 0
finx = 0
finy = 0

def on_click(x, y, button, pressed):
    global startx
    global starty
    global finx
    global finy
    if pressed:
        
        startx = x
        starty = y
        print(startx)
        print(starty)
        
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))

    if not pressed:
        finx = x
        finy = y
        # Stop listener
        return False

def sendFrame():
        #ws.connect("ws://192.168.1.102/test")
        #last_time = time.time()
        
        # Get raw pixels from the screen, save it to a Numpy array
        # Numpy Array structure: [Height, Width, BLUE, GREEN, RED, ??] 
        img = numpy.array(sct.grab(monitor))
        # print('Original Dimensions : ',img.shape)

        # Display the picture
        #cv2.imshow("Selected Screen", img)
        
        #parameters of new image
        height = 8
        width = 10
        dim = (width, height)
    
        # resizing original image
        resized = cv2.resize(img, dim, interpolation =cv2.INTER_AREA)

        resized_new = numpy.empty_like(resized)
        #if m = 0, first pixel is on RHS, if m = 1, first pixel is on LHS
        m = 1
        while m<height:
            n = 0 
            while n<width:
                resized_new[m,n] = resized[m, 9-n]
                n += 1
            m += 2
        #create a string called chunk with all the pixels of the resized numpy array
        chunk = ''
        i = 0
        while i < height:
            y = 0
            while y < width:
                r = 0
                while r < 3:
                    chunk += chr(resized_new[i,y,r])
                    r += 1
                y += 1
            i += 1

        # Send Binary values over websocket
        ws.send_binary(chunk)
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
           cv2.destroyAllWindows()
        #print('sent binary chunk')

# Collect events until released
with Listener(
        on_click=on_click) as listener:
    listener.join()
    
with mss.mss() as sct:
   # Part of the screen to capture
    print(startx, starty, abs((startx - finx)), abs((starty - finy)))
    monitor = {"top": starty, "left": startx, "width": abs((startx - finx)), "height": abs((starty - finy))}
    #monitor = {"top": 400, "left": 0, "width": 400, "height": 400}
    ws = websocket.WebSocket()
    #first line if using local WiFi, second line if using ESP32 as an Access Point
    #ws.connect("ws://192.168.1.102/test")
    ws.connect("ws://192.168.4.1/")    
    while True:
        
        #i = 0
        #while i <=75:
        #print(i)
        try:
            sendFrame()
        #i +=1
            sleep(0.00)
        #print("1")
        except:
            try:
                ws.connect("ws://192.168.4.1/")           
            except:
                try:
                    ws = websocket.WebSocket()
                except:
                    ws = websocket.WebSocket()
                    ws.connect("ws://192.168.4.1/")
    ws.close()
    print("ws.close")
