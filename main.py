import numpy as np
import cv2, os, subprocess, math, glob
import MovieSettings as mv
import MovieTimeline as mt
import MovieFrameSet as mfs
import helpers as hh

# cleaning out directory, during development
for f_remove in glob.glob("out/*.png"):
    os.remove(f_remove)

# Loading settings
current_dir = os.path.dirname(os.path.realpath(__file__))
movieSettings = mv.MovieSettings()
# movieSettings.read_settings(current_dir+os.sep+'movies'+os.sep+'LanLing.ini')
# movieSettings.set_movie(current_dir+os.sep+'movies'+os.sep+'LanLing26.mp4')
# movieSettings.read_settings(current_dir+os.sep+'movies'+os.sep+'Xiang.ini')
# movieSettings.set_movie(current_dir+os.sep+'movies'+os.sep+'Xiang35.mp4')
movieSettings.read_settings(current_dir+os.sep+'movies'+os.sep+'legendvideo.ini')
movieSettings.set_movie(current_dir+os.sep+'movies'+os.sep+'legendvideo.mp4')
movieSettings.set_out_path(current_dir+os.sep+'out'+os.sep)
movieSettings.set_origin_path(current_dir+os.sep+'origin'+os.sep)

# Timeline
timeline = mt.MovieTimeline(movieSettings)
timeline.process()

# print(movieSettings.out_path)

# clue
# for f_remove in glob.glob("tmp/*.png"):
#     os.remove(f_remove)
# img_prev = None
# for f_test in glob.glob("out/*.png"):
#     if img_prev is None:
#         img_prev = cv2.imread(f_test, 0)
#         img_prev = cv2.threshold(img_prev,127,255,cv2.THRESH_BINARY)[1]
#         img_prev_name = os.path.basename(f_test)
#         # cv2.imwrite('tmp'+os.sep+os.path.basename(f_test), (255-img_prev))
#         continue
#     img_now = cv2.imread(f_test, 0)
#     img_now = cv2.threshold(img_now,127,255,cv2.THRESH_BINARY)[1]
#     img_now_name = os.path.basename(f_test)
#     if mfs.MovieFrameSet.isEqualBin((255-img_prev), (255-img_now)):
#         print(img_prev_name, img_now_name)
#         name_movie = img_now_name.split('-')[0]
#         time_start = img_prev_name
#         time_end = img_now_name.split('-')[2]
#         img_prev_name = '{}-{}-{}'.format(name_movie, time_start, time_end)
#         img_prev = np.bitwise_and(img_now, img_prev)
#     else:
#         cv2.imwrite('tmp'+os.sep+img_prev_name, img_prev)
#         # cv2.imwrite('tmp'+os.sep+os.path.basename(f_test), (255-img_now))
#
#         img_prev = img_now
#         img_prev_name = os.path.basename(f_test)
# # saving final image
# cv2.imwrite('tmp'+os.sep+img_prev_name, img_prev)


# one big image
img_all = None
# movieSettings.fps = 25.0
hh.make_xlsx(movieSettings.fps)
f_j = 0
big_num = 1
sid_width = 110
for f_test in glob.glob("out/*.png"):
    if 'big' in os.path.basename(f_test):
        continue
    if img_all is None:
        img_all = cv2.imread(f_test, 0)
        img_all = hh.pull_text_left(img_all)
        # cv2.imshow('asdf', img_all)
        # cv2.waitKey()
        # exit()
        # adding hmsd
        h, w = img_all.shape[:2]
        img_clear = np.ones((h, w+sid_width), np.uint8)*255
        img_hmsd = np.ones((h, sid_width), np.uint8)*255
        cv2.putText(img_hmsd, str(1000+f_j), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        img_all = np.concatenate((img_hmsd, img_all), axis=1)
        f_j += 1
        continue
    img_now = cv2.imread(f_test, 0)
    img_now = hh.pull_text_left(img_now)
    img_hmsd = np.ones((h, sid_width), np.uint8)*255
    cv2.putText(img_hmsd, str(1000+f_j), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    img_now = np.concatenate((img_hmsd, img_now), axis=1)

    img_all = np.concatenate((img_all, img_clear), axis=0)
    img_all = np.concatenate((img_all, img_now), axis=0)
    f_j += 1
    if f_j%60 == 0 and f_j>=60:
        cv2.imwrite('out'+os.sep+'big'+str(big_num)+'.png', img_all)
        img_all = None
        big_num += 1

cv2.imwrite('out'+os.sep+'big'+str(big_num)+'.png', img_all)