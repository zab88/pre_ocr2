import cv2
import helpers as hh
import MovieFrameSet as mfs
import MovieFrame as mf

class MovieTimeline:
    settings = None
    cap = None
    def __init__(self, settings):
        self.settings = settings
        self.cap = cv2.VideoCapture(settings.path2movie)
        self.settings.fps = self.cap.get(5)

    def process(self):
        frame_number = 0
        frame_prev = None
        frameSet = mfs.MovieFrameSet(self.settings)
        while(self.cap.isOpened()):
            ret, frame = self.cap.read()
            if ret is False:
                # video ended
                print(frame_number)
                break
            frame_number += 1
            # if frame_number < 4000:
            #     continue

            if frame_prev is None:
                frame_prev = frame
                continue
            # if frame_number < 4800:
            #     continue
            if self.settings.is2lines:
                # split cropped in 2 lines
                mid_crop = sum(self.settings.cropY)/2
                frame = frame[mid_crop:self.settings.cropY[1], self.settings.cropX[0]:self.settings.cropX[1]]
            else:
                frame = frame[self.settings.cropY[0]:self.settings.cropY[1], self.settings.cropX[0]:self.settings.cropX[1]]
            f_obj = mf.MovieFrame(frame_number, frame)
            frameSet.makeStep(f_obj)

            # if self.isNewScene(frame_prev, frame) and self.isTextCanBe(frame):
            #     path_save = self.settings.out_path+hh.get_out_name('Lan', frame_number, frame_number, self.settings.fps)
            #     cv2.waitKey(0)
            #     cv2.imwrite(path_save, frame)
            #
            # frame_prev = frame
            # cv2.imshow('frame', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
