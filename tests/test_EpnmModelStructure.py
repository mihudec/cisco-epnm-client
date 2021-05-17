import unittest
import unittest
from unittest.signals import installHandler
from ciscoepnmclient.models import EpnmModelStructure

class TestEpnmModelStructure(unittest.TestCase):

    TEST_CLASS = EpnmModelStructure
    
    _REQUIRED_FIELD_NAMES = [x[0] for x in TEST_CLASS._required_fields]
    _OPTIONAL_FIELD_NAMES = [x[0] for x in TEST_CLASS._optional_fields]

    def test_init(self):
        instance = self.TEST_CLASS()
        self.assertIsInstance(instance, self.TEST_CLASS)

    def test_is_subclass(self):
        self.assertTrue(
            issubclass(self.TEST_CLASS, EpnmModelStructure)
        )

    def test_has_to_dict(self):
        self.assertTrue(
            callable(
                getattr(self.TEST_CLASS, "to_dict")
            )
        )

    def test_has_from_dict(self):
        self.assertTrue(
            callable(
                getattr(self.TEST_CLASS, "from_dict")
            )
        )

    def test_fields_have_dict_mapping(self):
        all_fields = set()
        all_fields.update([x[0] for x in self.TEST_CLASS._required_fields])
        all_fields.update([x[0] for x in self.TEST_CLASS._optional_fields])

        dict_field_keys = set(self.TEST_CLASS._dict_fields.keys())
        self.assertSetEqual(all_fields, dict_field_keys)

    def test_field_is_defined_once(self):
        required_fields = set([x[0] for x in self.TEST_CLASS._required_fields])
        optional_fields = set([x[0] for x in self.TEST_CLASS._optional_fields])
        self.assertTrue(required_fields.isdisjoint(optional_fields))


if __name__ == '__main__':
    unittest.main()
