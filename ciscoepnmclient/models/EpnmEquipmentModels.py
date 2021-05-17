from ciscoepnmclient.models import EpnmModelStructure, EpnmContainerModelStructure
from ciscoepnmclient.utils.fdn import fdn_to_dict

class EpnmPhysicalConnectorModel(EpnmModelStructure):

    _required_fields = [
        ("name", str),
        ("fdn", str)

    ]
    _optional_fields = [
        ("description", str),
        ("containing_equipment", str)
    ]
    _dict_fields = {
        "name": "fdtn.name",
        "fdn": "eq.fdn",
        "description": "fdtn.description",
        "containing_equipment": "eq.containing-equipment"
    }

class EpnmConnectorsContainerModel(EpnmContainerModelStructure):
    
    _optional_fields = [
        ("physical_connectors", list)
    ]
    _dict_fields = {
        "physical_connectors": "eq.physical-connector"
    }
    _list_fields = [
        ("physical_connectors", EpnmPhysicalConnectorModel)
    ]

class EpnmEquipmentModel(EpnmModelStructure):

    _required_fields = []
    _optional_fields = [
        ("name", str),
        ("fdn", str),
        ("description", str),
        ("connectors", EpnmConnectorsContainerModel),
        ("contained_equipment_recurse", str),
        ("contained_equipment", list),
        ("containing_equipment", str),
        ("ent_physical_index", int),
        ("equipment_type", str),
        ("hardware_version", str),
        ("is_field_replaceable_unit", str),
        ("is_physically_present", bool),
        ("is_reporting_alarms_allowed", str),
        ("manufacturer", str),
        ("operational_state_code", str),
        ("part_number", str),
        ("product_id", str),
        ("serial_number", str),
        ("service_state", str),
        ("vendor_equipment_type", str)
    ]

    _dict_fields = {
        "name": "fdtn.name",
        "description": "fdtn.description",
        "connectors": "eq.connectors",
        "contained_equipment_recurse": "eq.contained-equipment-recurse",
        "contained_equipment": "eq.contained-equipment",
        "containing_equipment": "eq.containing-equipment",
        "ent_physical_index": "eq.ent-physical-index",
        "equipment_type": "eq.equipment-type",
        "fdn": "eq.fdn",
        "hardware_version": "eq.hardware-version",
        "is_field_replaceable_unit": "eq.is-field-replaceable-unit",
        "is_physically_present": "eq.is-physically-present",
        "is_reporting_alarms_allowed": "eq.is-reporting-alarms-allowed",
        "manufacturer": "eq.manufacturer",
        "operational_state_code": "eq.operational-state-code",
        "part_number": "eq.part-number",
        "product_id": "eq.product-id",
        "serial_number": "eq.serial-number",
        "service_state": "eq.service-state",
        "vendor_equipment_type": "eq.vendor-equipment-type"
    }

    def __str__(self) -> str:
        return f"[{type(self).__name__}-{self.fdn}]"

    @property
    def fdn_dict(self):
        return fdn_to_dict(fdn=self.fdn)


