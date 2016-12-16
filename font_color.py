#!/usr/bin/env python

'''
HSV color selector.
Usage:
  font_color.py [<image>]
Keys:
  ESC   - exit
'''

# Python 2/3 compatibility
#from __future__ import print_function

import numpy as np
import cv2

if __name__ == '__main__':
    import sys
    try:
        fn = sys.argv[1]
    except:
        # fn = 'movie_01/Xiang-00-00-00-00.png'
        # fn = r'K:\MyPrograms\python2\recipe\pre_ocr2\origin\00-32-05-60_00-32-08-00.png'
        print(__doc__)
        sys.exit()

    img = cv2.imread(fn, True)
    img = cv2.pyrUp(img)
    # img = cv2.pyrDown(img)
    if img is None:
        print('Failed to load image file:', fn)
        sys.exit(1)

    h, w, channels = img.shape[:3]
    # mask = np.zeros((h+2, w+2), np.uint8)
    # seed_pt = None
    # fixed_range = True
    # connectivity = 4
    updated = False

    def update(dummy=None):
        global updated
        flooded = img.copy()
        hl = np.zeros((h, w, channels), np.uint8)
        hl[:,:,:] = (0, 0, 255)
        # mask[:] = 0
        if updated == True:
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
            updated = True
        # flags = connectivity
        # if fixed_range:
        #     flags |= cv2.FLOODFILL_FIXED_RANGE
        # cv2.floodFill(flooded, mask, seed_pt, (255, 255, 255), (lo,)*3, (hi,)*3, flags)
        # cv2.circle(flooded, seed_pt, 2, (0, 0, 255), -1)
        # cv2.imshow('font_color', flooded)

        lower = np.array([h_lower, s_lower, v_lower])
        upper = np.array([h_upper, s_upper, v_upper])
        hsv = cv2.cvtColor(flooded.copy(), cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv, lower, upper)
        # color_mask2 = (color_mask,)*255
        out = cv2.bitwise_and(hl, flooded, mask=color_mask)
        flooded = cv2.subtract(flooded, cv2.merge([color_mask, color_mask, color_mask]))
        cv2.imshow('font_color', cv2.add(flooded, out))
        # cv2.imshow('font_color', flooded)

    # def onmouse(event, x, y, flags, param):
    #     global seed_pt
    #     if flags & cv2.EVENT_FLAG_LBUTTON:
    #         seed_pt = x, y
    #         update()

    update()
    # cv2.setMouseCallback('floodfill', onmouse)
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
        # if ch == ord('f'):
        #     fixed_range = not fixed_range
        #     print('using %s range' % ('floating', 'fixed')[fixed_range])
        #     update()
        # if ch == ord('c'):
        #     connectivity = 12-connectivity
        #     print('connectivity =', connectivity)
        #     update()
    cv2.destroyAllWindows()