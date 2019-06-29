#!/usr/bin/python3
"""Tests for the place data model"""


from models.place import Place
from tests.test_models.test_base_model import TestBase


class TestPlace (TestBase):
    """Tests for the place data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = Place
        self._name = 'Place'
