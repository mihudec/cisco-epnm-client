from ciscoepnmclient.utils.common import get_line_rate
class EpnmRequestTemplateBase(object):

    def __init__(self):
        pass

    def get_payload(self):
        pass


class EpnmNetworkInterfaceTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                 name: str,
                 description: str = None,
                 activate: bool = True,
                 operation: str = None,
                 mtu: int = 1522,
                 bundling: bool = False,
                 service_multiplexing: bool = True,
                 enable_link_oam: bool = False
                 ):
        self.name = name
        self.description = description
        self.activate = activate
        self.operation = operation
        self.mtu = mtu
        self.bundling = bundling
        self.service_multiplexing = service_multiplexing
        self.enable_link_oam = enable_link_oam

    def get_payload(self, create: bool):
        payload = None
        if create:
            payload = {
                "sa.name": self.name,
                "sa.ce-data": {
                    "sa.activate": self.activate
                }
            }
            if self.description is not None:
                payload["sa.ce-data"]["sa.description"] = self.description
            if self.mtu is not None:
                payload["sa.ce-data"]["sa.mtu"] = self.mtu
            if self.bundling is not None:
                payload["sa.ce-data"]["sa.bundling"] = self.bundling
            if self.service_multiplexing is not None:
                payload["sa.ce-data"]["sa.service-multiplexing"] = self.service_multiplexing
            if self.enable_link_oam is not None:
                payload["sa.ce-data"]["sa.enable-link-oam"] = self.enable_link_oam
        else:
            payload = {
                "sa.ref": f"MD=CISCO-EPNM!NI={self.name}"
            }
        if self.operation is not None:
            payload["sa.operation"] = self.operation
        return payload

class EpnmTerminationPointTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                node_name: str,
                physical_interface: str, 
                ni_name: str,
                qinq_data: dict = None
    ):
        self.node_name = node_name
        self.physical_interface = physical_interface
        self.ni_name = ni_name
        self.qinq_data = qinq_data

        

    def get_payload(self, create_network_interface: bool = False):
        payload = {
            "sa.tp-ref": f"MD=CISCO-EPNM!ND={self.node_name}!FTP=name={self.physical_interface};lr={get_line_rate(self.physical_interface)}"
        }
        if create_network_interface:
            payload["sa.network-interface-name"] = self.ni_name
        else:
            payload["sa.network-interface-ref"] = f"MD=CISCO-EPNM!NI={self.ni_name}"

        ce_data = {}
        qinq_data = {}

        if self.qinq_data is not None:
            qinq_data = self.qinq_data

        if len(qinq_data):
            ce_data["sa.qinq-data"] = qinq_data
        if len(ce_data):
            payload["sa.ce-data"] = ce_data
        return payload
        

class EpnmServiceTemplateBase(EpnmRequestTemplateBase):
    pass


class EpnmServiceTemplateHeader(EpnmServiceTemplateBase):

    def __init__(self,
                 service_customer: str,
                 service_type: str,
                 service_sub_type: str,
                 service_name: str = None,
                 service_description: str = None,
                 service_activate: bool = True,
                 service_mtu: int = None,
                 enable_cfm: bool = None,
                 ccm_interval: str = None,
                 bundling: bool = None
                 ):
        self.service_customer = service_customer
        self.service_type = service_type
        self.service_sub_type = service_sub_type
        self.service_name = service_name
        self.service_description = service_description
        self.service_activate = service_activate
        self.service_mtu = service_mtu
        self.enable_cfm = enable_cfm
        self.ccm_interval = ccm_interval
        self.bundling = bundling
    
    def get_payload(self):
        sa_ce_data = {}
        payload = {
            "sa.customer-ref": f"MD=CISCO-EPNM!CUSTOMER={self.service_customer}",
            "sa.service-type": self.service_type,
            "sa.service-subtype": self.service_sub_type,
        }
        if self.service_name is not None:
            payload["sa.service-name"] = self.service_name
        if self.service_description is not None:
            payload["sa.service-description"] = self.service_description
        if self.service_activate is not None:
            payload["sa.service-activate"] = self.service_activate
        if self.service_mtu is not None:
            sa_ce_data["sa.mtu-size"] = self.service_mtu
        if self.enable_cfm is not None:
            sa_ce_data["sa.enable-cfm"] = self.enable_cfm
        if self.ccm_interval is not None:
            sa_ce_data["sa.ccm-interval"] = self.ccm_interval
        if self.bundling is not None:
            sa_ce_data["bundling"] = self.bundling
        if len(sa_ce_data):
            payload["sa.ce-data"] = sa_ce_data
        return payload
        
        
        


class EpnmServiceTemplateEVPL(EpnmServiceTemplateBase):

    def __init__(self,
                 service_name: str,
                 a_end_node_name: str,
                 a_end_physical_interface: str,
                 a_end_uni_name: str,
                 z_end_node_name: str,
                 z_end_physical_interface: str,
                 z_end_uni_name: str,
                 service_customer: str = "Infrastructure",
                 service_type: str = "carrier-ethernet-vpn",
                 service_sub_type: str = " EVPL",
                 service_description: str = None,
                 service_mtu: int = 1522,
                 service_pwid: int = None
                 ):
        self.service_name = service_name
        self.a_end_node_name = a_end_node_name
        self.a_end_physical_interface = a_end_physical_interface
        self.a_end_uni_name = a_end_uni_name
        self.z_end_node_name = z_end_node_name
        self.z_end_physical_interface = z_end_physical_interface
        self.z_end_uni_name = z_end_uni_name
        self.service_customer = service_customer
        self.service_type = service_type
        self.service_sub_type = service_sub_type
        self.service_description = service_description if service_description is not None else str(service_name)
        self.service_mtu = service_mtu
        self.service_pwid = service_pwid

        self.a_end_line_rate = get_line_rate(self.a_end_physical_interface)
        self.z_end_line_rate = get_line_rate(self.z_end_physical_interface)

        self.service_header = EpnmServiceTemplateHeader(
            service_customer=self.service_customer,
            service_name=self.service_name,
            service_description=self.service_description,
            service_type=self.service_type,
            service_sub_type=self.service_sub_type,
            service_activate=True,
            service_mtu=1522,
            enable_cfm=True,
            ccm_interval="1 sec"

        )

        self.a_ni = EpnmNetworkInterfaceTemplate(
            name=self.a_end_uni_name,
        )
        self.z_ni = EpnmNetworkInterfaceTemplate(
            name=self.z_end_uni_name,
        )

    def get_payload(self):
        payload = {"sa.service-order-data": self.service_header.get_payload()}
        payload["sa.service-order-data"]["sa.termination-point-list"] = {
            "sa.termination-point-config": [
                {
                    "sa.tp-ref": "MD=CISCO_EPNM!ND={}!FTP=name={};lr={}".format(self.a_end_node_name, self.a_end_physical_interface, self.a_end_line_rate),
                    "sa.directionality": "source",
                    "sa.network-interface-ref": f"MD=CISCO-EPNM!NI={self.a_end_uni_name}",
                    "sa.ce-data": {
                        # "sa.l2-cp-profile": A_end_mef_option,
                        # "sa.mep-group": "UNI A",
                        "sa.untagged": "false"
                    }
                },
                {
                    "sa.tp-ref": "MD=CISCO_EPNM!ND={}!FTP=name={};lr={}".format(self.z_end_node_name, self.z_end_physical_interface, self.z_end_line_rate),
                    "sa.directionality": "sink",
                    "sa.network-interface-name": f"MD-CISCO-EPNM!NI={self.z_end_uni_name}",
                    "sa.ce-data": {
                        # "sa.l2-cp-profile": Z_end_mef_option,
                        # "sa.mep-group": "UNI Z",
                        "sa.untagged": "false"
                    }
                }
            ]
        }
        payload["sa.service-order-data"]["sa.network-interface-list"] = {
            "sa.network-interface": [
                self.a_ni.get_payload(create=False),
                self.z_ni.get_payload(create=False)
            ]
        }
        payload["sa.service-order-data"]["sa.sa.forwarding-path"] = {
            "sa.pseudowire-settings": {
                "sa.enable-control-word": "true",
                # "sa.pw-id": pw_id
            }
        }
        return payload
