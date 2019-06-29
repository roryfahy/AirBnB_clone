#!/usr/bin/python3
"""Tests for the state data model"""


from models.state import State
from tests.test_models.test_base_model import TestBase


class TestState (TestBase):
    """Tests for the state data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = State
        self._name = 'State'
