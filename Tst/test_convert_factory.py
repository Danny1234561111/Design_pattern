# test_convert_factory.py

import unittest
from Src.Convert.convert_factory import convert_factory
from datetime import datetime

class TestConvertFactory(unittest.TestCase):
    def test_convert_factory_basic(self):
        factory = convert_factory()
        item = 123
        result = factory.Convert(item)
        self.assertEqual(result, [{'value': 123}])

    def test_convert_factory_datetime(self):
        factory = convert_factory()
        dt = datetime(2021, 1, 1, 12, 0)
        result = factory.Convert(dt)
        self.assertEqual(result, [{'date': "2021-01-01 12:00:00"}])

    def test_convert_factory_reference(self):
        class TestRef:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        ref_obj = TestRef(1, "Reference")
        factory = convert_factory()
        result = factory.Convert(ref_obj)
        self.assertEqual(result, [{'id': 1, 'name': 'Reference'}])

if __name__ == '__main__':
    unittest.main()