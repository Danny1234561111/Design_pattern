# test_converters.py

import unittest
from datetime import datetime
from Src.Convert.basic_convertor import basic_convertor
from Src.Convert.datetime_convertor import datetime_convertor
from Src.Convert.reference_convertor import reference_convertor
from datetime import datetime

class TestConverters(unittest.TestCase):
    def test_basic_convertor(self):
        converter = basic_convertor()
        self.assertEqual(converter.Convert(123), {"value": 123})
        self.assertEqual(converter.Convert("test"), {"value": "test"})
        self.assertRaises(ValueError, converter.Convert, [1, 2, 3])
    
    def test_datetime_convertor(self):
        converter = datetime_convertor()
        dt = datetime(2021, 1, 1, 12, 0)
        self.assertEqual(converter.Convert(dt), {"date": "2021-01-01 12:00:00"})
        self.assertRaises(ValueError, converter.Convert, "not_a_datetime")
    
    def test_reference_convertor(self):
        class TestRef:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        ref_obj = TestRef(1, "Reference")
        converter = reference_convertor()
        self.assertEqual(converter.Convert(ref_obj), {"id": 1, "name": "Reference"})
        self.assertRaises(ValueError, converter.Convert, "not_a_reference")

if __name__ == '__main__':
    unittest.main()