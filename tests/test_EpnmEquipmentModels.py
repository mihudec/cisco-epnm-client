import unittest
from tests.test_EpnmModelStructure import TestEpnmModelStructure
from ciscoepnmclient.models.EpnmEquipmentModels import *

class TestEpnmPhysicalConnectorModel(TestEpnmModelStructure):


    TEST_CLASS = EpnmPhysicalConnectorModel
    TEST_INSTANCE = None
    TEST_PAYLOAD = {
        "fdtn.description": "12xGE-4x10GE-FIXED",
        "fdtn.name": "GigabitEthernet0/0/7",
        "eq.containing-equipment": "MD=CISCO_EPNM!ND=POC-H-920.cezdata.corp!EQ=name= FIXED IM subslot 0/0;partnumber=cevModuleSPAETHER12XGE4X10GE",
        "eq.fdn": "MD=CISCO_EPNM!ND=POC-H-920.cezdata.corp!EQ=name= FIXED IM subslot 0/0;partnumber=cevModuleSPAETHER12XGE4X10GE!PC=GigabitEthernet0/0/7"
    }
        

    def test_init(self):
        instance = self.TEST_CLASS(**self.TEST_PAYLOAD)

class EpnmConnectorsContainerModel(TestEpnmModelStructure):

    TEST_CLASS = EpnmConnectorsContainerModel

if __name__ == '__main__':
    unittest.main()
