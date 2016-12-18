import numpy as np
import cv2, os, subprocess, math, glob, sys
import MovieSettings as mv
import MovieTimeline as mt
import MovieFrameSet as mfs
import helpers as hh

usage = '''USAGE
  python main.py <path_to_settings_ini_file> <path_to_movie_or_images>or<path_to_folders>
  path_to_movie_or_images should ends on *.jpg or *.png
'''
if len(sys.argv)<3:
    print(usage)
    sys.exit()
path_to_settings_ini_file = sys.argv[1]
path_to_movie_or_images = sys.argv[2]
if not os.path.isfile(path_to_settings_ini_file):
    print('not found <path_to_settings_ini_file>')
    sys.exit()
if not os.path.isfile(path_to_movie_or_images):
    # ok, it can be images
    if len(glob.glob(path_to_movie_or_images)) == 0:
        print('not found <path_to_movie_or_images>')
        sys.exit()
big_size = None
if len(sys.argv)==4:
    if sys.argv[3].isdigit():
        big_size = int(sys.argv[3])

# is one folder or many sub-folders?
is_one_folder = False
if path_to_movie_or_images[-4:] in ['.jpg', '.png']:
    is_one_folder = True

path_to_settings_ini_file = os.path.abspath(path_to_settings_ini_file)
path_to_movie_or_images = os.path.abspath(path_to_movie_or_images)

# if directories does not exist, let's create them
dirs_mast = ['out', 'origin', 'big', 'xlsx']
for d in dirs_mast:
    if not os.path.exists(d):
        os.makedirs(d)

# cleaning out and origin directory
for f_remove in glob.glob("out/*.png"):
    os.remove(f_remove)
for f_remove in glob.glob("origin/*.png"):
    os.remove(f_remove)

# Loading settings
#current_dir = os.path.dirname(os.path.realpath(__file__)) # does not work with py2exe
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
movieSettings = mv.MovieSettings()

movieSettings.read_settings(path_to_settings_ini_file)
movieSettings.set_out_path(current_dir+os.sep+'out'+os.sep)
movieSettings.set_origin_path(current_dir+os.sep+'origin'+os.sep)
if big_size is not None:
    movieSettings.set_big_size(big_size)

if is_one_folder:
    print('one folder start')
    movieSettings.set_movie(path_to_movie_or_images)
    movieSettings.set_movie_name(os.path.split(os.path.split(path_to_movie_or_images)[0])[1])

    # Timeline
    timeline = mt.MovieTimeline(movieSettings)
    timeline.process()

    # big images and xlsx
    # movieSettings.fps = 25.0
    hh.make_xlsx(movieSettings.fps, movieSettings.movieName)
    hh.make_big(movieSettings.movieName, movieSettings.bigSize)
    hh.make_big_origin(movieSettings.movieName, movieSettings.bigSize)
else:
    print('many folders start')
    for sub_dir in glob.glob(path_to_movie_or_images+os.sep+'*'+os.sep):
        # cleaning out and origin directory
        for f_remove in glob.glob("out/*.png"):
            os.remove(f_remove)
        for f_remove in glob.glob("origin/*.png"):
            os.remove(f_remove)

        movieSettings.set_movie(sub_dir+os.sep+'*.jpg')
        movieSettings.set_movie_name(os.path.split(os.path.split(sub_dir)[0])[1])

        timeline = mt.MovieTimeline(movieSettings)
        timeline.process()
        hh.make_xlsx(movieSettings.fps, movieSettings.movieName)
        hh.make_big(movieSettings.movieName, movieSettings.bigSize)
        hh.make_big_origin(movieSettings.movieName, movieSettings.bigSize)
