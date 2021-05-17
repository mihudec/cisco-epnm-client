from ciscoepnmclient import CiscoEpnmClientBase

class EpnmBaseManager(object):

    def __init__(self, client: CiscoEpnmClientBase):
        self.client = client

    def get_provision_status(self):
        pass

    def get_terminate_status(self):
        pass

    def __str__(self) -> str:
        return f"[{type(self).__name__}]"

    def __repr__(self) -> str:
        return self.__str__()
