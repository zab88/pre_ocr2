import ConfigParser, json
import numpy as np

class MovieSettings:
    path2movie = None
    cropX = None
    cropY = None
    out_path = None
    fps = None
    origin_path = None
    is2lines = False
    minLetterArea = None
    movieName = 'unnamed'
    bigSize = 60
    def __init__(self):
        pass
    def read_settings(self, path2ini):
        Config = ConfigParser.ConfigParser()
        Config.read(path2ini)
        MovieSettings.cropX = json.loads(Config.get('Movie', 'cropX'))
        MovieSettings.cropY = json.loads(Config.get('Movie', 'cropY'))
        MovieSettings.isNew = None # int(Config.get('Th', 'isNew'))
        MovieSettings.text_lower = np.array(json.loads(Config.get('Font', 'text_lower')))
        MovieSettings.text_upper = np.array(json.loads(Config.get('Font', 'text_upper')))
        MovieSettings.border_lower = np.array(json.loads(Config.get('Font', 'border_lower')))
        MovieSettings.border_upper = np.array(json.loads(Config.get('Font', 'border_upper')))
        MovieSettings.is2lines = True if int(Config.get('Movie', 'cropLines'))==2 else False
        MovieSettings.useSymmetry = True if int(Config.get('Movie', 'useSymmetry'))==1 else False
        MovieSettings.minLetterArea = int(Config.get('Th', 'minLetterArea'))

    def set_movie(self, path2movie):
        if path2movie[-4:] in ['.mp4']:
            MovieSettings.isCut = False
        MovieSettings.isCut = True
        MovieSettings.path2movie = path2movie

    def set_out_path(self, out_path):
        MovieSettings.out_path = out_path

    def set_origin_path(self, origin_path):
        MovieSettings.origin_path = origin_path

    def set_movie_name(self, movieName):
        MovieSettings.movieName = movieName

    def set_big_size(self, bigSize):
        self.bigSize = bigSize