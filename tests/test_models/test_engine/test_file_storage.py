#!/usr/bin/python3
"""Tests for the FileStorage class"""


import importlib
import json
import models.engine.file_storage
import os
import os.path
import unittest


FileStorage = models.engine.file_storage.FileStorage


class TestStorage (unittest.TestCase):
    """Tests for the FileStorage class"""

    class TestModel:
        """Dummy data model"""

        def __init__(self, includeClass=True):
            """Initialize dummy instance, optionally omitting __class__"""

            self.__includeClass = includeClass

        def to_dict(self):
            """Return this instance dictionary"""
            
            ret = dict(self.__dict__)
            if self.__includeClass:
                ret['__class__'] = 'TestModel'
            return ret

    def setUp(self):
        """Remove the JSON file before each test"""

        if os.path.exists('storage.json'):
            os.remove('storage.json')
        importlib.reload(models.engine.file_storage)

    def test_corruptFile(self):
        """Test failures when JSON file is incorrect"""
        contents = {
            'BaseModel.123': {
                '__class__': 'BaseModel',
                'created_at': '2019-06-27T15:55:30.0',
                'id': '123',
                'updated_at': '2019-07-27T15:56:30.0'
            },
            'wrong': ['stuff in', 'a', 'list']
        }
        storage = FileStorage()
        with self.subTest(msg='dictionary contains non instances'):
            with open('storage.json', 'wt') as file:
                json.dump(contents, file)
            storage.reload()
            self.assertEqual(storage.all(), contents)
        with self.subTest(msg='non json contents'):
            contents = 'this is a string, not json'
            with open('storage.json', 'wt') as file:
                file.write(contents)
            self.assertRaises(ValueError, storage.reload)
        with self.subTest(msg='empty file'):
            with open('storage.json', 'wt') as file:
                pass
            self.assertRaises(ValueError, storage.reload)

    def test_load(self):
        """Test loading the objects from the file"""

        storage = FileStorage()
        with self.subTest(msg='non-existent file ignored'):
            storage.reload()
            self.assertEqual(storage.all(), {})
        with self.subTest(msg='load one object'):
            contents = {
                'BaseModel.123': {
                    '__class__': 'BaseModel',
                    'created_at': '2019-06-27T15:55:30.0',
                    'id': '123',
                    'updated_at': '2019-07-27T15:56:30.0'
                }
            }
            with open('storage.json', 'wt') as file:
                json.dump(contents, file)
            storage.reload()
            name = 'BaseModel.123'
            self.assertEqual(storage.all()[name], contents[name])
        with self.subTest(msg='load multiple objects'):
            contents['OtherData.456'] = {
                '__class__': 'NotAClass',
                'other': 25,
                'crazy': 'in the membrane'
            }
            with open('storage.json', 'wt') as file:
                json.dump(contents, file)
            storage.reload()
            name = 'BaseModel.123'
            self.assertEqual(storage.all()[name], contents[name])
            name = 'OtherData.456'
            self.assertEqual(storage.all()[name], contents[name])

    def test_save(self):
        """Test saving objects to the file"""

        storage = FileStorage()
        storage.reload()
        with self.subTest(msg='save empty dictionary'):
            storage.save()
            with open('storage.json', 'rt') as file:
                self.assertEqual(file.read(), '{}')
        with self.subTest(msg='save one instance'):
            obj = TestStorage.TestModel()
            obj.id = '1000000'
            obj.attr1 = 5
            obj.name = 'object'
            storage.new(obj)
            storage.save()
            contents = {'TestModel.1000000': obj.to_dict()}
            with open('storage.json', 'rt') as file:
                self.assertEqual(json.load(file), contents)
        with self.subTest(msg='save multiple instances'):
            obj = TestStorage.TestModel()
            obj.id = '123'
            obj.thing = 'the'
            obj.age = 50
            storage.new(obj)
            storage.save()
            contents['TestModel.123'] = obj.to_dict()
            with open('storage.json', 'rt') as file:
                self.assertEqual(json.load(file), contents)

    def test_saveBadObject(self):
        """Trying to save objects that aren't valid data models"""

        storage = FileStorage()
        with self.subTest(msg='no to_dict method'):
            self.assertRaises(AttributeError, storage.new, 'not data')
        with self.subTest(msg='mandatory attributes invalid'):
            obj = TestStorage.TestModel(False)
            self.assertRaises(KeyError, storage.new, obj)
            obj = TestStorage.TestModel(True)
            self.assertRaises(KeyError, storage.new, obj)
            obj.id = '123'
            obj = TestStorage.TestModel(False)
            obj.id = '123'
            self.assertRaises(KeyError, storage.new, obj)
            obj = TestStorage.TestModel(True)
            obj.id = 123
            self.assertRaises(TypeError, storage.new, obj)
