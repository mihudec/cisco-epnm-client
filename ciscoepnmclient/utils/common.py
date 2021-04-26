import json

def jprint(obj, indent=2):
    try:
        print(json.dumps(obj=obj, indent=indent))
    except Exception:
        print(obj)

def get_line_rate(physical_interface: str):
    if physical_interface.startswith("Gi"):
        return "lr-gigabit-ethernet"
    elif physical_interface.startswith("Te"):
        return "lr-ten-gigabit-ethernet"
    elif physical_interface.startswith("Hu"):
        return "lr-hundred-gigabit-ethernet"