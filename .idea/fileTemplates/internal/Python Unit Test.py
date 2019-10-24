#parse ("DefaultVariables.py")
__author__ = "${FULLNAME}"
__email__ = "${FULLEMAIL}"
__copyright__ = "${COPYRIGHT}"
__license__ = "${LICENSE}"

import unittest

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
