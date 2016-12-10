import cv2
import numpy as np
import xlsxwriter, glob, os

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
    seconds = int(float(frame_number)/fps)
    hh = seconds/3600
    mm = (seconds - hh*3600)/60
    ss = seconds%60
    dd = int(10.*float((frame_number - fps*int(frame_number/fps)))/fps)
    return '{:0>2}:{:0>2}:{:0>2}:{:0<2}'.format(hh, mm, ss, dd)

def getHMSD(file_name, fps):
    frame_start = int(file_name.split('_')[0])
    frame_end = int(file_name.split('_')[1].replace('.png', ''))
    return '{}-{}'.format(getTimeByFrame(frame_start, fps), getTimeByFrame(frame_end, fps))
def getHMSD2(file_name, fps):
    frame_start = int(file_name.split('_')[0])
    frame_end = int(file_name.split('_')[1].replace('.png', ''))
    return getTimeByFrame(frame_start, fps), getTimeByFrame(frame_end, fps)

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

def pull_text_left(img):
    img_out = None
    h, w = img.shape[:2]
    img_negative = (255 - img)
    for i in xrange(0, w, 1):
        if sum(img_negative[:, i]) < 1:
            continue
        img_out = np.ones((h, w), np.uint8)*255
        img_out[:, :w-i] = img[:, i:]
        break
    if img_out is None:
        return img
    return img_out

def make_xlsx(fps):
    workbook = xlsxwriter.Workbook('out.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, 2, 12)
    worksheet.set_column(3, 4, 100)

    j = 0
    for f_test in glob.glob("out/*.png"):
        if 'big' in os.path.basename(f_test):
            continue
        print(str(j+1000), getHMSD2(os.path.basename(f_test), fps))
        worksheet.write('A'+str(j+1), str(j+1000))
        worksheet.write('B'+str(j+1), getHMSD2(os.path.basename(f_test), fps)[0])
        worksheet.write('C'+str(j+1), getHMSD2(os.path.basename(f_test), fps)[1])

        # image has big height
        worksheet.set_row(j, 32)
        # worksheet.insert_image('D'+str(j+1), f_test)
        worksheet.insert_image('D'+str(j+1), 'origin/'+os.path.basename(f_test))
        j += 1
    workbook.close()