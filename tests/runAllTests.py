
import os
import unittest

suite = unittest.defaultTestLoader.discover(os.path.realpath(os.path.dirname(__file__)))
#suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HereTestMethod)) #in case we create a TestCase here

if __name__ == '__main__':
    unittest.main(defaultTest='suite', verbosity=2)

