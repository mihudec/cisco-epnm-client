from ciscoepnmclient.models import EpnmModelStructure

class EpnmCeDataModel(EpnmModelStructure):
    pass

class EpnmCeDataServiceModel(EpnmCeDataModel):

    _required_fields = [
        ("bundling", bool),
        ("ce_vlan_id_preservation", bool),
        ("mtu", int)
    ]

    _optional_fields = [
        ("ce_vlan_cos_preservation", bool),
        ("enable_cfm", bool),
        ("cfm_domain_name", str),
        ("cfm_domain_level", str),
        ("ccm_interval", str),
        ("configure_remote_mep", bool),
        ("fault_management_map", dict),
        ("max_uni_endpoints", int),
        ("vpn_id", int),
        ("auto_allocate_vlan_id", bool)

    ]
    
    _dict_fields = {
        "bundling": "sa.bundling",
        "ce_vlan_id_preservation": "sa.ce-vlan-id-preservation",
        "ce_vlan_cos_preservation": "sa.ce-vlan-cos-preservation",
        "mtu": "sa.mtu-size",
        "enable_cfm": "sa.enable-cfm",
        "cfm_domain_name": "sa.cfm-domain-name",
        "cfm_domain_level": "sa.cfm-domain-level",
        "ccm_interval": "sa.ccm_interval",
        "configure_remote_mep": "sa.configure-remote-mep",
        "fault_management_map": "sa.fault-management-map",
        "max_uni_endpoints": "sa.max-uni-endpoints",
        "vpn_id": "sa.vpn-id",
        "auto_allocate_vlan_id": "sa.auto-allocate-vlan-id"
    }