import time

import cv2
import mss
import numpy
from pynput.mouse import Listener
i=0
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

# Collect events until released
with Listener(
        on_click=on_click) as listener:
    listener.join()

print(startx, starty, (startx - finx), (starty - finy))
with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": startx, "left": starty, "width": abs((startx - finx)), "height": abs((starty - finy))}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        # print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
        #break
