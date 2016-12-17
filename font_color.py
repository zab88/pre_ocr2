#!/usr/bin/env python

'''
HSV color selector.
Usage:
  font_color.py [<image>]
Keys:
  ESC   - exit
'''

import numpy as np
import cv2

if __name__ == '__main__':
    import sys
    try:
        fn = sys.argv[1]
    except:
        # fn = 'movie_01/Xiang-00-00-00-00.png'
        print(__doc__)
        sys.exit()

    img = cv2.imread(fn, True)
    img = cv2.pyrUp(img)
    if img is None:
        print('Failed to load image file:', fn)
        sys.exit(1)

    h, w, channels = img.shape[:3]
    isUpdated = False

    def update(dummy=None):
        flooded = img.copy()
        hl = np.zeros((h, w, channels), np.uint8)
        hl[:,:,:] = (0, 0, 255)
        # mask[:] = 0
        if isUpdated == True:
            h_lower = cv2.getTrackbarPos('H_lower', 'font_color')
            s_lower = cv2.getTrackbarPos('S_lower', 'font_color')
            v_lower = cv2.getTrackbarPos('V_lower', 'font_color')
            h_upper = cv2.getTrackbarPos('H_upper', 'font_color')
            s_upper = cv2.getTrackbarPos('S_upper', 'font_color')
            v_upper = cv2.getTrackbarPos('V_upper', 'font_color')
        else:
            h_lower = 0
            s_lower = 0
            v_lower = 205
            h_upper = 200
            s_upper = 200
            v_upper = 255

        lower = np.array([h_lower, s_lower, v_lower])
        upper = np.array([h_upper, s_upper, v_upper])
        hsv = cv2.cvtColor(flooded.copy(), cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lower, upper)
        # color_mask2 = (color_mask,)*255
        out = cv2.bitwise_and(hl, flooded, mask=color_mask)
        flooded = cv2.subtract(flooded, cv2.merge([color_mask, color_mask, color_mask]))
        cv2.imshow('font_color', cv2.add(flooded, out))
        # cv2.imshow('font_color', flooded)


    update()
    isUpdated = True
    print('defaults for white')

    cv2.createTrackbar('H_lower', 'font_color', 0, 255, update)
    cv2.createTrackbar('S_lower', 'font_color', 0, 255, update)
    cv2.createTrackbar('V_lower', 'font_color', 205, 255, update)

    cv2.createTrackbar('H_upper', 'font_color', 200, 255, update)
    cv2.createTrackbar('S_upper', 'font_color', 200, 255, update)
    cv2.createTrackbar('V_upper', 'font_color', 255, 255, update)

    while True:
        ch = 0xFF & cv2.waitKey()
        if ch == 27:
            break

    cv2.destroyAllWindows()