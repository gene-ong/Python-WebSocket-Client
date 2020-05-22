import time

import cv2
import mss
import numpy

setBrightness = 0
setContrast= 0

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

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 100, "left": 400, "width": 26*3, "height": 64*4}

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = apply_brightness_contrast(numpy.array(sct.grab(monitor)), setBrightness, setContrast)
        
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
