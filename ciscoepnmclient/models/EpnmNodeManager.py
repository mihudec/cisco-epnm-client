from ciscoepnmclient.models import EpnmBaseManager
from ciscoepnmclient import CiscoEpnmClientBase


class EpnmNodeManager(EpnmBaseManager):

    def __init__(self, client: CiscoEpnmClientBase):
        super().__init__(client=client)

    