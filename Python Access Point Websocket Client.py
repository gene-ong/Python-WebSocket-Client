import websocket
import time
import cv2
import mss
import numpy
import websocket
import threading
from time import sleep
from pynput.mouse import Listener
#import logging
#logging.basicConfig(format='%(asctime)s %(message)s')

startx = 0
starty = 0
finx = 0
finy = 0
nbOfLEDsCol = int(input('Define the number of LEDs in each column '))
nbOfLEDsRow = int(input('Define the number of LEDs in each row '))

LEDMatrixConfig = int(input('How is the matrix configured? 1 = LEDs snake from row to row, 2 = LEDs all start on same side'))
startingPosition = int(input('Where is the first LED? 1 = TOP LEFT, 2 = TOP RIGHT, 3 = BOTTOM LEFT, 4 = BOTTOM RIGHT '))
setBrightness = int(input('Set Brightness between -255 and +255 '))
setContrast = int(input('Set Contrast between -127 and +127 '))

##nbOfLEDsCol = 64
##nbOfLEDsRow = 26
##
##LEDMatrixConfig = 1
##startingPosition = 3
##setBrightness = int(input('Set Brightness between -255 and +255 '))
##setContrast = int(input('Set Contrast between -127 and +127 '))



#parameters of new image
height = nbOfLEDsCol
width = nbOfLEDsRow
dim = (width, height)

print('This display has ', nbOfLEDsCol*nbOfLEDsRow, ' LEDs')

print('Select an area of the screen with your mouse. Click and hold the LEFT mouse button, dragging the cursor over the area you wish to display')

def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def on_click(x, y, button, pressed):
    global startx
    global starty
    global finx
    global finy
    if pressed:
        
        startx = x
        starty = y
        print('first click startx = ', startx)
        print('first click starty = ', starty)

        
    #print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))

    if not pressed:
        print('released click finx = ', x)
        print('released click finy = ', y)
        if startx < x:
            finx = x
        else:
            finx = startx
            startx = x
        if starty < y:
            finy = y
        else:
            finy = starty
            starty = y
        print('startx = ',startx)
        print('finx = ',finx)
        print('starty = ',starty)
        print('finy = ',finy)
        # Stop listener
        return False

def sendFrame():
        # Get raw pixels from the screen, save it to a Numpy array
        # Numpy Array structure: [Height, Width, BLUE, GREEN, RED, ??] 
        img = numpy.array(sct.grab(monitor))
        adjustedImg = apply_brightness_contrast(img,setBrightness,setContrast)
        # print('Original Dimensions : ',img.shape)

        # Display the picture
        #cv2.imshow("Selected Screen", img)
        # resizing original image
        resized = cv2.resize(adjustedImg, dim, interpolation =cv2.INTER_AREA)
        #resized = cv2.resize(img, dim, interpolation =cv2.inter)
        resized_new = numpy.empty_like(resized)
                       
        #create a string called chunk with all the pixels of the resized numpy array
        chunk = ''
            
        #if m = 0, first pixel is on RHS, if m = 1, first pixel is on LHS
        
        m = 0
        while m<height:
            n = 0                     
            while n<width:
                
                if LEDMatrixConfig == 1:
                    if startingPosition == 1:
                        if (m % 2) != 0:
                            resized_new[m,n] = resized[m, (width -1)-n]
                    elif startingPosition == 2:
                        if (m % 2) == 0:
                            resized_new[m,n] = resized[m, (width -1)-n]
                    elif startingPosition == 3:
                        if (m % 2) != 0:
                            resized_new[m,n] = resized[(height-1) - m, (width -1)-n]
                        else:
                            resized_new[m,n] = resized[(height-1) - m, n]
                    elif startingPosition == 4:
                        if (m % 2) == 0:
                            resized_new[m,n] = resized[(height-1) - m, (width -1)-n]
                        else:
                            resized_new[m,n] = resized[(height-1) - m, n]

                elif LEDMatrixConfig == 2:
                    if startingPosition == 1:
                        resized_new[m,n] = resized[m, n]
                    elif startingPosition == 2:
                        resized_new[m,n] = resized[m, (width -1)-n]
                    elif startingPosition == 3:
                        resized_new[m,n] = resized[(height-1) - m, n]
                    elif startingPosition == 4:
                        resized_new[m,n] = resized[(height-1) - m, (width -1)-n]
                r = 0
                while r < 3:
                    chunk += chr(resized_new[m,n,r])
                    r += 1
                n += 1
            m += 1
        
  


        # Send Binary values over websocket
        ws.send_binary(chunk)
        #logging.warning('is when this event was logged.')
        # Press "q" to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
           cv2.destroyAllWindows()
        #print('sent binary chunk')

# Collect events until released
with Listener(
        on_click=on_click) as listener:
    listener.join()
    
with mss.mss() as sct:
   # Part of the screen to capture
    #print(startx, starty, abs((startx - finx)), abs((starty - finy)))
    print('Screen capturing successfully started')

    #Use this for UI Mouse Selection
    monitor = {"top": starty, "left": startx, "width": abs((startx - finx)), "height": abs((starty - finy))}

    #For testing, set screen capture area around the size of the UTS Tower
    #monitor = {"top": 10, "left": 600, "width": 590, "height": 700}

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
