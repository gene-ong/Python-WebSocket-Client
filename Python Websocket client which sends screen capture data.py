#integrating WEbsockets and screen capture
from pynput.mouse import Listener

import time

import cv2
import mss
import numpy
import websocket

with mss.mss() as sct:
    # Part of the screen to capture
##    boxSetup = 0
##    top = 0
##    left = 0
##    width = 0 
##    height = 0
##    if boxSetup != 1:
##        def on_move(x, y):
##            print("Mouse moved to ({0}, {1})".format(x, y))
##        def on_click(x, y, button, pressed):
##            while pressed:
##                print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
##                top = y
##                left = x
##                boxSetup = 1
##                print('boxSetup =', boxSetup)
##                print('top =', top)
##                print('left =', left)
##                
##            width = y - top
##            height = x - left
##            print('y =', y)
##            print('x =', x)
##            break
##        def on_scroll(x, y, dx, dy):
##            print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
##        with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
##            listener.join()

    monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    ws = websocket.WebSocket()
    ws.connect("ws://192.168.1.102/test")

    while "Screen capturing":
       
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        # Numpy Array structure: [Height, Width, BLUE, GREEN, RED, ??] 
        img = numpy.array(sct.grab(monitor))
        # print('Original Dimensions : ',img.shape)

        #parameters of new image
        width = 10
        height = 8
        dim = (width, height)

        #resizing original image
        resized = cv2.resize(img, dim, interpolation =cv2.INTER_AREA)
        # print('Resized Dimensions: ',resized.shape)

        #Change one pixel for testing
        #img[320,400] = [255,255,255,0]

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)
        #cv2.imshow("OpenCV/Numpy normal", resized)

        #checking out parameters of image from screen capture
        #print(type(img))
        #print(img.shape)
        #print(img[0,300])
        
        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
           cv2.destroyAllWindows()
        
        #send resized image over socket
        # print(' BGR Values Sent in decimal :',resized[0,0,0],resized[0,0,1],resized[0,0,2] )
        #print('Sent in character :' chr(resized[0,0,0]), chr(resized[0,0,1]), chr(resized[0,0,2]))
        # I need to make a string of 3 bytes
        #output = 1
        #ws.send('123456')
        
        blue = int(resized[0,0,0])
        ws.send_binary(chr(blue))
        # print(resized[0,0,0])

        ws.send_binary(chr(resized[0,0,1]))
        # print(resized[0,0,1])

        ws.send_binary(chr(resized[0,0,2]))
        # print(resized[0,0,2])
        
        # ws.send(resized)
        
    ws.close()

    
