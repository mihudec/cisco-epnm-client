import json
from ciscoepnmclient.utils.common import alter_keys


class EpnmBaseSerializer(object):   

    

    @staticmethod
    def dumps(data: dict, default, prefix="sa.") -> str:
        data = alter_keys(data=data, func=lambda x: f"{prefix}{x.replace('_', '-')}")
        return json.dumps(obj=data, default=default)

    @staticmethod
    def loads(text: str) -> dict:
        data = json.loads(text)
        data = alter_keys(data=data, func=lambda x: x.split('.')[1].replace('-', '_'))
        return data




