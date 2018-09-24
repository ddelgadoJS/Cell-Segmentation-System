import unittest
from LoadImages import Images

class TestLoadImage(unittest.TestCase):
    def test_BlackPixels(self):
        image = Images()
        self.assertEqual(image.loadImage("BlackPixels.jpg"), 0)
        
    def test_WhitePixels(self):
        image = Images()
        self.assertEqual(image.loadImage("WhitePixels.jpg"), 2550000)
        
if __name__ == '__main__':
    unittest.main()