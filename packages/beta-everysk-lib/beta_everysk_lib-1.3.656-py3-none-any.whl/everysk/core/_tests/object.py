###############################################################################
#
# (C) Copyright 2023 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
# pylint: disable=protected-access, attribute-defined-outside-init
from copy import copy, deepcopy
from typing import Any
from unittest import TestCase
from everysk.core.datetime import DateTime, Date
from everysk.core.exceptions import DefaultError, FieldValueError, RequiredError
from everysk.core.fields import BoolField
from everysk.core.object import BaseField, BaseDict, BaseObject, _required, _validate, MetaClass


class RequiredTestCase(TestCase):

    def test_required(self):
        self.assertRaises(RequiredError, _required, attr_name='Test', value=None)
        self.assertRaises(RequiredError, _required, attr_name='Test', value='')
        self.assertRaises(RequiredError, _required, attr_name='Test', value=())
        self.assertRaises(RequiredError, _required, attr_name='Test', value=[])
        self.assertRaises(RequiredError, _required, attr_name='Test', value={})


class ValidateTestCase(TestCase):

    def test_none(self):
        _validate(attr_name='test', value=None, attr_type=Date)
        _validate(attr_name='test', value=None, attr_type=DateTime)
        _validate(attr_name='test', value=None, attr_type=dict)
        _validate(attr_name='test', value=None, attr_type=float)
        _validate(attr_name='test', value=None, attr_type=int)
        _validate(attr_name='test', value=None, attr_type=list)
        _validate(attr_name='test', value=None, attr_type=str)

    def test_date(self):
        _validate(attr_name='test', value=Date.today(), attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=Date)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=Date)

    def test_datetime(self):
        _validate(attr_name='test', value=DateTime.now(), attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=DateTime)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=DateTime)

    def test_dict(self):
        _validate(attr_name='test', value={}, attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=dict)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=dict)

    def test_float(self):
        _validate(attr_name='test', value=1.0, attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=float)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=float)

    def test_int(self):
        _validate(attr_name='test', value=1, attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=int)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=int)

    def test_list(self):
        _validate(attr_name='test', value=[], attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value='1', attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=list)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=list)

    def test_str(self):
        _validate(attr_name='test', value='1', attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=DateTime.now(), attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=Date.today(), attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1, attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=1.0, attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value=[], attr_type=str)
        self.assertRaises(FieldValueError, _validate, attr_name='test', value={}, attr_type=str)

    def test_any(self):
        _validate(attr_name='test', value=None, attr_type=Any)
        _validate(attr_name='test', value={}, attr_type=Any)
        _validate(attr_name='test', value=[], attr_type=Any)
        _validate(attr_name='test', value=123, attr_type=Any)
        _validate(attr_name='test', value='123', attr_type=Any)
        _validate(attr_name='test', value=callable, attr_type=Any)

    def test_callable(self):
        _validate(attr_name='test', value=lambda x: x, attr_type=callable)
        with self.assertRaisesRegex(FieldValueError, 'Key test must be <built-in function callable>.'):
            _validate(attr_name='test', value=None, attr_type=callable)


class BaseFieldTestCase(TestCase):

    def test_init(self):
        field = BaseField(attr_type=str, default='default', required=True, readonly=True, other='Test')
        self.assertEqual(field.attr_type, str)
        self.assertEqual(field.default, 'default')
        self.assertTrue(field.required)
        self.assertTrue(field.readonly)
        self.assertEqual(field.other, 'Test') # pylint: disable=no-member

    def test_init_default_empty(self):
        self.assertRaises(DefaultError, BaseField, attr_type=str, default=[])
        self.assertRaises(DefaultError, BaseField, attr_type=str, default={})

    def test_init_default_not_empty(self):
        BaseField(attr_type=str, default=[1, 2, 3])
        BaseField(attr_type=str, default={'a': 1, 'b': 2})

    def test_init_readonly_default(self):
        self.assertRaises(RequiredError, BaseField, attr_type=str, readonly=True)

    def test_clean(self):
        field = BaseField(attr_type=str)
        self.assertEqual(field.clean_value('Test'), 'Test')

    def test_transform_to_none(self):
        field = BaseField(attr_type=str, empty_is_none=False)
        self.assertEqual(field.transform_to_none(''), '')
        field = BaseField(attr_type=str, empty_is_none=True)
        self.assertEqual(field.transform_to_none(''), None)

    def test_validate_attr_type(self):
        field = BaseField(attr_type=str)
        self.assertRaises(FieldValueError, field.validate, attr_name='test', value=True)
        self.assertRaises(FieldValueError, field.validate, attr_name='test', value='1', attr_type=int)

    def test_validate_readonly(self):
        field = BaseField(attr_type=str, readonly=True, default='Teste')
        self.assertRaises(FieldValueError, field.validate, attr_name='test', value='new')

    def test_validate_required(self):
        field = BaseField(attr_type=str, required=True)
        self.assertRaises(RequiredError, field.validate, attr_name='test', value=None)

    def test_validate_required_lazy(self):
        field = BaseField(attr_type=str, required=False, required_lazy=True)
        field.validate(attr_name='test', value=None)

    def test_repr(self):
        field = BaseField(attr_type=str)
        self.assertEqual(repr(field), 'BaseField')

    def test_get_value(self):
        def func():
            return 'Test'
        field = BaseField(attr_type=callable)
        self.assertEqual(field.get_value(func), 'Test')

    def test_required_and_required_lazy_error(self):
        self.assertRaisesRegex(
            FieldValueError,
            "Required and required_lazy can't be booth True.",
            BaseField,
            attr_type=str,
            required=True,
            required_lazy=True
        )

    def test_equal(self):
        self.assertEqual(
            BaseField(attr_type=str, default='field'),
            BaseField(attr_type=str, default='field')
        )

    def test_not_equal(self):
        self.assertNotEqual(
            BaseField(attr_type=str, default='field1'),
            BaseField(attr_type=str, default='field2')
        )

    def test_getattr_method(self):
        field = BaseField(attr_type=str)
        self.assertTrue(hasattr(field, 'startswith'))
        # int.real
        self.assertFalse(hasattr(field, 'real'))


## Fake class for BaseObject tests.
class BaseObjectTestClass(BaseObject):
    attr: int = None

class BaseObjectFieldsTestClass(BaseObject):
    _private: str = 'Private'
    normal_attr = 'Normal'
    field1 = BaseField(attr_type=int)
    field_default = BaseField(attr_type=int, default=100)
    field_readonly = BaseField(attr_type=str, default='default_value', readonly=True)

class BaseObjectAttributeInheritanceTestClass(BaseObjectFieldsTestClass):
    local_attr = BaseField(attr_type=str, default='Local Field')

class BaseObjectInheritanceTestClass(BaseObjectTestClass):
    attr_other: str = None

class BaseObjectRequiredTestClass(BaseObject):
    required = BaseField(attr_type=int, required=True)
    required1 = BaseField(attr_type=int, required=True)

class BaseObjectRequiredInheritanceTestClass(BaseObjectRequiredTestClass):
    required1 = 1

class BaseObjectRequiredLazyTestClass(BaseObject):
    required = BaseField(attr_type=int, required_lazy=True)
    required1 = BaseField(attr_type=int, required_lazy=True)

class BaseObjectRequiredLazyInheritanceTestClass(BaseObjectRequiredLazyTestClass):
    required1 = 1

class BaseObjectAttributeReplace(BaseObject):
    is_parent = BaseField(attr_type=bool, default=True)

class BaseObjectAttributeReplaceChild(BaseObjectAttributeReplace):
    is_parent = False

class BaseFieldClean(BaseField):

    def clean_value(self, value: Any) -> Any:
        if value not in (None, int):
            raise FieldValueError('Error')

class BaseObjectCleanValueError(BaseObject):
    field1 = BaseFieldClean(attr_type=int)

class BaseObjectTestCase(TestCase):

    def test_init(self):
        obj = BaseObjectTestClass()
        self.assertIsNone(obj.attr)

    def test_attr_creation(self):
        obj = BaseObjectTestClass()
        obj.attr = 1
        self.assertEqual(obj.attr, 1)

    def test_fields(self):
        obj = BaseObjectFieldsTestClass()
        self.assertEqual(obj._private, 'Private')
        self.assertEqual(obj.normal_attr, 'Normal')
        self.assertIsNone(obj.field1)
        self.assertEqual(obj.field_default, 100)
        self.assertEqual(obj.field_readonly, 'default_value')
        self.assertRaises(FieldValueError, BaseObjectFieldsTestClass, field_readonly='Changed')
        with self.assertRaisesRegex(FieldValueError, "The field 'field_readonly' value cannot be changed."):
            obj.field_readonly = 'Changed'

    def test_required(self):
        self.assertRaises(RequiredError, BaseObjectRequiredTestClass)

    def test_required_inheritance(self):
        self.assertRaisesRegex(RequiredError, 'The required attribute is required.', BaseObjectRequiredInheritanceTestClass)
        obj = BaseObjectRequiredInheritanceTestClass(required=2)
        self.assertEqual(obj.required, 2)
        self.assertEqual(obj.required1, 1)

    def test_required_lazy(self):
        obj = BaseObjectRequiredLazyTestClass()
        self.assertRaisesRegex(
            RequiredError,
            'The required attribute is required.',
            obj.validate_required_fields
        )

    def test_required_lazy_inheritance(self):
        obj = BaseObjectRequiredLazyInheritanceTestClass()
        self.assertRaisesRegex(
            RequiredError,
            'The required attribute is required.',
            obj.validate_required_fields
        )
        obj.required = 2
        obj.validate_required_fields()
        self.assertEqual(obj.required, 2)
        self.assertEqual(obj.required1, 1)

    def test_default_receive_none(self):
        obj = BaseObjectFieldsTestClass(field_default=None)
        self.assertEqual(obj.field_default, None)

    def test_attribute_change_bool_type(self):
        parent = BaseObjectAttributeReplace()
        self.assertTrue(parent.is_parent)
        child = BaseObjectAttributeReplaceChild()
        self.assertFalse(child.is_parent)

    def test_get_attribute_class(self):
        self.assertEqual(BaseObjectFieldsTestClass.field_default, 100)

    def test_get_attribute_inheritance_class(self):
        self.assertEqual(BaseObjectAttributeInheritanceTestClass.local_attr, 'Local Field')
        self.assertEqual(BaseObjectAttributeInheritanceTestClass.field_readonly, 'default_value')

    def test_get_attribute_class_error(self):
        with self.assertRaisesRegex(AttributeError, "type object 'BaseObjectFieldsTestClass' has no attribute 'field_default_erro'"):
            BaseObjectFieldsTestClass.field_default_erro # pylint: disable=pointless-statement

    def test_get_clean_value(self):
        obj = BaseObjectFieldsTestClass()
        self.assertIsNone(obj.field1)
        obj.field1 = 21
        self.assertEqual(obj.field1, 21)

    def test_get_clean_value_error(self):
        with self.assertRaisesRegex(FieldValueError, 'field1: Error'):
            BaseObjectCleanValueError(field1='21')

    def test_del_attribute(self):
        obj = BaseObject(attr1=1)
        self.assertEqual(obj.attr1, 1)
        del obj.attr1
        with self.assertRaisesRegex(AttributeError, "'BaseObject' object has no attribute 'attr1'"):
            obj.attr1 # pylint: disable=pointless-statement

    def test_del_private_attribute(self):
        obj = BaseObject(_attr1=1)
        self.assertEqual(obj._attr1, 1)
        del obj._attr1
        with self.assertRaisesRegex(AttributeError, "'BaseObject' object has no attribute '_attr1'"):
            obj._attr1 # pylint: disable=pointless-statement

    def test_copy(self):
        obj1 = BaseObject(_private=1, public=2)
        obj2 = copy(obj1)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertEqual(obj1.public, obj2.public)

    def test_copy_config(self):
        obj1 = BaseObject(config='Banana')
        obj2 = copy(obj1)
        self.assertEqual(obj1.config, 'Banana')
        with self.assertRaisesRegex(AttributeError, "'BaseObject' object has no attribute 'config'"):
            obj2.config # pylint: disable=pointless-statement

    def test_deepcopy(self):
        obj1 = BaseObject(_private=1, public=2)
        obj2 = deepcopy(obj1)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertEqual(obj1.public, obj2.public)

    def test_deepcopy_config(self):
        obj1 = BaseObject(config='Banana')
        obj2 = deepcopy(obj1)
        self.assertEqual(obj1.config, 'Banana')
        with self.assertRaisesRegex(AttributeError, "'BaseObject' object has no attribute 'config'"):
            obj2.config # pylint: disable=pointless-statement

    def test_replace(self):
        obj1 = BaseObject(_private=1, public=2)
        obj2 = obj1.replace(_private=3, public=4)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj2._private, 3)
        self.assertEqual(obj2.public, 4)

    def test_replace_config(self):
        obj1 = BaseObject(config=1)
        obj2 = obj1.replace(public=4)
        with self.assertRaisesRegex(AttributeError, "'BaseObject' object has no attribute 'config'"):
            obj2.config # pylint: disable=pointless-statement


## Fake class for BaseDict tests.
class BaseDictTestClass(BaseDict):
    attr: int = None
    field = BaseField(attr_type=str)

class BaseDictFieldsTestClass(BaseDict):
    _private: str = 'Private'
    normal_attr = 'Normal'
    field1 = BaseField(attr_type=int)
    field_default = BaseField(attr_type=int, default=100)
    field_readonly = BaseField(attr_type=str, default='default_value', readonly=True)

class BaseDictInheritanceTestClass(BaseDictTestClass):
    attr_other: str = None

class BaseDictRequiredTestClass(BaseDict):
    required = BaseField(attr_type=int, required=True)

class BaseDictRequiredLazyTestClass(BaseDict):
    normal: bool = True
    required = BaseField(attr_type=int, required_lazy=True)

class BaseDictBoolTestClass(BaseDict):
    attr = BoolField()

class BaseDictTestCase(TestCase):

    def test_init(self):
        obj = BaseDictTestClass()
        self.assertIsNone(obj.attr)
        self.assertIsNone(obj['field'])

    def test_attr_creation(self):
        obj = BaseDictTestClass()
        obj.attr = 1
        self.assertEqual(obj.attr, 1)
        self.assertEqual(obj['attr'], 1)
        obj['attr2'] = 10
        self.assertEqual(obj.attr2, 10) # pylint: disable=no-member
        self.assertEqual(obj['attr2'], 10)

    def test_fields(self):
        obj = BaseDictFieldsTestClass()
        self.assertEqual(obj._private, 'Private')
        self.assertEqual(obj.normal_attr, 'Normal')
        self.assertIsNone(obj.field1)
        self.assertIsNone(obj['field1'])
        self.assertEqual(obj.field_default, 100)
        self.assertEqual(obj['field_default'], 100)
        self.assertEqual(obj.field_readonly, 'default_value')
        self.assertEqual(obj['field_readonly'], 'default_value')
        self.assertRaises(FieldValueError, BaseDictFieldsTestClass, field_readonly='Changed')
        with self.assertRaisesRegex(FieldValueError, "The field 'field_readonly' value cannot be changed."):
            obj.field_readonly = 'Changed'
        with self.assertRaisesRegex(FieldValueError, "The field 'field_readonly' value cannot be changed."):
            obj['field_readonly'] = 'Changed'

    def test_private_attr(self):
        obj = BaseDictFieldsTestClass()
        self.assertNotIn('_private', obj)
        obj._other = 1
        self.assertNotIn('_other', obj)
        self.assertEqual(obj._other, 1)
        with self.assertRaisesRegex(KeyError, "Keys can't start with '_'"):
            obj['_other'] = 1

    def test_config_key(self):
        obj = BaseDict(config=1)
        with self.assertRaisesRegex(KeyError, 'config'):
            obj['config'] # pylint: disable=pointless-statement

        obj = BaseDict()
        with self.assertRaisesRegex(KeyError, 'The key cannot be called "config".'):
            obj['config'] = 1

    def test_update(self):
        obj = BaseDictTestClass()
        self.assertIsNone(obj.attr)
        self.assertIsNone(obj['field'])
        obj.update({'attr': 1, 'field': 'a', 'attr2': 2})
        self.assertEqual(obj.attr, 1)
        self.assertEqual(obj['attr'], 1)
        self.assertEqual(obj.attr2, 2) # pylint: disable=no-member
        self.assertEqual(obj['attr2'], 2)
        self.assertRaises(FieldValueError, obj.update, {'attr': '1', 'attr2': 2})

    def test_required(self):
        self.assertRaises(RequiredError, BaseDictRequiredTestClass)

    def test_required_lazy(self):
        obj = BaseDictRequiredLazyTestClass()
        self.assertRaisesRegex(
            RequiredError,
            'The required attribute is required.',
            obj.validate_required_fields
        )

    def test_default_receive_none(self):
        obj = BaseDictFieldsTestClass(field_default=None)
        self.assertEqual(obj.field_default, None)
        self.assertEqual(obj['field_default'], None)

    def test_value_persist_on_error(self):
        obj = BaseDictFieldsTestClass()
        try:
            obj['field_readonly'] = 'Changed'
        except FieldValueError:
            pass
        self.assertEqual(obj.field_readonly, 'default_value')
        self.assertEqual(obj['field_readonly'], 'default_value')

    def test_clean_value(self):
        base = BaseDictBoolTestClass(attr=1)
        # check clean value changed to bool True
        self.assertTrue(base.attr is True)
        self.assertTrue(base['attr'] is True)

        base = BaseDictBoolTestClass()
        base.attr = 1
        self.assertTrue(base.attr is True)
        self.assertTrue(base['attr'] is True)

        base = BaseDictBoolTestClass()
        base['attr'] = 1
        self.assertTrue(base.attr is True)
        self.assertTrue(base['attr'] is True)

    def test_del_attribute(self):
        obj = BaseDict(attr1=1)
        self.assertEqual(obj['attr1'], 1)
        self.assertEqual(obj.attr1, 1)
        del obj.attr1
        with self.assertRaisesRegex(KeyError, "'attr1'"):
            obj['attr1'] # pylint: disable=pointless-statement

        with self.assertRaisesRegex(AttributeError, "'BaseDict' object has no attribute 'attr1'"):
            obj.attr1 # pylint: disable=pointless-statement

    def test_del_private_attribute(self):
        obj = BaseDict(_attr1=1)
        # Private attributes don't turn into keys
        with self.assertRaisesRegex(KeyError, "'_attr1'"):
            obj['_attr1'] # pylint: disable=pointless-statement

        self.assertEqual(obj._attr1, 1)
        del obj._attr1
        with self.assertRaisesRegex(KeyError, "'_attr1'"):
            obj['_attr1'] # pylint: disable=pointless-statement

        with self.assertRaisesRegex(AttributeError, "'BaseDict' object has no attribute '_attr1'"):
            obj._attr1 # pylint: disable=pointless-statement

    def test_del_key(self):
        obj = BaseDict(attr1=1)
        self.assertEqual(obj['attr1'], 1)
        self.assertEqual(obj.attr1, 1)
        del obj['attr1']
        with self.assertRaisesRegex(KeyError, "'attr1'"):
            obj['attr1'] # pylint: disable=pointless-statement

        with self.assertRaisesRegex(AttributeError, "'BaseDict' object has no attribute 'attr1'"):
            obj.attr1 # pylint: disable=pointless-statement

    def test_fromkeys(self):
        obj = BaseDict(_private=1, public=2, excluded=3)
        dct = obj.fromkeys(['public', 'new'], 4)
        self.assertEqual(obj._private, dct._private)
        self.assertEqual(obj.public, dct.public)
        self.assertEqual(obj['public'], dct['public'])
        self.assertEqual(dct.new, 4)
        self.assertEqual(dct['new'], 4)

    def test_clear(self):
        obj = BaseDict(_private=1, public=2)
        self.assertDictEqual(obj, {'public': 2})
        self.assertEqual(obj._private, 1)
        self.assertEqual(obj.public, 2)
        obj.clear()
        self.assertDictEqual(obj, {})
        self.assertEqual(obj._private, 1)
        self.assertFalse(hasattr(obj, 'public'))

    def test_self_copy(self):
        obj1 = BaseDict(_private=1, public=2)
        obj2 = obj1.copy()
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)

    def test_copy(self):
        obj1 = BaseDict(_private=1, public=2)
        obj2 = copy(obj1)
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)

    def test_deepcopy(self):
        obj1 = BaseDict(_private=1, public=2)
        obj2 = deepcopy(obj1)
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)

    def test_pop(self):
        obj = BaseDict(_private=1, public=2)
        self.assertEqual(obj.pop('public'), 2)
        self.assertEqual(obj.pop('public', 4), 4)
        with self.assertRaisesRegex(KeyError, 'public'):
            obj.pop('public')

    def test_popitem(self):
        obj = BaseDict(_private=1, public=2)
        self.assertEqual(obj.popitem(), ('public', 2))
        with self.assertRaisesRegex(KeyError, r'popitem\(\)\: dictionary is empty'):
            obj.popitem()

    def test_replace(self):
        obj1 = BaseDict(_private=1, public=2)
        obj2 = obj1.replace(_private=3, public=4)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj2._private, 3)
        self.assertEqual(obj2.public, 4)
        self.assertEqual(obj2['public'], 4)

    def test_replace_config(self):
        obj1 = BaseDict()
        obj1.config = 1
        obj2 = obj1.replace(public=4)
        with self.assertRaisesRegex(AttributeError, "'BaseDict' object has no attribute 'config'"):
            obj2.config # pylint: disable=pointless-statement


class BaseDictProperty(BaseDict):
    _to_date = BaseField(attr_type=str)

    @property
    def to_date(self):
        return self._to_date

    @to_date.setter
    def to_date(self, value):
        self._to_date = value

class BaseDictPropertyInherit(BaseDictProperty):
    pass


class BaseDictPropertyTestCase(TestCase):

    def test_property_setattr_init(self):
        obj = BaseDictProperty(to_date='Test')
        self.assertEqual(obj.to_date, 'Test')
        self.assertEqual(obj._to_date, 'Test')
        self.assertNotIn('to_date', obj)

    def test_property_setattr(self):
        obj = BaseDictProperty()
        obj.to_date = 'Test'
        self.assertEqual(obj.to_date, 'Test')
        self.assertEqual(obj._to_date, 'Test')
        self.assertNotIn('to_date', obj)

    def test_property_setitem(self):
        obj = BaseDictProperty()
        obj['to_date'] = 'Test'
        self.assertEqual(obj.to_date, 'Test')
        self.assertEqual(obj._to_date, 'Test')
        self.assertNotIn('to_date', obj)


class BaseObjectConfig(BaseObject):
    class Config:
        value: int = 1

class BaseDictConfig(BaseDict):
    class Config:
        value: int = 1

    config: Config


class MetaClassConfigTestCase(TestCase):

    def setUp(self) -> None:
        BaseObjectConfig.config.value = 1
        BaseDictConfig.config.value = 1

    def test_object_config_attribute(self):
        self.assertEqual(BaseObjectConfig.config.value, 1)
        obj = BaseObjectConfig()
        self.assertEqual(obj.config.value, BaseObjectConfig.config.value)

    def test_object_config_singleton(self):
        obj = BaseObjectConfig()
        obj.config.value = 3
        self.assertEqual(BaseObjectConfig.config.value, 3)
        self.assertEqual(obj.config.value, BaseObjectConfig.config.value)

    def test_object_config_delete(self):
        obj = BaseObjectConfig()
        with self.assertRaisesRegex(AttributeError, "type object 'BaseObjectConfig' has no attribute 'Config'"):
            BaseObjectConfig.Config # pylint: disable=pointless-statement

        with self.assertRaisesRegex(AttributeError, "'BaseObjectConfig' object has no attribute 'Config'"):
            obj.Config # pylint: disable=pointless-statement

    def test_dict_config_attribute(self):
        self.assertEqual(BaseDictConfig.config.value, 1)
        obj = BaseDictConfig()
        self.assertEqual(obj.config.value, BaseDictConfig.config.value)

    def test_dict_config_singleton(self):
        obj = BaseDictConfig()
        obj.config.value = 3
        self.assertEqual(BaseDictConfig.config.value, 3)
        self.assertEqual(obj.config.value, BaseDictConfig.config.value)

    def test_dict_config_delete(self):
        obj = BaseDictConfig()
        with self.assertRaisesRegex(AttributeError, "type object 'BaseDictConfig' has no attribute 'Config'"):
            BaseDictConfig.Config # pylint: disable=pointless-statement

        with self.assertRaisesRegex(AttributeError, "'BaseDictConfig' object has no attribute 'Config'"):
            obj.Config # pylint: disable=pointless-statement

    def test_dict_config_no_key(self):
        obj = BaseDictConfig()
        with self.assertRaisesRegex(KeyError, 'config'):
            obj['config'] # pylint: disable=pointless-statement

    def test_dict_config_attribute_copy(self):
        obj1 = BaseDictConfig()
        obj1.config = copy(obj1.config)
        obj1.config.value = 2
        obj2 = BaseDictConfig()
        obj3 = BaseDictConfig(**obj1)
        self.assertNotEqual(obj1.config, obj2.config)
        self.assertNotEqual(obj1.config, obj3.config)
        self.assertEqual(obj1.config.value, 2)
        self.assertEqual(obj2.config.value, 1)
        self.assertEqual(obj3.config.value, 1)


class FrozenObject(BaseObject):
    class Config:
        frozen: bool = True


class FrozenObjectTestCase(TestCase):

    def setUp(self) -> None:
        self.message = 'Class everysk.core._tests.object.FrozenObject is frozen and cannot be modified.'

    def test_create(self):
        obj = FrozenObject(attr=1, attr2='Banana')
        self.assertEqual(obj.attr, 1)
        self.assertEqual(obj.attr2, 'Banana')

    def test_delete(self):
        obj = FrozenObject(attr=1)
        with self.assertRaisesRegex(AttributeError, self.message):
            del obj.attr

    def test_create_new_attribute(self):
        obj = FrozenObject(attr=1)
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.attr2 = 2

    def test_create_update_attribute(self):
        obj = FrozenObject(attr=1)
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.attr = 2

    def test_copy(self):
        obj1 = FrozenObject(_private=1, public=2)
        obj2 = copy(obj1)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertEqual(obj1.public, obj2.public)
        self.assertTrue(obj1._is_frozen)
        self.assertTrue(obj2._is_frozen)

    def test_deepcopy(self):
        obj1 = FrozenObject(_private=1, public=2)
        obj2 = deepcopy(obj1)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertEqual(obj1.public, obj2.public)
        self.assertTrue(obj1._is_frozen)
        self.assertTrue(obj2._is_frozen)

    def test_replace(self):
        obj1 = FrozenObject(_private=1, public=2)
        obj2 = obj1.replace(_private=3, public=4)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj2._private, 3)
        self.assertEqual(obj2.public, 4)
        self.assertTrue(obj2._is_frozen)


class FrozenDict(BaseDict):
    class Config:
        frozen: bool = True


class FrozenDictTestCase(TestCase):
    def setUp(self) -> None:
        self.message = 'Class everysk.core._tests.object.FrozenDict is frozen and cannot be modified.'

    def test_create(self):
        obj = FrozenDict(attr=1, attr2='Banana')
        self.assertEqual(obj.attr, 1)
        self.assertEqual(obj.attr2, 'Banana')
        self.assertEqual(obj['attr'], 1)
        self.assertEqual(obj['attr2'], 'Banana')

    def test_delete(self):
        obj = FrozenDict(attr=1, attr2='Banana')
        with self.assertRaisesRegex(AttributeError, self.message):
            del obj.attr

        with self.assertRaisesRegex(AttributeError, self.message):
            del obj['attr2']

    def test_create_new_attribute(self):
        obj = FrozenDict()
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.attr = 2

        with self.assertRaisesRegex(AttributeError, self.message):
            obj['attr'] = 2

    def test_create_update_attribute(self):
        obj = FrozenDict(attr=1, attr2='Banana')
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.attr = 2

        with self.assertRaisesRegex(AttributeError, self.message):
            obj['attr'] = 2

    def test_clear(self):
        obj = FrozenDict(attr=1, attr2='Banana')
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.clear()

    def test_self_copy(self):
        obj1 = FrozenDict(_private=1, public=2)
        obj2 = obj1.copy()
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertTrue(obj2.__dict__['_is_frozen'])
        self.assertTrue(obj1._is_frozen)
        self.assertTrue(obj2._is_frozen)

    def test_copy(self):
        obj1 = FrozenDict(_private=1, public=2)
        obj2 = copy(obj1)
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertTrue(obj2.__dict__['_is_frozen'])
        self.assertTrue(obj1._is_frozen)
        self.assertTrue(obj2._is_frozen)

    def test_deepcopy(self):
        obj1 = FrozenDict(_private=1, public=2)
        obj2 = deepcopy(obj1)
        self.assertDictEqual(obj1, obj2)
        self.assertEqual(obj1._private, obj2._private)
        self.assertTrue(obj2.__dict__['_is_frozen'])
        self.assertTrue(obj1._is_frozen)
        self.assertTrue(obj2._is_frozen)

    def test_pop(self):
        obj = FrozenDict(_private=1, public=2)
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.pop('public')

    def test_popitem(self):
        obj = FrozenDict(_private=1, public=2)
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.popitem()

    def test_update(self):
        obj = FrozenDict(_private=1, public=2)
        with self.assertRaisesRegex(AttributeError, self.message):
            obj.update({'attr': 1})

    def test_replace(self):
        obj1 = FrozenDict(_private=1, public=2)
        obj2 = obj1.replace(_private=3, public=4)
        self.assertNotEqual(obj1, obj2)
        self.assertEqual(obj2._private, 3)
        self.assertEqual(obj2.public, 4)
        self.assertEqual(obj2['public'], 4)
        self.assertTrue(obj2._is_frozen)


class FakeBaseObject(BaseObject):
    class Config(BaseObject):
        f1: str = 'FakeBaseObject'
        f2 =  BaseField(attr_type=str, default='FakeBaseObject')

class FakeBaseDict(BaseDict):
    class Config(BaseObject):
        f1: str = 'FakeBaseDict'
        f2 = BaseField(attr_type=str, default='FakeBaseDict')

class Fake01PythonClass:
    class Config:
        pass

class Fake02PythonClass:
    class Config:
        pass

class ConfigHashTestCase(TestCase):
    # https://everysk.atlassian.net/browse/COD-2746

    def test_different_values(self):
        self.assertEqual(FakeBaseObject.config.f1, 'FakeBaseObject')
        self.assertEqual(FakeBaseObject.config.f2, 'FakeBaseObject')
        self.assertEqual(FakeBaseDict.config.f1, 'FakeBaseDict')
        self.assertEqual(FakeBaseDict.config.f2, 'FakeBaseDict')

    def test_python_qualname(self):
        self.assertEqual(Fake01PythonClass.Config.__name__, 'Config')
        self.assertEqual(Fake01PythonClass.Config.__qualname__, 'Fake01PythonClass.Config')
        self.assertEqual(Fake02PythonClass.Config.__name__, 'Config')
        self.assertEqual(Fake02PythonClass.Config.__qualname__, 'Fake02PythonClass.Config')


class MetaClassParent(BaseObject):
    p01 = BaseField(attr_type=str, default='Parent field')
    p02: str = '1'
    p03 = 1
    p04: float

    @property
    def prop(self):
        return self.p01

    @prop.setter
    def prop(self, value: str) -> None:
        self.p01 = value

    def func(self):
        pass


class MetaClassChild(MetaClassParent):
    p01 = BaseField(attr_type=str, default='Child field')
    c02: str = '1'
    c03 = 1
    c04: float


class MetaClassAttributesTestCase(TestCase):

    def test_class_attributes(self):
        attrs = getattr(MetaClassParent, MetaClass._attr_name)
        self.assertDictEqual(
            attrs,
            {
                '_is_frozen': bool,
                'p01': BaseField(attr_type=str, default='Parent field'),
                'p02': str,
                'p03': int,
                'p04': float
            }
        )

    def test_class_annotations(self):
        self.assertDictEqual(
            MetaClassParent.__annotations__,
            {
                'p01': str,
                'p02': str,
                'p03': int,
                'p04': float
            }
        )

    def test_class_inheritance_attributes(self):
        attrs = getattr(MetaClassChild, MetaClass._attr_name)
        self.assertDictEqual(
            attrs,
            {
                '_is_frozen': bool,
                'p01': BaseField(attr_type=str, default='Child field'),
                'p02': str,
                'p03': int,
                'p04': float,
                'c02': str,
                'c03': int,
                'c04': float
            }
        )

    def test_class_inheritance_annotations(self):
        self.assertDictEqual(
            MetaClassChild.__annotations__,
            {
                'p01': str,
                'c02': str,
                'c03': int,
                'c04': float
            }
        )

    def test_class_inheritance_default_value(self):
        self.assertEqual(MetaClassChild.p01, 'Child field')
        self.assertEqual(MetaClassChild.p02, '1')
        self.assertEqual(MetaClassChild.p03, 1)
        self.assertIsNone(MetaClassChild.p04)
        self.assertIsNone(MetaClassChild().func())

    def test_class_inheritance_changed_value(self):
        old_parent_p02 = MetaClassParent.p02
        old_child_p02 = MetaClassChild.p02
        MetaClassParent.p02 = 'First'
        self.assertEqual(MetaClassParent.p02, 'First')
        self.assertEqual(MetaClassChild.p02, 'First')
        MetaClassChild.p02 = 'Second'
        self.assertEqual(MetaClassParent.p02, 'First')
        self.assertEqual(MetaClassChild.p02, 'Second')
        MetaClassParent.p02 = old_parent_p02
        MetaClassChild.p02 = old_child_p02

    def test_obj_attributes(self):
        obj = MetaClassParent()
        attrs = getattr(obj, MetaClass._attr_name)
        self.assertDictEqual(
            attrs,
            {
                '_is_frozen': bool,
                'p01': BaseField(attr_type=str, default='Parent field'),
                'p02': str,
                'p03': int,
                'p04': float
            }
        )

    def test_obj_annotations(self):
        obj = MetaClassParent()
        self.assertDictEqual(
            obj.__annotations__,
            {
                'p01': str,
                'p02': str,
                'p03': int,
                'p04': float
            }
        )

    def test_obj_inheritance_attributes(self):
        obj = MetaClassChild()
        attrs = getattr(obj, MetaClass._attr_name)
        self.assertDictEqual(
            attrs,
            {
                '_is_frozen': bool,
                'p01': BaseField(attr_type=str, default='Child field'),
                'p02': str,
                'p03': int,
                'p04': float,
                'c02': str,
                'c03': int,
                'c04': float
            }
        )

    def test_obj_inheritance_annotations(self):
        obj = MetaClassChild()
        self.assertDictEqual(
            obj.__annotations__,
            {
                'p01': str,
                'c02': str,
                'c03': int,
                'c04': float
            }
        )

    def test_obj_inheritance_default_value(self):
        obj = MetaClassChild()
        self.assertEqual(obj.p01, 'Child field')
        self.assertEqual(obj.p02, '1')
        self.assertEqual(obj.p03, 1)
        self.assertIsNone(obj.p04)

    def test_obj_inheritance_changed_value(self):
        parent = MetaClassParent()
        child = MetaClassChild()
        parent.p02 = 'First'
        self.assertEqual(parent.p02, 'First')
        self.assertEqual(child.p02, '1')
        child.p02 = 'Second'
        self.assertEqual(parent.p02, 'First')
        self.assertEqual(child.p02, 'Second')

    def test_property_value(self):
        # https://everysk.atlassian.net/browse/COD-3457
        obj = MetaClassParent(p01='01')
        self.assertEqual(obj.p01, '01')
        self.assertEqual(obj.prop, '01')

        obj = MetaClassParent(prop='02')
        self.assertEqual(obj.p01, '02')
        self.assertEqual(obj.prop, '02')
