import unittest

import logging
import sys


from src import Mensa

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Test(unittest.TestCase):

    def setUp(self):
        global stream_handler
        stream_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stream_handler)


    def test_Mensa(self):
        Mensa.getMensaData()
    


    def tearDown(self):
        logger.removeHandler(stream_handler)



if __name__ == '__main__':
    unittest.main()
