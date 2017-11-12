
import os
import unittest


#suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(HereTestMethod)) #in case we create a TestCase here


if __name__ == '__main__':
    ##### Due to a problem with travis, cannot use test02_osg for now. so we select all the others
    cwd = os.path.realpath(os.path.dirname(__file__))
    #suite = unittest.defaultTestLoader.discover(cwd) # UNCOMMENT if you want to test all test cases

    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.discover(cwd, "test00_read_write.py"))
    suite.addTest(unittest.defaultTestLoader.discover(cwd, "test01_nodes.py"))

    unittest.main(defaultTest='suite', verbosity=2)

