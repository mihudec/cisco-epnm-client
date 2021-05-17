import unittest 
from tests.test_EpnmModelStructure import TestEpnmModelStructure
from ciscoepnmclient.models.EpnmCeDataModels import *

class TestEpnmCeDataModel(TestEpnmModelStructure):

    TEST_CLASS = EpnmCeDataModel

class TestEpnmCeDataServiceModel(TestEpnmModelStructure):

    TEST_CLASS = EpnmCeDataServiceModel

    def test_init(self):
        instance = self.TEST_CLASS(
            mtu=1522,
            bundling=False,
            ce_vlan_id_preservation=False
        )
        self.assertIsInstance(instance, self.TEST_CLASS)

    def test_required_fields(self):
        instance = self.TEST_CLASS(
            mtu=1522,
            bundling=False,
            ce_vlan_id_preservation=False
        )
        self.assertTrue(all([hasattr(instance, x) for x in self._REQUIRED_FIELD_NAMES]))


if __name__ == '__main__':
    unittest.main()