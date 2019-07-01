#!/usr/bin/python3
"""Module for the Storage interface"""


from abc import ABC, abstractmethod


class Storage (ABC):
    """Storage base class enabling persistence of data models"""

    @abstractmethod
    def __contains__(self, obj):
        """Test if the obj exists in storage"""
        pass

    @abstractmethod
    def delete(self, cls, id):
        """Remove a stored data model object, but don't commit this yet"""
        pass

    @abstractmethod
    def get(self, cls, id):
        """Get a data model object given its class or class name and its ID"""
        pass

    @abstractmethod
    def new(self, obj):
        """Add a new data model object to storage, but don't save it yet"""
        pass

    @abstractmethod
    def save(self):
        """Save all stored instances, committing all unsaved changes"""
        pass

    @abstractmethod
    def tryGet(self, cls, id, default):
        """Try to get an object from storage, return default if not found"""
        pass
