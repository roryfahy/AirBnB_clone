#!/usr/bin/python3
"""Tests for the BaseModel class"""


import datetime
from itertools import chain
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import os
import os.path
from time import sleep
import unittest
import uuid


class TestBase (unittest.TestCase):
    """Tests for the BaseModel class"""

    def __init__(self, *args, **kwargs):
        """Set up which data model to test"""

        super().__init__(*args, **kwargs)
        self._cls = BaseModel
        self._name = 'BaseModel'

    @classmethod
    def tearDownClass(self):
        """Remove the JSON file after each test case"""

        if os.path.exists('storage.json'):
            os.remove('storage.json')

    def test_creationTime(self):
        """Test that the creation time stamp is set properly"""

        b = self._cls()
        now = datetime.datetime.now()
        self.assertIsInstance(b.created_at, datetime.datetime)
        self.assertTrue(0 <= (now - b.created_at).total_seconds() < 1)

    def test_id(self):
        """Test that the base model UUID is created properly"""

        b = self._cls()
        with self.subTest(msg='id is a UUID'):
            self.assertIsInstance(b.id, str)
            self.assertIsInstance(uuid.UUID(b.id), uuid.UUID)
        with self.subTest(msg='IDs are unique'):
            self.assertNotEqual(self._cls().id, self._cls().id)

    def test_persistence(self):
        """Test saving and loading data models to storage"""

        if os.path.exists('storage.json'):
            os.remove('storage.json')
        storage = FileStorage()
        storage.reload()
        with self.subTest(msg='new models added to storage'):
            obj = self._cls()
            self.assertTrue(self._name + '.' + obj.id in storage.all())
        with self.subTest(msg='instances can be saved and loaded'):
            obj.save()
            old = obj.to_dict()
            del obj, storage
            storage = FileStorage()
            storage.reload()
            self.assertEqual(storage.get(self._cls, old['id']).to_dict(), old)

    def test_toDictionary(self):
        """Test converting to a dictionary using to_dict"""

        b = self._cls()
        d = b.to_dict()
        with self.subTest(msg='contains all attributes'):
            s1 = set(d.keys())
            s2 = set(b.__dict__.keys())
            self.assertTrue(s2.issubset(s1))
        with self.subTest(msg='class name key added'):
            self.assertTrue('__class__' in d.keys())
            self.assertEqual(d['__class__'], self._name)
        with self.subTest(msg='datetimes converted to str'):
            self.assertIsInstance(d['created_at'], str)
            self.assertIsInstance(d['updated_at'], str)
            self.assertEqual(d['created_at'], b.created_at.isoformat())
            self.assertEqual(d['updated_at'], b.updated_at.isoformat())

    def test_toString(self):
        """Test converting to a string with __str__"""

        b = self._cls()
        good = '[' + self._name + '] ({}) {}'.format(b.id, str(b.__dict__))
        self.assertEqual(str(b), good)

    def test_updateTime(self):
        """Test that the update time is set and updated properly"""

        b = self._cls()
        with self.subTest(msg='time set when object created'):
            now = datetime.datetime.now()
            self.assertIsInstance(b.updated_at, datetime.datetime)
            self.assertTrue(0 <= (now - b.updated_at).total_seconds() < 1)
        with self.subTest(msg='time updated when instance saved'):
            old = b.updated_at
            sleep(.001)
            b.save()
            now = datetime.datetime.now()
            self.assertTrue(old < b.updated_at < now)

    def test_fromDict(self):
        """Test that instances can be created from a given dictionary"""

        d = self._cls().to_dict()
        b = self._cls(**d)
        with self.subTest(msg='check for \'__class__\' in new instance'):
            self.assertNotIsInstance(b.__class__, str)
        del d['__class__']
        with self.subTest(msg='check all/proper attributes are passed'):
            for key in d.keys():
                self.assertTrue(hasattr(b, key))
        d['created_at'] = datetime.datetime.strptime(
            d['created_at'],
            '%Y-%m-%dT%H:%M:%S.%f'
        )
        d['updated_at'] = datetime.datetime.strptime(
            d['updated_at'],
            '%Y-%m-%dT%H:%M:%S.%f'
        )
        with self.subTest(msg='check if correct values are set in new inst'):
            for key, value in d.items():
                self.assertEqual(value, getattr(b, key))
        with self.subTest(msg='check if positional args are ignored'):
            d = self._cls().to_dict()
            c = self._cls('dfsa', 'sfsd', **d)
            e = self._cls('dfsa', 'sfsd')
            for value in chain(c.__dict__.values(), e.__dict__.values()):
                self.assertNotEqual('dfsa', value)
                self.assertNotEqual('sfsd', value)
        with self.subTest(msg='unknown attributes can be added'):
            d['test'] = 5
            b = self._cls(**d)
            self.assertEqual(b.test, 5)
