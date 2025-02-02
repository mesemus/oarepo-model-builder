from unittest.mock import patch

from oarepo_model_builder.api import resolve_includes
from oarepo_model_builder.proxies import current_model_builder
from tests.api.conftest import extra_entrypoints


@patch('pkg_resources.iter_entry_points', extra_entrypoints)
def test_resolve_includes(app):
    assert {'test', 'include1', 'include2', 'include3', 'include4'} == set(current_model_builder.datamodels)

    test_cases = [
        # 1) Check if list type references resolves correctly
        # 1.1) For explicit oarepo:type keyword definition
        ({
             "title": "Test record for 1.1",
             "type": "object",
             "additionalProperties": False,
             "oarepo:type": ["include1"],
             "properties": {
                 "field1": {
                     "oarepo:type": [
                         "include1",
                         "include4"
                     ]
                 }
             }
         }, {
             "title": "Test record for 1.1",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "includedField1": {"type": "string"},
                 "field1": {
                     "type": "object",
                     'title': 'Included properties v1.0.0',
                     "additionalProperties": False,
                     "properties": {
                         "includedField1": {"type": "string"},
                         "includedField2": {"type": "number"}
                     }
                 }
             }
         }),
        # 1.2) For implicit list definition
        ({
             "title": "Test record for 1.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": [
                     'include1',
                     'include4'
                 ]
             }
         }, {
             "title": "Test record for 1.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": {
                     "type": "object",
                     "title": "Included properties v1.0.0",
                     "additionalProperties": False,
                     "properties": {
                         "includedField1": {"type": "string"},
                         "includedField2": {"type": "number"}
                     }
                 }
             }
         }),
        # 2) Check if string type reference is resolved correctly
        # 2.1) For explicit oarepo:type keyword definition
        ({
             "title": "Test record for 2.1",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": {
                     "oarepo:type": "include2"
                 }
             }
         }, {
             "title": "Test record for 2.1",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": {
                     "type": "number"
                 }
             }
         }),
        # 2.2) For implicit property type definition
        ({
             "title": "Test record for 2.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": "include2"
             }
         }, {
             "title": "Test record for 2.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "field1": {
                     "type": "number"
                 }
             }
         }),
        # 3) Check array items type reference resolves correctly
        # 3.1) For string reference
        ({
             "title": "Test record for 3.1",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "arrayField": {
                     "type": "array",
                     "items": "include2"
                 }
             }
         }, {
             "title": "Test record for 3.1",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "arrayField": {
                     "type": "array",
                     "items": {
                         "type": "number"
                     }
                 }
             }
         }),
        # 3.2) For list reference
        ({
             "title": "Test record for 3.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "arrayField": {
                     "type": "array",
                     "items": [
                         "include1",
                         "include4",
                         {
                             "type": "object",
                             "properties": {
                                 "field1": "include2"
                             }
                         }
                     ]
                 }
             }
         }, {
             "title": "Test record for 3.2",
             "type": "object",
             "additionalProperties": False,
             "properties": {
                 "arrayField": {
                     "type": "array",
                     "items": {
                         "type": "object",
                         'title': 'Included properties v1.0.0',
                         "additionalProperties": False,
                         "properties": {
                             "includedField1": {"type": "string"},
                             "includedField2": {"type": "number"},
                             "field1": {"type": "number"}
                         }
                     }
                 }
             }
         })
    ]

    for tc in test_cases:
        src, result = tc

        resolve_includes(src, None)
        assert src == result
