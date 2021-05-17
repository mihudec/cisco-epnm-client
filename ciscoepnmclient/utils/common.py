import json

def jprint(obj, indent=2):
    try:
        print(json.dumps(obj=obj, indent=indent))
    except Exception as e:
        print(f"JPRINT Exception: {repr(e)}")
        print(obj)

def get_linerate(physical_interface: str):
    if physical_interface.startswith("Gi"):
        return "lr-gigabit-ethernet"
    elif physical_interface.startswith("Te"):
        return "lr-ten-gigabit-ethernet"
    elif physical_interface.startswith("Hu"):
        return "lr-hundred-gigabit-ethernet"

def alter_keys(data, func):
    new = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = alter_keys(v)
        new[func(k)] = v
    return new