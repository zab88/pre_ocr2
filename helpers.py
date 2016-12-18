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
    return img_out, i

def make_xlsx(fps, movieName):
    # if not os.path.exists('xlsx'+os.sep+movieName):
    #     os.makedirs('xlsx'+os.sep+movieName)
    workbook = xlsxwriter.Workbook('xlsx'+os.sep+movieName+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column(1, 2, 12)
    worksheet.set_column(3, 4, 100)

    j = 0
    for f_test in glob.glob("out/*.png"):
        if 'big' in os.path.basename(f_test):
            continue
        # print(str(j+1000), getHMSD2(os.path.basename(f_test), fps))
        if fps is None:
            time_start = os.path.basename(f_test).replace('.png', '').split('_')[0].replace('-', ':')
            time_end = os.path.basename(f_test).replace('.png', '').split('_')[1].replace('-', ':')
        else:
            time_start = getHMSD2(os.path.basename(f_test), fps)[0]
            time_end = getHMSD2(os.path.basename(f_test), fps)[1]
        time_start = time_start[::-1].replace(':', '.', 1)[::-1] + '0'
        time_end = time_end[::-1].replace(':', '.', 1)[::-1] + '0'

        worksheet.write('A'+str(j+1), str(j+1000))
        worksheet.write('B'+str(j+1), time_start)
        worksheet.write('C'+str(j+1), time_end)

        # image has big height
        worksheet.set_row(j, 32)
        # worksheet.insert_image('D'+str(j+1), f_test)
        worksheet.insert_image('D'+str(j+1), 'origin/'+os.path.basename(f_test))
        j += 1
    workbook.close()

def make_big(movieName, bigSize=60):
    img_all = None
    f_j = 0
    big_num = 1
    sid_width = 130
    for f_test in glob.glob("out/*.png"):
        if 'big' in os.path.basename(f_test):
            continue
        if img_all is None:
            img_all = cv2.imread(f_test, 0)
            img_all = pull_text_left(img_all)[0]
            # cv2.imshow('asdf', img_all)
            # cv2.waitKey()
            # exit()
            # adding hmsd
            h, w = img_all.shape[:2]
            img_clear = np.ones((h, w+sid_width), np.uint8)*255
            img_hmsd = np.ones((h, sid_width), np.uint8)*255
            cv2.putText(img_hmsd, str(1000+f_j)+'A', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            img_all = np.concatenate((img_hmsd, img_all), axis=1)
            f_j += 1
            continue
        img_now = cv2.imread(f_test, 0)
        img_now = pull_text_left(img_now)[0]
        img_hmsd = np.ones((h, sid_width), np.uint8)*255
        cv2.putText(img_hmsd, str(1000+f_j)+'A', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        img_now = np.concatenate((img_hmsd, img_now), axis=1)

        img_all = np.concatenate((img_all, img_clear), axis=0)
        img_all = np.concatenate((img_all, img_now), axis=0)
        f_j += 1
        #
        # if not os.path.exists('big'+os.sep+movieName):
        #     os.makedirs('big'+os.sep+movieName)
        if f_j%bigSize == 0 and f_j>=bigSize:
            cv2.imwrite('big'+os.sep+movieName+str(big_num).zfill(2)+'.png', img_all)
            img_all = None
            big_num += 1
    # the rest
    cv2.imwrite('big'+os.sep+movieName+str(big_num).zfill(2)+'.png', img_all)

def make_big_origin(movieName, bigSize=60):
    '''
    make JPG images, not png
    :param movieName:
    :return:
    '''
    img_all = None
    f_j = 0
    big_num = 1
    sid_width = 130
    for f_test in glob.glob("origin/*.png"):
        if 'big' in os.path.basename(f_test):
            continue
        if img_all is None:
            img_all = cv2.imread(f_test, 0)
            h, w = img_all.shape[:2]
            img_all = (255-img_all)
            # cutting from left and right
            path_to_bin = f_test.replace('origin'+os.sep+os.path.basename(f_test), 'out'+os.sep+os.path.basename(f_test))
            img_bin = cv2.imread(path_to_bin, 0)
            _, offset_left = pull_text_left(img_bin.copy())
            _, offset_right = pull_text_left(cv2.flip(img_bin.copy(), 1)) # flip horizontal
            img_with_offset = np.ones((h, w), np.uint8)*255
            img_with_offset[:, :w-offset_left-offset_right] = img_all[:, offset_left:w-offset_right]
            img_all = img_with_offset

            img_clear = np.ones((h, w+sid_width), np.uint8)*255
            img_hmsd = np.ones((h, sid_width), np.uint8)*255
            cv2.putText(img_hmsd, str(1000+f_j)+'A', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            img_all = np.concatenate((img_hmsd, img_all), axis=1)
            f_j += 1
            continue
        img_now = cv2.imread(f_test, 0)
        img_now = (255-img_now)
        # cutting from left and right, based on bin img
        path_to_bin = f_test.replace('origin'+os.sep+os.path.basename(f_test), 'out'+os.sep+os.path.basename(f_test))
        img_bin = cv2.imread(path_to_bin, 0)
        _, offset_left = pull_text_left(img_bin.copy())
        _, offset_right = pull_text_left(cv2.flip(img_bin.copy(), 1)) # flip horizontal
        img_with_offset = np.ones((h, w), np.uint8)*255
        img_with_offset[:, :w-offset_left-offset_right] = img_now[:, offset_left:w-offset_right]
        img_now = img_with_offset

        img_hmsd = np.ones((h, sid_width), np.uint8)*255
        cv2.putText(img_hmsd, str(1000+f_j)+'A', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        img_now = np.concatenate((img_hmsd, img_now), axis=1)

        img_all = np.concatenate((img_all, img_clear), axis=0)
        img_all = np.concatenate((img_all, img_now), axis=0)
        f_j += 1

        if f_j%bigSize == 0 and f_j>=bigSize:
            cv2.imwrite('big'+os.sep+movieName+str(big_num).zfill(2)+'.jpg', img_all)
            img_all = None
            big_num += 1
    # the rest
    cv2.imwrite('big'+os.sep+movieName+str(big_num).zfill(2)+'.jpg', img_all)