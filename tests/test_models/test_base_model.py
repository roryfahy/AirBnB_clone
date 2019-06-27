#!/usr/bin/python3
"""Tests for the BaseModel class"""


import datetime
from models import BaseModel
import unittest
import uuid


class TestBase (unittest.TestCase):
    """Tests for the BaseModel class"""

    def test_creationTime(self):
        """Test that the creation time stamp is set properly"""

        b = BaseModel()
        now = datetime.datetime.now()
        self.assertIsInstance(b.created_at, datetime.datetime)
        self.assertTrue(0 < (now - b.created_at).total_seconds() < 1)

    def test_id(self):
        """Test that the base model UUID is created properly"""

        b = BaseModel()
        self.assertIsInstance(b.id, str)
        self.assertIsInstance(uuid.UUID(b.id), uuid.UUID)

    def test_toDictionary(self):
        """Test converting to a dictionary using to_dict"""

        b = BaseModel()
        d = b.to_dict()
        with self.subTest(msg='contains all attributes'):
            s1 = set(d.keys())
            s2 = set(b.__dict__.keys())
            self.assertTrue(s2.issubset(s1))
        with self.subTest(msg='class name key added'):
            self.assertTrue('__class__' in d.keys())
            self.assertEqual(d['__class__'], 'BaseModel')
        with self.subTest(msg='datetimes converted to str'):
            self.assertIsInstance(d['created_at'], str)
            self.assertIsInstance(d['updated_at'], str)
            self.assertEqual(d['created_at'], b.created_at.isoformat())
            self.assertEqual(d['updated_at'], b.updated_at.isoformat())

    def test_toString(self):
        """Test converting to a string with __str__"""

        b = BaseModel()
        good = '[BaseModel] ({}) {}'.format(b.id, str(b.__dict__))
        self.assertEqual(str(b), good)

    def test_updateTime(self):
        """Test that the update time is set and updated properly"""

        b = BaseModel()
        with self.subTest(msg='time set when object created'):
            now = datetime.datetime.now()
            self.assertIsInstance(b.updated_at, datetime.datetime)
            self.assertTrue(0 < (now - b.updated_at).total_seconds() < 1)
        with self.subTest(msg='time updated when instance saved'):
            old = b.updated_at
            b.save()
            now = datetime.datetime.now()
            self.assertTrue(old < b.updated_at < now)
