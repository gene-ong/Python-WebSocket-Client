#integrating WEbsockets and screen capture
from pynput.mouse import Listener

import time

import cv2
import mss
import numpy
import websocket

with mss.mss() as sct:

    monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    ws = websocket.WebSocket()
    ws.connect("ws://192.168.1.102/test")

    while "Screen capturing":
       
        #ws.connect("ws://192.168.1.102/test")
        #last_time = time.time()
        
        # Get raw pixels from the screen, save it to a Numpy array
        # Numpy Array structure: [Height, Width, BLUE, GREEN, RED, ??] 
        img = numpy.array(sct.grab(monitor))
        # print('Original Dimensions : ',img.shape)

        #parameters of new image
        height = 8
        width = 10
        dim = (width, height)
    
        # resizing original image
        resized = cv2.resize(img, dim, interpolation =cv2.INTER_AREA)

        resized_new = numpy.empty_like(resized)
 
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
        #ws.close()
    
        
    

    
