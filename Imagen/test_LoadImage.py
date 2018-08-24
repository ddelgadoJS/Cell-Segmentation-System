import unittest
from keras.preprocessing import image
from LoadImages import LoadImage

class TestLoadImage(unittest.TestCase):
    def TestImage(self):
        self.assertRaises(AttributeError, LoadImage, None)