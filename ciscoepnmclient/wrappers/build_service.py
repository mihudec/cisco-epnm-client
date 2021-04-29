from ciscoepnmclient.models.EpnmTemplates import *

# Constants

def build_evpl_service(
    a_node_name: str,
    a_node_physical_interface: str,
    a_uni_name: str,
    z_node_name: str,
    z_node_physical_interface: str,
    z_uni_name: str,
    service_customer: str,
    service_name: str,
    service_description: str,
    vlan_id: str,
):
    # 
    mtu = 1522

    service_ce_data = EpnmServiceCeDataTemplate(
        mtu=mtu,
        bundling=False,
        enable_cfm=True,
        ccm_interval="1 sec",
        ce_vlan_id_preservation=False,
        ce_vlan_cos_preservation=False
    )

    service_request_header = EpnmServiceHeaderTemplate(
        service_customer=service_customer,
        service_type="carrier-ethernet-vpn",
        service_sub_type="EVPL",
        service_name=service_name,
        service_description=service_description,
        service_activate=True,
        service_ce_data=service_ce_data
    )

    qinq_data = EpnmQinqDataTemplate(
        match_type="dot1q",
        vlan_id_list=vlan_id
    )

    
    termination_points = [
        EpnmTerminationPointTemplate(
            node_name=a_node_name,
            physical_interface=a_node_physical_interface,
            ni_name=a_uni_name,
            qinq_data=qinq_data,
            directionality="source"
        ),
        EpnmTerminationPointTemplate(
            node_name=z_node_name,
            physical_interface=z_node_physical_interface,
            ni_name=z_uni_name,
            qinq_data=qinq_data,
            directionality="sink"
        )
    ]
    network_interfaces = [
        EpnmNetworkInterfaceTemplate(
            name=a_uni_name,
            activate=True,
            mtu=mtu,
            bundling=False,
            service_multiplexing=True,
            enable_link_oam=False,
            operation="update"
        ),
        EpnmNetworkInterfaceTemplate(
            name=z_uni_name,
            activate=True,
            mtu=mtu,
            bundling=False,
            service_multiplexing=True,
            enable_link_oam=False,
            operation="update"
        )
    ]
    forwarding_path = {
        "sa.pseudowire-settings": {
            "sa.enable-control-word": True,
        }
    }
    service_payload = EpnmEvplServiceTemplate(
        service_request_header=service_request_header,
        termination_points=termination_points,
        network_interfaces=network_interfaces,
        forwarding_path=forwarding_path
    )

    return service_payload

