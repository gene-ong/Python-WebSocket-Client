import websocket
import time
import cv2
import mss
import numpy
import websocket
import threading
from time import sleep


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

        
        ws.send_binary(chunk)
        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
           cv2.destroyAllWindows()
        #print('sent binary chunk')
           
with mss.mss() as sct:
    
    monitor = {"top": 300, "left": 300, "width": 1000, "height": 400}
    ws = websocket.WebSocket()
    #first line if using local WiFi, second line if using ESP32 as an Access Point
    #ws.connect("ws://192.168.1.102/test")
    
        
    
    ws.connect("ws://192.168.4.1/")    
    while True:
        
        sendFrame()
        
        sleep(0.00)
        #print("Just slept")
    ws.close()
