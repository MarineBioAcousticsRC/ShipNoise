from keras.utils import Sequence
import numpy as np

class Generator(Sequence):

    def __init__(self, spects, labels, batch_size):
        self.spects = spects
        self.labels = labels
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.spects) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.spects[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.labels[idx * self.batch_size:(idx + 1) * self.batch_size]

        return batch_x, batch_y