#!/usr/bin/python3
"""Tests for the city data model"""


from models.city import City
from tests.test_models.test_base_model import TestBase


class TestCity (TestBase):
    """Tests for the city data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = City
        self._name = 'City'
