import data

from meritous.core.properties import *


def property_test_executor(property, assert_type, sample, false_sample):
    p = property()
    assert p.type == assert_type 
    assert p.validate(sample) == True 
    assert p.validate(false_sample) == False
    assert p.is_required == True
    assert p.is_nullable == False
    p = property(default=sample, required=False, nullable=True)
    assert p.default == sample 
    assert p.is_required == False
    assert p.is_nullable == True
    assert p.validate(sample) == True 
    assert p.validate(None) == True
    

property_tests = {
    (TupleProperty, tuple, data.TEST_TUPLE, data.TEST_STR),
    (FloatProperty, float, data.TEST_FLOAT, data.TEST_INT),
    (IntProperty, int, data.TEST_INT, data.TEST_STR),
    (StrProperty, str, data.TEST_STR, data.TEST_INT),
    (BoolProperty, bool, data.TEST_BOOL, data.TEST_INT)
}

def test_property_basics():
    for test_vars in property_tests:
        property_test_executor(*test_vars)
    property_test_executor(ListProperty, list, data.TEST_LIST, data.TEST_TUPLE)
