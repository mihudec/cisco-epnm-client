import requests
import json
import time
from requests.models import Response
from requests.sessions import session
import urllib3
from ciscoepnmclient.utils.get_logger import get_logger



class CiscoEpnmClientBase(object):

    def __init__(self, base_url: str, username: str, password: str, verify_ssl: bool = False, verbosity: int = 4) -> None:
        self.base_url = base_url
        self.username = username
        self.password = password
        self.verify_ssl = verify_ssl
        self.verbosity = verbosity
        self.logger = get_logger(name="EPNM", verbosity=self.verbosity, with_threads=True)
        self.logger.info(msg="Initializing EPNM Client")
        self.session = None

    def initialize(self):
        if not self.verify_ssl:
            self.logger.debug(msg="Disabling warnings for urllib3")
            urllib3.disable_warnings()
        session = requests.Session()
        if self.verify_ssl is False:
            session.verify = False
        session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Cache-Control": "no-cache"
            }
        )
        self.authenticate(session=session)
        self.session = session

    def authenticate(self, session: requests.Session):
        # Call any endpoint with HTTP Basic Auth and store the session cookie
        try:
            auth_response = session.get(
                url=f"{self.base_url}/restconf/data/v1/cisco-customer:customer",
                auth=(self.username, self.password)
                
            )
            if auth_response.status_code == 200:
                self.logger.info("Authentication Successful.")
            if auth_response.status_code == 401:
                self.logger.error("Authentication Error. Check username and password.")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection Error. Cannot connect to {self.base_url}. Exception: {repr(e)}")
        except Exception as e:
            self.logger.error(f"Encountered unhandled exception: {repr(e)}")


    def get(self, path, params: dict = None):
        response = self.session.get(
            url=self.base_url + path, 
            params=params
        )
        # self.logger.debug(f"Response: [Status: {response.status_code} Path: {path} Params: {params} Text: {response.text}]")
        return response

    def post(self, path, params: dict = None, data: dict = None):
        response = self.session.post(
            url=self.base_url + path, 
            params=params,
            data=json.dumps(data)
        )
        # self.logger.debug(f"Response: [Status: {response.status_code} Path: {path} Params: {params} Text: {response.text}]")
        return response

    def poller_get(self, path: str, check, params: dict = None, wait: int = 5, max_retries: int = 6):
        result, message, response = (None, None, None)
        retries = 0
        while result is None:
            self.logger.debug(f"Attempt: {retries}/{max_retries}")
            response = self.get(path=path, params=params)
            result, message = check(response)
            if isinstance(result, bool):
                break
            else:
                retries += 1
                if retries >= max_retries:
                    self.logger.warning("Maximum number of retries reached.")
                    break
                else:
                    self.logger.debug(f"Waiting for {wait} seconds")
                    time.sleep(wait)
        if result is True:
            self.logger.debug(f"Stopping poller. Result: {result} Message: '{message}'")
        elif result is False:
            self.logger.error(f"Stopping poller. Result: {result} Message: '{message}'")
        return (result, message, response)


    def get_data(self, response: requests.Response):
        if response.status_code == 200:
            try:
                data = response.json()
                if "com.response-message" in data.keys():
                    header = data["com.response-message"]["com.header"]
                    first = data["com.response-message"]["com.header"]["com.firstIndex"]
                    last = data["com.response-message"]["com.header"]["com.lastIndex"]
                    response_length = last - first + 1
                    # self.logger.debug(f"Response length: {response_length}, firstIndex: {first}, lastIndex: {last}")
                    inner_data = None
                    if data["com.response-message"]["com.data"] != "":
                        inner_data = data["com.response-message"]["com.data"]
                    else:
                        self.logger.debug("Response contains no data.")
                    return inner_data 
            except KeyError as e:
                self.logger.error(f"KeyError while trying to unpack data from response. Error: {repr(e)}")
            except Exception as e:
                self.logger.error(f"Encountered unhandled exception: {repr(e)}")

            return response.json()

        elif response.status_code == 400:
            self.logger.error(f"BadRequest. Error: {response.text}")
        elif response.status_code == 401:
            self.logger.error("Authentication Error. Check username and password.")
            return response
        return response

    def get_nodes(self, name: str = None, fdn: str = None, params: dict = None):
        if any([name, fdn]) and params is None:
            params = {}
        if name is not None:
            params.update({"name": name})
        if fdn is not None:
            params.update({"fdn": fdn})
        path = "/restconf/data/v1/cisco-resource-physical:node"
        nodes = self.get_data(self.get(path=path, params=params))
        if nodes is not None:
            nodes = nodes["nd.node"]
            self.logger.debug(f"Received {len(nodes)} nodes.")
        return nodes

    def get_services(self, fdn: str = None, service_type: str = None, params: dict = None):
        if any([service_type]) and params is None:
            params = {}
        path = "/restconf/data/v1/cisco-service-network:virtual-connection"
        service_types = ["carrier-ethernet-vpn", "tdm-cem", "mpls-te-tunnel", "mpls-l3-vpn", "optical"]
        if service_type is not None:
            if service_type not in service_types:
                self.logger.warning(f"Unsuported service-type: {service_type}")
                return None
            else:
                params.update({"type": service_type})
        if fdn is not None:
            params.update({"fdn": fdn})
        services = self.get_data(self.get(path=path, params=params))
        if services is not None:
            services = services["vc.virtual-connection"]
            self.logger.debug(f"Received {len(services)} services.")
        return services

    def get_customers(self):
        path = "/restconf/data/v1/cisco-customer:customer"
        customers = self.get_data(self.get(path=path))
        return customers

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

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.logger.info("Session closed.")


    def __str__(self) -> str:
        return f"[CiscoEpnmClient-{self.base_url}]"

    def __repr__(self) -> str:
        return self.__str__()
