import unittest
import pathlib
import json
from ciscoepnmclient.utils.fdn import parse_fdn, build_fdn

RESOURCE_PATH = pathlib.Path(__file__).parent.joinpath("resources")

class TestEpnmFDN(unittest.TestCase):

    def test_parse(self):
        test_fdns = json.loads(RESOURCE_PATH.joinpath("test_fdn.json").read_text())
        for i, fdn in enumerate(test_fdns):
            with self.subTest(msg=i):
                want = fdn["data"]
                have = parse_fdn(fdn=fdn["string"])
                self.assertEqual(want, have)

    def test_build(self):
        test_fdns = json.loads(RESOURCE_PATH.joinpath("test_fdn.json").read_text())
        for i, fdn in enumerate(test_fdns):
            with self.subTest(msg=i):
                want = fdn["string"]
                have = build_fdn(data=fdn["data"])
                self.assertEqual(want, have)
        


if __name__ == '__main__':
    unittest.main()