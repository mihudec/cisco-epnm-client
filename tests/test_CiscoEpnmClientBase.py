import unittest
from ciscoepnmclient.CiscoEpnmClientBase import CiscoEpnmClientBase

class TestCiscoEpnmClinetBase(unittest.TestCase):

    def test_init(self):
        client = CiscoEpnmClientBase()

if __name__ == '__main__':
    unittest.main()