#!/usr/bin/python3
"""Tests for the amenity data model"""


from models.amenity import Amenity
from tests.test_models.test_base_model import TestBase


class TestAmenity (TestBase):
    """Tests for the amenity data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = Amenity
        self._name = 'Amenity'
