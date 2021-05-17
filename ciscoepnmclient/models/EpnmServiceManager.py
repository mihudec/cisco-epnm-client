import requests
from requests.models import Response
from ciscoepnmclient.CiscoEpnmClientBase import CiscoEpnmClientBase
from ciscoepnmclient.models.EpnmBaseManager import EpnmBaseManager
from ciscoepnmclient.utils.checks import *
from ciscoepnmclient.utils.fdn import *
from ciscoepnmclient.models.EpnmTemplates import *


class EpnmServiceManager(EpnmBaseManager):

    
    PROVISION_PATH = "/restconf/operations/v1/cisco-service-activation:provision-service"
    TERMINATE_PATH = "/restconf/operations/v1/cisco-service-activation:terminate-service"
    GET_PATH = "/restconf/data/v1/cisco-service-network:virtual-connection"
    RESYNC_PATH = "/restconf/operations/v1/cisco-service-activation:resync-service"

    def __init__(self, client: CiscoEpnmClientBase):
        self.client = client

    def get_response_data(self, response: Response):
        data = None
        try:
            data = response.json()
            if data["com.response-message"]["com.data"] != "":
                data = data["com.response-message"]["com.data"]
            else:
                self.client.logger.debug("Response contains no data.")
                data = None
        # Hail Mary
        except Exception as e:
            data = None
            self.client.logger.error(f"Failed to extract data from response. Exception: {repr(e)}")
            self.client.logger.debug(f"Failed response text: {response.text}")

        return data

    def get_services(self, fdn: str = None, service_type: str = None, params: dict = None):
        if any([service_type]) and params is None:
            params = {}
        service_types = ["carrier-ethernet-vpn", "tdm-cem", "mpls-te-tunnel", "mpls-l3-vpn", "optical"]
        if service_type is not None:
            if service_type not in service_types:
                self.client.logger.warning(f"Unsuported service-type: {service_type}")
                return None
            else:
                params.update({"type": service_type})
        if fdn is not None:
            params.update({"fdn": fdn})
        services = self.client.get_data(self.client.get(path=self.GET_PATH, params=params))
        if services is not None:
            services = services["vc.virtual-connection"]
            if isinstance(services, dict):
                services = [services]
            self.client.logger.debug(f"Received {len(services)} services.")
        return services

    def check_service_exists(self, fdn: str) -> bool:
        """Function for checking service existence.

        Args:
            fdn (str): FDN of the service

        Returns:
            bool: `True` if service exists, `False` if it does not
        """
        result = None
        response = self.client.get(path=self.GET_PATH, params={"fdn": fdn})
        services = self.get_response_data(response=response)
        if services is None or len(services) == 0:
            self.client.logger.debug("Found no matching service.")
            result = False
        else:
            if isinstance(services, dict):
                services = services["vc.virtual-connection"]
                if isinstance(services, dict):
                    services = [services]
            if len(services) == 1:
                self.client.logger.debug("Found matching service.")
                result = True
            else:  
                self.client.logger.error("Found multiple candidates for service. This should not happen (probably).")
        return result

    def create_service(self, data: Union[dict, EpnmServiceTemplateBase], confirm: bool = False):

        if isinstance(data, dict):
            pass
        elif isinstance(data, EpnmServiceTemplateBase):
            data = data.get_payload()

        service_name = data["sa.service-order-data"]["sa.service-name"]
        service_fdn = f"{FDN_BASE}!VC={service_name}"
        service_exists = self.check_service_exists(fdn=service_fdn)
        if service_exists:
            self.client.logger.warning(f"Service with name '{service_name}' already exists.")
            return False

        # Create service
        self.client.logger.info(f"Creating service. Name: '{service_name}'")
        response = self.client.post(path=self.PROVISION_PATH, data=data)
        response_data = None
        try:
            response_data = response.json()
            if "sa.provision-service-response" in response_data.keys():
                response_data = response_data["sa.provision-service-response"]
            elif "rc.errors" in response_data.keys():
                response_data = response_data["rc.errors"]["error"]
                self.client.logger.error(f"Error while creating service: Error-message: '{response_data['error-message']}'")
                return False
        except Exception as e:
            self.client.logger.error(f"Unhandled Exception occured. Exception: '{repr(e)}' Response Text: '{response.text}'")
        if response_data is None:
            return False
        if response_data["sa.completion-status"] == "SUBMITTED":
            request_id = response_data["sa.request-id"]
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
            
    def delete_service(self, data: dict, confirm: bool = False):
        service_name = data["sa.service-order-data"]["sa.service-name"]
        service_fdn = f"{FDN_BASE}!VC={service_name}"
        service_exists = self.check_service_exists(fdn=service_fdn)
        if service_exists is False:
            self.client.logger.info(f"Service with FDN: '{service_fdn}' does not exist.")
            return False
        elif service_exists is True:
            self.client.logger.debug(f"Service with FDN: '{service_fdn}' exists.")
            self.client.logger.info(f"Deleting service. FDN: '{service_fdn}'")
            response = self.client.post(path=self.TERMINATE_PATH, data=data)
            response_data = None
            try:
                response_data = response.json()
                if "sa.terminate-service-response" in response_data.keys():
                    response_data = response_data["sa.terminate-service-response"]
                elif "rc.errors" in response_data.keys():
                    response_data = response_data["rc.errors"]["error"]
                    self.client.logger.error(f"Error while deleting service: Error-message: '{response_data['error-message']}'")
                    return False
            except Exception as e:
                self.client.logger.error(f"Unhandled Exception occured. Exception: '{repr(e)}' Response Text: '{response.text}'")
            if response_data is None:
                return False
            if response_data["sa.completion-status"] == "SUBMITTED":
                request_id = response_data["sa.request-id"]
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

    def resync_service(self, data: str):
        pass

    def get_provision_status(self, request_id: str, wait: int = 10, max_retries: int = 30):
        params = {"request-id": request_id}
        self.client.logger.info(
            f"Getting status for provisioning job. Request ID: {request_id}")
        result, message, response = self.client.poller_get(
            path=self.PROVISION_PATH, check=check_provision_service, params=params, wait=wait, max_retries=max_retries)
        job_status = False
        if result is True:
            self.client.logger.info(
                f"Sucessfully created Service. RequestID: {request_id}")
            job_status = True
        elif result is False:
            self.client.logger.error(
                f"Failed to create Service. RequestID: {request_id} Message: ")
            job_status = False
        else:
            self.client.logger.warning(
                f"Unhandled Error: Did not receive status in specified timeout. RequestID: {request_id}")
        return job_status

    def get_terminate_status(self, request_id: str, wait: int = 10, max_retries: int = 30):
        params = {"request-id": request_id}
        job_status = None
        self.client.logger.info(
            f"Getting status for termination job. Request ID: {request_id}")
        result, message, response = self.client.poller_get(
            path=self.TERMINATE_PATH, check=check_terminate_service, params=params, wait=wait, max_retries=max_retries)
        job_status = False
        if result is True:
            self.client.logger.info(
                f"Sucessfully deleted Service. RequestID: {request_id}")
            job_status = True
        elif result is False:
            self.client.logger.error(
                f"Failed to delete Service. RequestID: {request_id}")
            job_status = False
        else:
            self.client.logger.warning(
                f"Unhandled Error: Did not receive status in specified timeout. RequestID: {request_id}")
        return job_status