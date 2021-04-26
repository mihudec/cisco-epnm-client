import re
FDN_TYPE_REGEX = re.compile(pattern=r"^[A-Z]+?(?=\=)")

def parse_fdn(fdn: str):
    data = []
    parts = fdn.split("!")
    for part in parts:
        type_delimiter_index = part.index("=")
        type_string = part[:type_delimiter_index]
        values_string = part[type_delimiter_index + 1:]
        entry = {
            "type": type_string,
            "values": []
        }
        for value_string in values_string.split(";"):
            if "=" in value_string:
                key, value = value_string.split("=")
                entry["values"].append({"key": key, "value": value})
            else:
                entry["values"].append({"key": None, "value": value_string})
        data.append(entry)
    return data

def fdn_to_dict(fdn: str):
    fdn_data = parse_fdn(fdn=fdn)
    data = {k:v for k,v in map(lambda x: (x["type"], x["values"]), fdn_data)}
    for key in data.keys():
        # Single value
        if len(data[key]) == 1:
            if data[key][0]["key"] is None:
                data[key] = data[key][0]["value"]
        elif len(data[key]) > 1:
            data[key] = {k:v for k,v in map(lambda x: (x["key"], x["value"]), data[key])}
    return data


def build_fdn(data):
    fdn = ""
    type_parts = []
    for type_part in data:
        values_string_parts = []
        for value in type_part["values"]:
            if value["key"] is None:
                values_string_parts.append(value["value"])
            else:
                values_string_parts.append(f"{value['key']}={value['value']}")
        values_string = ";".join(values_string_parts)
        type_parts.append(f"{type_part['type']}={values_string}")
    fdn = "!".join(type_parts)
    return fdn