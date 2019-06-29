#!/usr/bin/python3
"""Tests for the user data model"""


from models.user import User
from tests.test_models.test_base_model import TestBase


class TestUser (TestBase):
    """Tests for the user data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = User
        self._name = 'User'
