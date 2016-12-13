import cv2
import numpy as np
import helpers as hh


class MovieFrameSet:
    frames = []
    test_frames = []
    length = 12
    settings = None

    def __init__(self, settings):
        self.settings = settings

    def makeStep(self, new_frame):
        # if new_frame.frame_number < 1000:
        #     return
        # if new_frame.frame_number > 2000:
        #     exit()
        self.frames.append(new_frame)
        if len(self.frames) < self.length:
            # let's fill all set
            return
        self.test_frames = self.frames[-self.length:]
        now_canny, now_text_mask = self.getMacroAnd(self.frames[:-1])
        test_canny, test_text_mask = self.getMacroAnd(self.test_frames)
        diff_canny = np.bitwise_and(now_canny, test_canny)
        diff_text_mask = np.bitwise_and(now_text_mask, test_text_mask)
        # representative part
        rep_canny = self.get_partA(diff_canny)
        rep_text = self.get_partA(diff_text_mask)

        isContinue = self.isEqualBin(now_text_mask, test_text_mask)
        # del self.test_frames[:]
        # del self.frames[0]
        # if cv2.countNonZero(rep_text) > 121:
        #     cv2.imwrite('out/{}_{}.png'.format(self.frames[0].frame_number,
        #                                    hh.getTimeByFrame(self.frames[0].frame_number, self.settings.fps)),
        #             diff_text_mask
        #             )
        if (cv2.countNonZero(rep_text) > self.settings.minLetterArea) and (cv2.countNonZero(rep_canny) > 40) and isContinue:
        # if (cv2.countNonZero(rep_text) > 121) and isContinue:
            # can make step
            pass
        # nothing to output
        elif cv2.countNonZero(self.get_partA(now_text_mask)) < self.settings.minLetterArea:
            self.justStop()
        else:
            # stop it
            self.stopSequence(now_text_mask)

    # without output
    def justStop(self):
        del self.frames[:-1]
        del self.test_frames[:-1]

    def stopSequence(self, imgOut):
        if len(self.frames) <= self.length:
            self.justStop()
            return

        # path_save = self.settings.out_path + \
        #             hh.get_out_name('Lan', self.frames[0].frame_number, self.frames[-1].frame_number, self.settings.fps)
        path_save = '{}{:0>8}_{:0>8}.png'.format(self.settings.out_path, self.frames[0].frame_number, self.frames[-1].frame_number)
        cv2.imwrite(path_save, (255-imgOut))
        path_save_origin = '{}{:0>8}_{:0>8}.png'.format(self.settings.origin_path, self.frames[0].frame_number, self.frames[-1].frame_number)
        cv2.imwrite(path_save_origin, self.frames[0].img_origin)
        # cv2.imwrite(path_save.replace('.png', 'c.png'), self.getMacroAnd(self.frames[:-1])[0])
        # cv2.imwrite(path_save.replace('.png', 't.png'), self.getMacroAnd(self.frames[:-1])[1])

        self.justStop()

    def getMacroAnd(self, frames):
        canny = frames[0].img_canny
        text_mask = frames[0].text_mask
        for f in frames[1:]:
            canny = cv2.bitwise_and(canny, f.img_canny)
            text_mask = cv2.bitwise_and(text_mask, f.text_mask)
        return canny, text_mask

    def isTextCanBe(self, frame):
        frame = self.get_partA(frame)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        text_lower = self.settings.text_lower
        text_upper = self.settings.text_upper
        # print(text_lower, text_upper)
        text_mask = cv2.inRange(hsv, text_lower, text_upper)
        h, w = text_mask.shape[:2]
        text_mask_left = text_mask[:, 0:int(w / 2.)]
        text_mask_right = text_mask[:, int(w / 2.):]
        th_counted_left = cv2.countNonZero(text_mask_left)
        th_counted_right = cv2.countNonZero(text_mask_right)
        # print('is_text', th_counted_left+th_counted_right)
        if ((th_counted_left > self.settings.isNew / 2.) and (th_counted_right > self.settings.isNew / 2.)):
            # cv2.imshow('text_mask', text_mask)
            return True
        return False

    @staticmethod
    def isEqualBin(bin1, bin2):
        s12 = cv2.countNonZero(bin1) + cv2.countNonZero(bin2)
        th_counted = cv2.countNonZero(np.bitwise_xor(bin1, bin2))
        if th_counted > (s12*0.1): # TODO: param to settings
            return False
        return True


    def get_partA(self, img):
        height, width = img.shape[:2]
        img_tmp = img[:, int(width / 2. - width * 0.1):int(width / 2. + width * 0.1)]
        return img_tmp.copy()
