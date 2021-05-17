import pydantic
import json
from ciscoepnmclient.serializers import EpnmBaseSerializer


class EpnmBaseModel(pydantic.BaseModel):

    class Config:
        json_loads = EpnmBaseSerializer.loads
        json_dumps = EpnmBaseSerializer.dumps


