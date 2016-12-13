import cv2
import numpy as np
import MovieSettings as mv

class MovieFrame:
    frame_number = None
    img_origin = None
    img_gray = None
    img_canny = None
    text_mask = None
    def __init__(self, frame_number, img):
        # img = cv2.pyrDown(img)
        self.frame_number = frame_number
        self.img_origin = img
        # self.img_origin = cv2.medianBlur(img, 5)
        self.img_gray = cv2.cvtColor(self.img_origin, cv2.COLOR_BGR2GRAY)
        self.img_canny = cv2.Canny(self.img_gray, 100, 200)

        # HSV
        hsv = cv2.cvtColor(self.img_origin, cv2.COLOR_BGR2HSV)
        text_lower = mv.MovieSettings.text_lower
        text_upper = mv.MovieSettings.text_upper
        # text_lower = mv.MovieSettings.border_lower
        # text_upper = mv.MovieSettings.border_upper
        self.text_mask = cv2.inRange(hsv, text_lower, text_upper)

        # self.text_mask = cv2.erode(self.text_mask, np.ones((3, 1), np.uint8))

        # text_mask correction
        self.text_mask = cv2.copyMakeBorder(self.text_mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(255))
        cv2.floodFill(self.text_mask, None, (0, 0), (0))
        # self.text_mask = cv2.dilate(self.text_mask, np.ones((3, 1), np.uint8))

        # symmetry correction
        if mv.MovieSettings.useSymmetry:
            self.text_mask = self.symmetry_clean(self.text_mask)

    def delete_big_blobs(self):
        # http://www.learnopencv.com/blob-detection-using-opencv-python-c/
        # detector = cv2.SimpleBlobDetector()
        pass

    def symmetry_clean(self, img_bin):
        # axes sum
        # img_bin = img_bin/255
        h, w = img_bin.shape[:2]
        cols_sum = img_bin.sum(axis=0)
        cols_sum = [1 if s > 1 else 0 for s in cols_sum]
        mid = len(cols_sum)/2
        m_w = 25
        min_clean = None
        for i in xrange(0, len(cols_sum)/2, 1):
            if sum(cols_sum[mid-i-m_w:mid-i]) < 1:
                min_clean = i
                break
            if sum(cols_sum[mid+i:mid+i+m_w]) < 1:
                min_clean = i
                break
        if min_clean is not None:
            # clean
            res = img_bin.copy()
            cv2.rectangle(res, (0, 0), (mid-min_clean, h), color=(0), thickness=-1)
            cv2.rectangle(res, (mid+min_clean, 0), (w, h), color=(0), thickness=-1)
        return res