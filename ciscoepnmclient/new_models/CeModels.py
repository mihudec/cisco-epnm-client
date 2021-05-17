from pydantic.utils import ValueItems
from ciscoepnmclient.new_models import EpnmBaseModel
from pydantic import validator, root_validator
from typing import Optional
from typing_extensions import Literal

from ciscoepnmclient.definitions import FDN_BASE


class EpnmQinqDataModel(EpnmBaseModel):
    
    match_type: str
    vlan_id_list: str
    inner_vlan_id_list: Optional[str]
    untagged: Optional[bool] = False
    priority_tagged: Optional[bool]
    match_exact: Optional[bool]
    vlan_cos: Optional[str]
    inner_vlan_cos: Optional[str]
    ether_type: Optional[dict]
    rewrite_definition: Optional[dict]


class EpnmNiModel(EpnmBaseModel):

    _fdn_string = "{base}!NI={name}"

    name: str
    ref: str
    description: Optional[str]
    activate: bool = True
    operation: Optional[Literal["add", "update", "remove"]]
    mtu: int = 1522
    speed: Optional[str]
    duplex: Optional[str]
    bundling: bool = False
    service_multiplexing: Optional[bool]
    enable_link_oam: Optional[bool]
    auto_negotiation: Optional[bool]

    @root_validator(pre=True)
    def generate_ref(cls, values):
        if values.get("name") and values.get("ref"):
            return values
        elif values.get("name") and not values.get("ref"):
            values["ref"] = cls._fdn_string.format(base=FDN_BASE, name=values.get("name"))
        return values




if __name__ == '__main__':
    model = EpnmNiModel(name="EPNM")
    
    print(model.json(exclude_none=True))