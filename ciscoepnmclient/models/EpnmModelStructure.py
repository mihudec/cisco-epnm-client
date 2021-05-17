from ciscoepnmclient.utils.fdn import fdn_to_dict
import collections
class EpnmModelStructure(object):

    _required_fields = []
    _optional_fields = []
    _dict_fields = {}

    def _init_arg(self, expected_type, value):
        if isinstance(value, expected_type):
            return value
        else:
            if isinstance(value, collections.Mapping):
                return expected_type(**value)
            else: 
                return expected_type(value)

    def __init__(self, **kwargs):
        required_field_names = []
        required_field_types = []
        optional_field_names = []
        optional_field_types = []
        if len(self._required_fields):
            required_field_names, required_field_types = zip(*self._required_fields)
            assert([isinstance(name, str) for name in required_field_names])
            assert([isinstance(type_, type) for type_ in required_field_types])
        if len(self._optional_fields):
            optional_field_names, optional_field_types = zip(*self._optional_fields)
            assert([isinstance(name, str) for name in optional_field_names])
            assert([isinstance(type_, type) for type_ in optional_field_types])

        # Required arguments
        for name, field_type in self._required_fields:
            dict_field_name = self._dict_fields.get(name)
            if name in kwargs.keys():
                setattr(self, name, self._init_arg(expected_type=field_type, value=kwargs.pop(name)))
            elif dict_field_name in kwargs.keys():
                setattr(self, name, self._init_arg(expected_type=field_type, value=kwargs.pop(dict_field_name)))
            else: 
                raise ValueError(f"Required Field MISSING: {name}") 
        # Optional arguments
        for name, field_type in self._optional_fields:
            dict_field_name = self._dict_fields.get(name)
            if name in kwargs.keys():
                setattr(self, name, self._init_arg(expected_type=field_type, value=kwargs.pop(name)))
                continue
            if dict_field_name not in kwargs.keys():
                setattr(self, name, None)
            else:
                setattr(self, name, self._init_arg(expected_type=field_type, value=kwargs.pop(dict_field_name)))

        # Check for any remaining arguments
        if kwargs:
            raise TypeError('Invalid arguments(s): {}'.format(','.join(kwargs)))


    @classmethod
    def from_dict(cls, data):
        obj = cls.__new__(cls)
        super(cls, obj).__init__(**data)
        return obj

    def to_dict(self):
        data = {}
        # Required fields first
        if hasattr(self, "_required_fields"):
            for key, value in map(lambda x: (x[0], getattr(self, x[0])), self._required_fields):
                if isinstance(value, EpnmModelStructure):
                    value = value.to_dict()
                data.update({self._dict_fields[key]: value})
        # Optional Fields
        if hasattr(self, "_required_fields"):
            for key, value in map(lambda x: (x[0], getattr(self, x[0])), self._optional_fields):
                if value is None:
                    continue
                if isinstance(value, EpnmModelStructure):
                    value = value.to_dict()
                data.update({self._dict_fields[key]: value})

        return data

    @property
    def fdn_dict(self):
        raise NotImplementedError(f"Class {type(self).__name__} does not implement 'fdn_dict' property.")

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"[{type(self).__name__}]"

class EpnmContainerModelStructure(EpnmModelStructure):

    _required_fields = []
    _optional_fields = []
    _dict_fields = {}
    _list_fields = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for name, type_ in self._list_fields:
            if hasattr(self, name):
                if isinstance(getattr(self, name), list):
                    # Convert all list items to specified type
                    if issubclass(type_, EpnmModelStructure):
                        setattr(self, name, [type_(**x) for x in getattr(self, name)])

    def to_dict(self):
        data = super().to_dict()
        for name, type_ in self._list_fields:
            if self._dict_fields[name] in data.keys() and isinstance(data[self._dict_fields[name]], list):
                data[self._dict_fields[name]] = [x.to_dict() for x in data[self._dict_fields[name]] if isinstance(x, EpnmModelStructure)]
        return data
