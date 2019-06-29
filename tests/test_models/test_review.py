#!/usr/bin/python3
"""Tests for the review data model"""


from models.review import Review
from tests.test_models.test_base_model import TestBase


class TestReview (TestBase):
    """Tests for the review data model"""

    def __init__(self, *args, **kwargs):
        """Set up tests for this particular data model"""

        super().__init__(*args, **kwargs)
        self._cls = Review
        self._name = 'Review'
