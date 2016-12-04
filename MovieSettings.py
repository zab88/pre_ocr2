import ConfigParser, json
import numpy as np

class MovieSettings:
    path2movie = None
    cropX = None
    cropY = None
    out_path = None
    fps = None
    def __init__(self):
        pass
    def read_settings(self, path2ini):
        Config = ConfigParser.ConfigParser()
        Config.read(path2ini)
        MovieSettings.cropX = json.loads(Config.get('Movie', 'cropX'))
        MovieSettings.cropY = json.loads(Config.get('Movie', 'cropY'))
        MovieSettings.isNew = int(Config.get('Th', 'isNew'))
        MovieSettings.text_lower = np.array(json.loads(Config.get('Font', 'text_lower')))
        MovieSettings.text_upper = np.array(json.loads(Config.get('Font', 'text_upper')))

    def set_movie(self, path2movie):
        MovieSettings.path2movie = path2movie

    def set_out_path(self, out_path):
        MovieSettings.out_path = out_path