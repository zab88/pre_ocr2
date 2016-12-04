import cv2
import numpy as np

def get_out_name(movie_name, frame_start, frame_end, fps):
    start = int(float(frame_start)/fps)
    end = int(float(frame_end)/fps)
    start_h = start/3600
    start_m = (start - start_h*3600)/60
    start_s = start%60
    end_h = end/3600
    end_m = (end - end_h*3600)/60
    end_s = end%60
    out_name = '{:0>}-{}h{:0>2}m{:0>2}s-{}h{:0>2}m{:0>2}s.png'.format(movie_name, start_h, start_m, start_s, end_h, end_m, end_s)
    return out_name

def getTimeByFrame(frame_number, fps):
    start = int(float(frame_number)/fps)
    start_h = start/3600
    start_m = (start - start_h*3600)/60
    start_s = start%60
    return '{}h{:0>2}m{:0>2}s'.format(start_h, start_m, start_s)

def isNewScene(self, frame_prev, frame_now):
    fgbg = cv2.BackgroundSubtractorMOG()
    f_prev = self.get_partA(frame_prev)
    f_now = self.get_partA(frame_now)
    # focus on center
    fgmask = fgbg.apply(f_prev)
    fgmask = fgbg.apply(f_now)
    th_counted = cv2.countNonZero(fgmask)
    # if (th_counted > width*height*0.2*0.03):
    print('is_new', th_counted)
    if (th_counted > self.settings.isNew):
        cv2.imshow('isNew', fgmask)
        return True
    return False