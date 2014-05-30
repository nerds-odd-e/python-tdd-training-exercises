'''
Please put the implementation and test in the same Python module
for this simple exercise.
'''
import unittest


class TestFizzBuzz(unittest.TestCase):
    '''
    Derive the test group class from unittest.TestCase class.
    '''

    def setUp(self):
        '''will be executed before every test case. Optional'''
        pass

    def tearDown(self):
        '''
        will be executed after every test case,
        even when the test case fails.
        Optional.
        '''
        pass

    def test_name(self):
        '''Any method with a name begin with test will become a test case.'''
        # Use the assertion methods from the unittest.TestCase class
        # to check the result of the test.
        self.assertEqual(1, 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()