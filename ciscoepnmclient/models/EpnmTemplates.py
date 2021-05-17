from typing import Union, Literal, List
from ciscoepnmclient.definitions import *
from ciscoepnmclient.utils.common import get_linerate


class EpnmRequestTemplateBase(object):

    def get_payload(self):
        pass


class EpnmQinqDataTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                 match_type: str,
                 vlan_id_list: str,
                 inner_vlan_id_list: str = None,
                 untagged: bool = None,
                 priority_tagged: bool = None,
                 match_exact: bool = None,
                 vlan_cos: str = None,
                 inner_vlan_cos: str = None,
                 ether_type: dict = None,
                 rewrite_definition: dict = None
                 ):
        self.match_type = match_type
        self.vlan_id_list = vlan_id_list
        self.inner_vlan_id_list = inner_vlan_id_list
        self.untagged = untagged
        self.priority_tagged = priority_tagged
        self.match_exact = match_exact
        self.vlan_cos = vlan_cos
        self.inner_vlan_cos = inner_vlan_cos
        self.ether_type = ether_type
        self.rewrite_definition = rewrite_definition

    def get_payload(self):
        payload = {
            "sa.match-type": self.match_type,
            "sa.vlan-id-list": self.vlan_id_list
        }
        if self.untagged is not None:
            payload["sa.untagged"] = self.untagged
        if self.priority_tagged is not None:
            payload["sa.priority-tagged"] = self.priority_tagged
        if self.match_exact is not None:
            payload["sa.match-exact"] = self.match_exact
        if self.vlan_cos is not None:
            payload["sa.vlan-cos"] = self.vlan_cos
        if self.inner_vlan_id_list is not None:
            payload["sa.inner-vlan-id-list"] = self.inner_vlan_id_list
        if self.inner_vlan_cos is not None:
            payload["sa.inner-vlan-cos"] = self.inner_vlan_cos
        if self.ether_type is not None:
            payload["sa.ether-type"] = self.ether_type
        if self.rewrite_definition is not None:
            payload["sa.rewrite-definition"] = self.rewrite_definition
        return payload


class EpnmNetworkInterfaceTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                 name: str,
                 description: str = None,
                 activate: bool = True,
                 operation: Literal["add", "update", "remove"] = None,
                 mtu: int = 1522,
                 speed: str = None,
                 duplex: str = None,
                 bundling: bool = False,
                 service_multiplexing: bool = None,
                 enable_link_oam: bool = None,
                 auto_negotiation: bool = None,
                 ):

        self.name = name
        self.description = description
        self.activate = activate
        self.operation = operation
        self.mtu = mtu
        self.speed = speed
        self.duplex = duplex
        self.bundling = bundling
        self.service_multiplexing = service_multiplexing
        self.enable_link_oam = enable_link_oam
        self.auto_negotiation = auto_negotiation

    @property
    def fdn(self):
        return f"{FDN_BASE}!NI={self.name}"

    def get_payload(self, action: Literal["create", "reference", "reference-only"]):
        payload = {}
        if action in ["reference", "reference-only"]:
            payload.update({"sa.ref": self.fdn})
        elif action in ["create"]:
            payload.update({"sa.name": self.name})

        if self.operation is not None:
            payload.update({"sa.operation": self.operation})

        ce_data = {}
        if action in ["create", "reference"]:
            if self.activate is not None:
                ce_data["sa.activate"] = self.activate
            if self.description is not None:
                ce_data["sa.description"] = self.description
            if self.mtu is not None:
                ce_data["sa.mtu"] = self.mtu
            if self.speed is not None:
                ce_data["sa.speed"] = self.speed
            if self.duplex is not None:
                ce_data["sa.duplex"] = self.duplex
            if self.auto_negotiation is not None:
                ce_data["sa.auto-negotiation"] = self.auto_negotiation
            if self.bundling is not None:
                ce_data["sa.bundling"] = self.bundling
            if self.service_multiplexing is not None:
                ce_data["sa.service-multiplexing"] = self.service_multiplexing
            if self.enable_link_oam is not None:
                ce_data["sa.enable-link-oam"] = self.enable_link_oam

            if len(ce_data):
                payload.update({"sa.ce-data": ce_data})

        return payload


class EpnmTerminationPointTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                 node_name: str,
                 physical_interface: str,
                 ni_name: str,
                 mep_group: Literal["UNI A", "UNI Z"] = None,
                 directionality: Literal["source",
                                         "sink", "bi-directional"] = None,
                 untagged: bool = None,
                 qinq_data: Union[dict, EpnmQinqDataTemplate] = None
                 ):
        self.node_name = node_name
        self.physical_interface = physical_interface
        self.ni_name = ni_name
        self.mep_group = mep_group
        self.directionality = directionality
        self.untagged = untagged
        self.mep_group = mep_group
        self.qinq_data = qinq_data

    def get_payload(self, create_network_interface: bool = False):
        payload = {
            "sa.tp-ref": f"{FDN_BASE}!ND={self.node_name}!FTP=name={self.physical_interface};lr={get_linerate(self.physical_interface)}"
        }
        if create_network_interface:
            payload["sa.network-interface-name"] = self.ni_name
        else:
            payload["sa.network-interface-ref"] = f"{FDN_BASE}!NI={self.ni_name}"

        ce_data = {}
        qinq_data = {}

        if self.directionality is not None:
            payload.update({"sa.directionality": self.directionality})

        if self.mep_group is not None:
            ce_data["sa.mep-group"] = self.mep_group
        if self.untagged is not None:
            ce_data["sa.untagged"] = self.untagged

        if self.qinq_data is not None:
            if isinstance(self.qinq_data, dict):
                qinq_data = self.qinq_data
            elif isinstance(self.qinq_data, EpnmQinqDataTemplate):
                qinq_data = self.qinq_data.get_payload()

        if len(qinq_data):
            ce_data["sa.qinq-data"] = qinq_data
        if len(ce_data):
            payload["sa.ce-data"] = ce_data
        return payload


class EpnmServiceCeDataTemplate(EpnmRequestTemplateBase):

    def __init__(self,
                 mtu: int,
                 bundling: bool,
                 ce_vlan_id_preservation: bool,
                 enable_cfm: bool = None,
                 ccm_interval: str = None,
                 ce_vlan_cos_preservation: bool = None,

                 ):
        self.mtu = mtu
        self.bundling = bundling
        self.ce_vlan_id_preservation = ce_vlan_id_preservation
        self.enable_cfm = enable_cfm
        self.ccm_interval = ccm_interval
        self.ce_vlan_cos_preservation = ce_vlan_cos_preservation

    def get_payload(self):
        payload = {
            "sa.mtu-size": self.mtu,
            "sa.bundling": self.bundling,
            "sa.ce-vlan-id-preservation": self.ce_vlan_id_preservation
        }
        if (self.enable_cfm is not None) and (self.ccm_interval is not None):
            payload.update({"sa.enable-cfm": self.enable_cfm,
                           "sa.ccm-interval": self.ccm_interval})

        if self.ce_vlan_cos_preservation is not None:
            payload.update(
                {"sa.ce-vlan-cos-preservation": self.ce_vlan_cos_preservation})

        return payload


class EpnmServiceTemplateBase(EpnmRequestTemplateBase):

    # All args optional here
    def __init__(self,
                 service_name: str = None,
                 service_type: str = None,
                 service_sub_type: str = None
                 ):
        self.service_name = service_name
        self.service_type = service_type
        self.service_sub_type = service_sub_type

    def get_terminate_payload(self):
        payload = {
            "sa.cfs-ref": f"{FDN_BASE}!CFS={self.service_name}",
            "sa.service-order-data": {
                "sa.service-name": self.service_name,
                "sa.service-type": self.service_type,
                "sa.service-subtype": self.service_sub_type
            }
        }
        return payload

    def __str__(self) -> str:
        return f"[{type(self).__name__}]"
 
    def __repr__(self) -> str:
        return self.__str__()


class EpnmServiceHeaderTemplate(EpnmServiceTemplateBase):

    def __init__(self,
                 service_customer: str,
                 service_type: str,
                 service_sub_type: str,
                 service_name: str = None,
                 service_description: str = None,
                 service_activate: bool = True,
                 service_ce_data: Union[dict, EpnmServiceCeDataTemplate] = None,
                 ):
        self.service_customer = service_customer
        self.service_type = service_type
        self.service_sub_type = service_sub_type
        self.service_name = service_name
        self.service_description = service_description
        self.service_activate = service_activate
        self.service_ce_data = service_ce_data

    def get_payload(self):
        sa_ce_data = {}
        payload = {
            "sa.customer-ref": f"{FDN_BASE}!CUSTOMER={self.service_customer}",
            "sa.service-type": self.service_type,
            "sa.service-subtype": self.service_sub_type,
        }
        if self.service_name is not None:
            payload["sa.service-name"] = self.service_name
        if self.service_description is not None:
            payload["sa.service-description"] = self.service_description
        if self.service_activate is not None:
            payload["sa.service-activate"] = self.service_activate

        service_ce_data = None
        if self.service_ce_data is not None:
            if isinstance(self.service_ce_data, dict):
                service_ce_data = dict(service_ce_data)
            elif isinstance(self.service_ce_data, EpnmServiceCeDataTemplate):
                service_ce_data = self.service_ce_data.get_payload()

        if len(sa_ce_data):
            payload["sa.ce-data"] = sa_ce_data

        if service_ce_data is not None:
            payload["sa.ce-data"] = service_ce_data
        return payload


class EpnmEvplServiceTemplate(EpnmServiceTemplateBase):

    def __init__(self,
                 service_request_header: Union[dict, EpnmServiceHeaderTemplate],
                 termination_points: List[Union[dict, EpnmTerminationPointTemplate]],
                 network_interfaces: List[Union[dict, EpnmNetworkInterfaceTemplate]],
                 forwarding_path: dict = None
                 ):
        self.service_request_header = service_request_header
        self.termination_points = termination_points
        self.network_interfaces = network_interfaces
        self.forwarding_path = forwarding_path

    def get_payload(self):
        payload = {
            "sa.service-order-data": {}
        }

        service_request_header = None
        if isinstance(self.service_request_header, dict):
            service_request_header = self.service_request_header
        elif isinstance(self.service_request_header, EpnmServiceHeaderTemplate):
            service_request_header = self.service_request_header.get_payload()

        termination_points = []
        # Convert to dict if needed
        for tp in self.termination_points:
            if isinstance(tp, dict):
                termination_points.append(tp)
            elif isinstance(tp, EpnmTerminationPointTemplate):
                termination_points.append(tp.get_payload())

        network_interfaces = []
        # Convert to dict if needed
        for ni in self.network_interfaces:
            if isinstance(ni, dict):
                network_interfaces.append(ni)
            elif isinstance(ni, EpnmNetworkInterfaceTemplate):
                network_interfaces.append(ni.get_payload(action="reference"))

        payload["sa.service-order-data"].update(service_request_header)
        payload["sa.service-order-data"]["sa.termination-point-list"] = {
            "sa.termination-point-config": termination_points
        }
        payload["sa.service-order-data"]["sa.network-interface-list"] = {
            "sa.network-interface": network_interfaces
        }
        # TODO: Convert forwarding_path to Template object
        if self.forwarding_path is not None:
            payload["sa.service-order-data"]["sa.forwarding-path"] = self.forwarding_path

        return payload
