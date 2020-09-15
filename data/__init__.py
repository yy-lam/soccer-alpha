'''
docstring class for match statistics
'''

import numpy as np
import pickle
from app import s3


class Match(object):
    def __init__(self, home, away):
        home_data = np.load('data/2021/teams/' + home + '.npy')
        away_data = np.load('data/2021/teams/' + away + '.npy')
        self.model = pickle.load(open('data/model.sav', 'rb'))
        self.X = (np.log(home_data) - np.log(away_data)).reshape((1, 340))

    def predict(self):
        return self.model.predict(self.X)[0]

    def predict_proba(self):
        return self.model.predict_proba(self.X)[0]
