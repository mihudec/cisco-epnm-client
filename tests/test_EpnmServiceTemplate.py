import unittest
import pathlib
import json
from ciscoepnmclient.models.EpnmTemplates import *
from ciscoepnmclient.wrappers.build_service import *
from ciscoepnmclient.utils.common import jprint


class TestCiscoEpnmServiceTemplate(unittest.TestCase):

    def test_service_ce_data_template(self):

        tests = [
            {
                "name": "Test-01",
                "params": {
                    "mtu": 1522,
                    "bundling": False,
                    "enable_cfm": True,
                    "ccm_interval": "1 sec",
                    "ce_vlan_id_preservation": True,
                    "ce_vlan_cos_preservation": False
                },
                "result": {
                    "sa.ce-vlan-id-preservation": True,
                    "sa.ce-vlan-cos-preservation": False,
                    "sa.mtu-size": 1522,
                    "sa.enable-cfm": True,
                    "sa.ccm-interval": "1 sec",
                    "sa.bundling": False
                }
            }
        ]

        for test in tests:
            with self.subTest(msg=test["name"]):
                template = EpnmServiceCeDataTemplate(**test["params"])
                have = template.get_payload()
                want = test["result"]
                jprint(want)
                jprint(have)
                self.assertDictEqual(want, have)

    def test_uni_header_request_template(self):

        tests = [
            {
                "name": "Test-01",
                "params": {
                    "service_customer": "API_TEST",
                    "service_type": "carrier-ethernet-vpn",
                    "service_sub_type": "UNI",
                    "service_activate": True
                },
                "result": {
                    "sa.customer-ref": "MD=CISCO_EPNM!CUSTOMER=API_TEST",
                    "sa.service-type": "carrier-ethernet-vpn",
                    "sa.service-subtype": "UNI",
                    "sa.service-activate": True
                }
            },
            {
                "name": "Test-02",
                "params": {
                    "service_customer": "Infrastructure",
                    "service_type": "carrier-ethernet-vpn",
                    "service_sub_type": "EVPL",
                    "service_name": "API_TEST_SERVICE_001",
                    "service_description": "API_TEST_SERVICE_001",
                    "service_activate": True,

                },
                "result": {
                    "sa.customer-ref": "MD=CISCO_EPNM!CUSTOMER=Infrastructure",
                    "sa.service-type": "carrier-ethernet-vpn",
                    "sa.service-subtype": "EVPL",
                    "sa.service-name": "API_TEST_SERVICE_001",
                    "sa.service-description": "API_TEST_SERVICE_001",
                    "sa.service-activate": True,
                    "sa.ce-data": {
                        "sa.ce-vlan-id-preservation": True,
                        "sa.ce-vlan-cos-preservation": False,
                        "sa.mtu-size": 1522,
                        "sa.enable-cfm": True,
                        "sa.ccm-interval": "1 sec",
                        "sa.bundling": False
                    }
                }
            }
        ]
        for test in tests:
            with self.subTest(msg=test["name"]):
                template = EpnmServiceHeaderTemplate(**test["params"])
                have = template.get_payload()
                jprint(have)
                want = test["result"]

    def test_uni_template(self):

        tests = [
            {
                "name": "Test-Reference-01",
                "params": {
                    "name": "API_E_UNI_007",
                    "activate": True,
                    "mtu": 1522,
                    "service_multiplexing": True,
                    "bundling": False,
                    "enable_link_oam": False,
                    "operation": "update"
                },
                "action": "reference",
                "result": {
                    "sa.ref": "MD=CISCO-EPNM!NI=API_E_UNI_007",
                    "sa.operation": "update",
                    "sa.ce-data": {
                        "sa.activate": True,
                        "sa.mtu": 1522,
                        "sa.bundling": False,
                        "sa.service-multiplexing": True,
                        "sa.enable-link-oam": False
                    }
                }
            },
            {
                "name": "Test-Create-01",
                "params": {
                    "name": "API_E_UNI_007",
                    "activate": True,
                    "mtu": 1522,
                    "service_multiplexing": True,
                    "bundling": False,
                    "enable_link_oam": False,
                    "operation": "add"
                },
                "action": "create",
                "result": {
                    "sa.name": "API_E_UNI_007",
                    "sa.operation": "add",
                    "sa.ce-data": {
                        "sa.activate": True,
                        "sa.mtu": 1522,
                        "sa.bundling": False,
                        "sa.service-multiplexing": True,
                        "sa.enable-link-oam": False
                    },
                }
            }
        ]
        for test in tests:
            with self.subTest(test["name"]):
                template = EpnmNetworkInterfaceTemplate(**test["params"])
                have = template.get_payload(action=test["action"])
                want = test["result"]
                self.assertDictEqual(want, have)

    def test_qinq_template(self):

        tests = [
            {
                "name": "Test-01",
                "params": {
                    "match_type": "dot1q",
                    "vlan_id_list": "100",
                },
                "result": {
                    "sa.match-type": "dot1q",
                    "sa.vlan-id-list": "100"
                }
            }
        ]

        for test in tests:
            with self.subTest(test["name"]):
                template = EpnmQinqDataTemplate(**test["params"])
                have = template.get_payload()
                want = test["result"]
                jprint(want)
                jprint(have)
                self.assertDictEqual(want, have)

    def test_termination_point_template(self):

        tests = [
            {
                "name": "Test-01",
                "params": {
                    "node_name": "POC-D-903.test.local",
                    "physical_interface": "GigabitEthernet0/0/7",
                    "ni_name": "API_D_UNI_007",
                    "directionality": "source",
                    "qinq_data": EpnmQinqDataTemplate(match_type="dot1q", vlan_id_list="100").get_payload()
                },
                "result": {
                    "sa.tp-ref": "MD=CISCO_EPNM!ND=POC-D-903.test.local!FTP=name=GigabitEthernet0/0/7;lr=lr-gigabit-ethernet",
                    "sa.directionality": "source",
                    "sa.network-interface-ref": "MD=CISCO_EPNM!NI=API_D_UNI_007",
                    "sa.ce-data": {
                        "sa.qinq-data": {
                            "sa.match-type": "dot1q",
                            "sa.vlan-id-list": "100"
                        }
                    }
                }
            }
        ]

        for test in tests:
            with self.subTest(test["name"]):
                template = EpnmTerminationPointTemplate(**test["params"])
                have = template.get_payload()
                want = test["result"]
                jprint(want)
                jprint(have)
                self.assertDictEqual(want, have)

    def test_evpl_service_template(self):

        service_ce_data = EpnmServiceCeDataTemplate(**{
            "mtu": 1522,
            "bundling": False,
            "enable_cfm": True,
            "ccm_interval": "1 sec",
            "ce_vlan_id_preservation": False,
            "ce_vlan_cos_preservation": False
        })
        service_request_header = EpnmServiceHeaderTemplate(**{
            "service_customer": "Infrastructure",
            "service_type": "carrier-ethernet-vpn",
            "service_sub_type": "EVPL",
            "service_name": "API_TEST_SERVICE_001",
            "service_description": "API_TEST_SERVICE_001",
            "service_activate": True,
            "service_ce_data": service_ce_data
        })
        tp_qinq_data = EpnmQinqDataTemplate(**{
            "match_type": "dot1q",
            "vlan_id_list": "100",
        }).get_payload()
        tp_a = EpnmTerminationPointTemplate(**{
            "node_name": "POC-D-903.test.local",
            "physical_interface": "GigabitEthernet0/0/7",
            "ni_name": "API_D_UNI_007",
            "directionality": "source",
            "qinq_data": tp_qinq_data
        })
        tp_z = EpnmTerminationPointTemplate(**{
            "node_name": "POC-E-903.test.local",
            "physical_interface": "GigabitEthernet0/0/7",
            "ni_name": "API_E_UNI_007",
            "directionality": "sink",
            "qinq_data": tp_qinq_data
        })
        termination_points = [tp_a, tp_z]
        ni_a = EpnmNetworkInterfaceTemplate(**{
            "name": "API_D_UNI_007",
            "activate": True,
            "mtu": 1522,
            "service_multiplexing": True,
            "bundling": False,
            "enable_link_oam": False,
            "operation": "update"
        })
        ni_z = EpnmNetworkInterfaceTemplate(**{
            "name": "API_E_UNI_007",
            "activate": True,
            "mtu": 1522,
            "service_multiplexing": True,
            "bundling": False,
            "enable_link_oam": False,
            "operation": "update"
        })
        network_interfaces = [ni_a, ni_z]
        forwarding_path = {
            "sa.pseudowire-settings": {
                "sa.enable-control-word": True,
            }
        }

        service_template = EpnmEvplServiceTemplate(
            service_request_header=service_request_header,
            termination_points=termination_points,
            network_interfaces=network_interfaces,
            forwarding_path=forwarding_path
        )
        jprint(service_template.get_payload())
        result = None
        with pathlib.Path(__file__).parent.joinpath("resources/evpl_request_01.json").open() as f:
            result = json.load(fp=f)
        jprint(result)
        self.maxDiff = 10000

        self.assertDictEqual(result, service_template.get_payload())


class TestBuildService(unittest.TestCase):

    def test_build_evpl_service(self):
        self.maxDiff = 10000
        have = service_payload = build_evpl_service(
            a_node_name="POC-D-903.test.local",
            a_node_physical_interface="GigabitEthernet0/0/7",
            a_uni_name="API_D_UNI_007",
            z_node_name="POC-E-903.test.local",
            z_node_physical_interface="GigabitEthernet0/0/7",
            z_uni_name="API_E_UNI_007",
            service_customer="Infrastructure",
            service_name="API_TEST_SERVICE_001",
            service_description="API_TEST_SERVICE_001",
            vlan_id="100"
        ).get_payload()

        want = None
        with pathlib.Path(__file__).parent.joinpath("resources/evpl_request_01.json").open() as f:
            want = json.load(fp=f)
        
        jprint(want)
        jprint(have)

        self.assertDictEqual(want, have)


if __name__ == '__main__':
    unittest.main()
