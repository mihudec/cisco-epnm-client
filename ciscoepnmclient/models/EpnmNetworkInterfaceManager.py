from requests.models import Response
from ciscoepnmclient.CiscoEpnmClientBase import CiscoEpnmClientBase
from ciscoepnmclient.models.EpnmBaseManager import EpnmBaseManager
from ciscoepnmclient.utils.filters import filter_network_interface
from ciscoepnmclient.utils.checks import *
from ciscoepnmclient.utils.fdn import *
from ciscoepnmclient.utils import get_logger
from ciscoepnmclient.models.EpnmTemplates import *



def get_network_interfaces(self, fdn: str = None, params: dict = None):
        if any([fdn]) and params is None:
            params = {}
        # self.logger.debug(f"FDN: {fdn} Params: {params}")
        path = "/restconf/data/v1/cisco-service-network:network-interface"
        if fdn is not None:
            if params is None:
                params = {}
            params.update({"fdn": fdn})
        network_interfaces = self.get_data(self.get(path=path, params=params))
        if network_interfaces is None:
            self.logger.info("Received 0 elements.")
        else:
            network_interfaces = network_interfaces["ni.network-interface"]
            if isinstance(network_interfaces, dict):
                network_interfaces = [network_interfaces]
        return network_interfaces

class EpnmNetworkInterfaceManager(EpnmBaseManager):

    PROVISION_PATH = "/restconf/operations/v1/cisco-service-activation:provision-service"
    TERMINATE_PATH = "/restconf/operations/v1/cisco-service-activation:terminate-service"
    GET_PATH = "/restconf/data/v1/cisco-service-network:network-interface"


    def __init__(self, client: CiscoEpnmClientBase):
        self.client = client

    def get_response_data(self, response: Response):
        data = None
        try:
            data = response.json()
            if data["com.response-message"]["com.data"] != "":
                data = data["com.response-message"]["com.data"]
            else:
                self.logger.info("Response contains no data.")
        # Hail Mary
        except Exception as e:
            data = None
            self.client.logger.error("Failed to extract data from response.")
            self.client.logger.debug(f"Failed response text: {response.text}")

    def get_network_interfaces(self, fdn: str = None, params: dict = None):
        if any([fdn]) and (params is None):
            params = {}
        if fdn is not None:
            params.update({"fdn": fdn})
        response = self.client.get(path=self.GET_PATH, params=params)
        data = self.get_response_data(response=response)
            
    

    def check_interface_exists(self, fdn: str = None, node_name: str = None, physical_interface: str = None):
        network_interfaces = []
        if fdn is not None:
            self.client.logger.debug(f"Checking existence of NI FDN: '{fdn}'")
            network_interfaces = self.client.get_network_interfaces(fdn=fdn)
        else:
            network_interfaces = self.client.get_network_interfaces()
            if node_name is None or physical_interface is None:
                self.client.logger.error(
                    "You have to provide either fdn or node_name and physical_interface")
                return False
            else:
                self.client.logger.debug(
                    f"Filtering network interfaces for node_name={node_name} and physical_interface={physical_interface}")
                network_interfaces = filter_network_interface(
                    data=network_interfaces, node_name=node_name, physical_interface=physical_interface)
        if network_interfaces is None or len(network_interfaces) == 0:
            self.client.logger.debug("Found no matching network interface.")
            return False
        elif len(network_interfaces) == 1:
            self.client.logger.debug(
                f"Found matching network interface. FDN: {network_interfaces[0]['ni.fdn']}")
            return network_interfaces[0]['ni.fdn']
        else:
            self.client.logger.error(
                "Found multiple candidates for network interface. This should not happen (probably).")

    def create_network_interface(self, data, force_create: bool = False, confirm: bool = False):
        name = data["sa.service-order-data"]["sa.termination-point-list"]["sa.termination-point-config"]["sa.network-interface-name"]
        # Check if interface name already exists
        interface_exists = None
        # Construct FDN
        fdn = f"{FDN_BASE}!NI={name}"
        interface_exists = self.check_interface_exists(fdn=fdn)
        if isinstance(interface_exists, str):
            self.client.logger.warning(
                f"Network Interface '{name}' already exists. FDN: '{interface_exists}'")
            interface_exists = True
        elif interface_exists is False:
            # Check if node_name and physical_interface already have NI assigned
            tp_ref_data = fdn_to_dict(
                data["sa.service-order-data"]["sa.termination-point-list"]["sa.termination-point-config"]["sa.tp-ref"])
            node_name = tp_ref_data["ND"]
            physical_interface = tp_ref_data["FTP"]["name"]
            self.client.logger.debug(
                f"Checking existence of NI node_name: '{node_name}', physical_interface: '{physical_interface}'")
            interface_candidates = filter_network_interface(data=self.client.get_network_interfaces(
            ), node_name=node_name, physical_interface=physical_interface)
            if interface_candidates is None:
                interface_exists = False
            else:
                if len(interface_candidates) > 0:
                    self.client.logger.warning(
                        f"Found {len(interface_candidates)} existing NIs node_name: '{node_name}', physical_interface: '{physical_interface}'")
                    for candidate in interface_candidates:
                        self.client.logger.warning(
                            f"NI FDN: '{candidate['ni.fdn']}' Status: '{candidate['ni.status']}'")
                    interface_exists = True
                    if force_create:
                        self.client.logger.warning(
                            f"FORCE CREATE: Trying to force creatin of NI FDN: '{fdn}'")
                        # Override
                        interface_exists = False

        if interface_exists is True:
            return False
        if interface_exists is False:
            self.client.logger.info(f"Creating Network Interface Name: {name}")
            response = self.client.post(path=self.PROVISION_PATH, data=data)
            if response.status_code == 200:
                response_data = response.json()
                if response_data["sa.provision-service-response"]["sa.completion-status"] == "SUBMITTED":
                    request_id = response_data["sa.provision-service-response"]["sa.request-id"]
                    self.client.logger.info(f"Request successfully SUBMITTED. Request ID: {request_id}")
                    if confirm:
                        job_status = self.get_provision_status(request_id=request_id)
                        return job_status
                    else:
                        return True
                else:
                    self.client.logger.warning(
                        f"Did not receive confirmation of successful request submission. Response: {response.text}")
                    return False

    def delete_network_interface(self, fdn: str, force_delete: bool = False, confirm: bool = False):
        """Method for deleting UNI Interfaces

        Args:
            fdn (str): FDN of the UNI
            force_delete (bool, optional): Try deleting UNIs in Ceased state. Defaults to False.
        """
        # Check if interface exists
        interface_exists = self.check_interface_exists(fdn=fdn)
        if isinstance(interface_exists, str):
            self.client.logger.debug(
                f"Interface with FDN: {fdn} currently exists and will be deleted.")
        elif interface_exists is False:
            # Better check another way
            self.client.logger.debug("Checking for NI existence other way...")
            interface_candidates = filter_network_interface(
                data=self.client.get_network_interfaces(), fdn=fdn)
            if interface_candidates is None:
                interface_exists = False
            else:
                if len(interface_candidates) > 0:
                    self.client.logger.warning(
                        f"Interface with FDN: {fdn} was discovered, eventhough it should not exist.")
                    for candidate in interface_candidates:
                        self.client.logger.warning(
                            f"NI FDN: '{candidate['ni.fdn']}' Status: '{candidate['ni.status']}'")
                    interface_exists = False
                    if force_delete:
                        # Override
                        self.client.logger.warning(
                            f"FORCE DELETE: Trying to force deletion of NI FDN: {fdn}")
                        interface_exists = True

        uni_terminate_req = {
            "sa.ni-ref": f"{fdn}",
            "sa.service-order-data": {
                "sa.service-type": "carrier-ethernet-vpn",
                "sa.service-subtype": "UNI"

            }
        }
        if interface_exists is False:
            return False
        if interface_exists:
            self.client.logger.debug(f"Deleting Network Interface FDN: {fdn}")
            response = self.client.post(
                path=self.TERMINATE_PATH, data=uni_terminate_req)
            if response.status_code == 200:
                response_data = response.json()
                if response_data["sa.terminate-service-response"]["sa.completion-status"] == "SUBMITTED":
                    request_id = response_data["sa.terminate-service-response"]["sa.request-id"]
                    self.client.logger.info(f"Request successfully SUBMITTED. Request ID: {request_id}")
                    if confirm:
                        job_status = self.get_terminate_status(request_id=request_id)
                        return job_status
                    else:
                        return True
                else:
                    self.client.logger.warning(
                        f"Did not receive confirmation of successful request submission. Response: {response.text}")
                    return False

    def get_provision_status(self, request_id: str, wait: int = 10, max_retries: int = 12):
        params = {"request-id": request_id}
        self.client.logger.info(
            f"Getting status for provisioning job. Request ID: {request_id}")
        result, message, response = self.client.poller_get(
            path=self.PROVISION_PATH, check=check_provision_uni, params=params, wait=wait, max_retries=max_retries)
        if result is True:
            self.client.logger.info(
                f"Sucessfully created NI. RequestID: {request_id}")
            job_status = True
        elif result is False:
            self.client.logger.error(
                f"Failed to create NI. RequestID: {request_id}")
            job_status = False
        else:
            self.client.logger.warning(
                f"Unhandled Error: Did not receive status in specified timeout. RequestID: {request_id}")
        return job_status

    def get_terminate_status(self, request_id: str, wait: int = 10, max_retries: int = 12):
        params = {"request-id": request_id}
        job_status = None
        self.client.logger.info(
            f"Getting status for termination job. Request ID: {request_id}")
        result, message, response = self.client.poller_get(
            path=self.TERMINATE_PATH, check=check_terminate_uni, params=params, wait=wait, max_retries=max_retries)
        if result is True:
            self.client.logger.info(
                f"Sucessfully deleted NI. RequestID: {request_id}")
            job_status = True
        elif result is False:
            self.client.logger.error(
                f"Failed to delete NI. RequestID: {request_id}")
            job_status = False
        else:
            self.client.logger.warning(
                f"Unhandled Error: Did not receive status in specified timeout. RequestID: {request_id}")
        return job_status

    def get_create_payload(self,
                           name: str,
                           node_name: str,
                           physical_interface: str,
                           service_customer: str = "Infrastructure",
                           mtu: int = 1522,
                           description: str = None,
                           bundling: bool = False,
                           service_multiplexing: bool = False
                           ):
        service_header = EpnmServiceHeaderTemplate(
            service_customer=service_customer,
            service_type="carrier-ethernet-vpn",
            service_sub_type="UNI",
            service_activate=True
        )
        termination_point = EpnmTerminationPointTemplate(
            node_name=node_name,
            physical_interface=physical_interface,
            ni_name=name
        )
        network_interface = EpnmNetworkInterfaceTemplate(
            name=name,
            description=description,
            operation="add",
            activate=True,
            mtu=mtu,
            bundling=bundling,
            service_multiplexing=service_multiplexing,
            enable_link_oam=False

        )
        payload = {
            "sa.service-order-data": service_header.get_payload()
        }
        payload["sa.service-order-data"]["sa.termination-point-list"] = {
            "sa.termination-point-config": termination_point.get_payload(create_network_interface=True)
        }
        payload["sa.service-order-data"]["sa.network-interface-list"] = {
            "sa.network-interface": network_interface.get_payload(create=True)
        }

        return payload

    def post_req_template(self, name: str, node_name: str, physical_interface: str, customer: str, description: str = None):
        uni_post_req = {
            "sa.service-order-data": {
                "sa.customer-ref": f"MD=CISCO_EPNM!CUSTOMER={customer}",
                "sa.service-type": "carrier-ethernet-vpn",
                "sa.service-subtype": "UNI",
                "sa.service-activate": True,
                "sa.termination-point-list": {
                    "sa.termination-point-config": {
                        "sa.tp-ref": f"MD=CISCO_EPNM!ND={node_name}!FTP=name={physical_interface};lr=lr-gigabit-ethernet",
                        "sa.network-interface-name": name
                    }
                },
                "sa.network-interface-list": {
                    "sa.network-interface": {
                        "sa.name": name,
                        "sa.ce-data": {
                            "sa.activate": True,
                            "sa.description": description if description is not None else "",
                            "sa.mtu": 1522,
                            "sa.bundling": False,
                            "sa.service-multiplexing": True,
                            "sa.enable-link-oam": False
                        }
                    }
                }
            }
        }
        return uni_post_req
