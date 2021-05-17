from ciscoepnmclient.models import EpnmModelStructure

class EpnmQinqModel(EpnmModelStructure):

    _required_fields = [
        ("match_type", str),
        ("vlan_id_list", str)
    ]

    _optional_fields = [
        ("inner_vlan_id_list", str),
        ("untagged", bool),
        ("priority_tagged", bool),
        ("match_exact", bool),
        ("vlan_cos", str),
        ("inner_vlan_cos", str),
        ("ether_type", dict),
        ("rewrite_definition", dict)
    ]

    _dict_fields = {
        "match_type": "sa.match-type",
        "vlan_id_list": "sa.vlan-id-list",
        "inner_vlan_id_list": "sa.inner-vlan-id-list",
        "untagged": "sa.untagged",
        "priority_tagged": "sa.priority-tagged",
        "match_exact": "sa.match-exact",
        "vlan_cos": "sa.vlan-cos",
        "inner_vlan_cos": "sa.inner-vlan-cos",
        "ether_type": "sa.ether-type",
        "rewrite_definition": "sa.rewrite-definition",
    }