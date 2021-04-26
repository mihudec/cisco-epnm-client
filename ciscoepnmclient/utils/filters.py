MD_PREFIX = "MD=CISCO_EPNM"
def filter_network_interface(data: list, fdn: str = None, name: str = None, interface_type: str = None, node_name: str = None, physical_interface: str = None, custommer: str = None, status: str = None):
    if isinstance(data, list):
        if fdn is not None:
            data = filter(lambda x: x["ni.fdn"] == fdn, data)
        if name is not None:
            data = filter(lambda x: x["ni.fdn"] == f"{MD_PREFIX}!NI={name}", data)
        if interface_type is not None:
            data = filter(lambda x: f"{interface_type}" in x["ni.type"], data)
        if node_name is not None:
            data = filter(lambda x: f"{MD_PREFIX}!ND={node_name}" in x["ni.port-ref"], data)
        if physical_interface is not None:
            data = filter(lambda x: f"FTP=name={physical_interface}" in x["ni.port-ref"], data)
        if custommer is not None:
            data = filter(lambda x: f"CUSTOMER={custommer}" in x["ni.subscriber-ref"], data)
        if status is not None:
            data = filter(lambda x: x["ni.status"] == status, data)
        data = list(data)
    elif data is None:
        pass
    return data
    