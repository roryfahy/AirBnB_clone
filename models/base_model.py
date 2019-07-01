#!/usr/bin/python3
"""Module for basemodel"""

import datetime
from models import storage
import uuid


class BaseModel:
    """Base class for data models

    Attributes:
        id (str): a random UUID string unique to each instance
        created_at (datetime.datetime): time stamp when instance was created
        updated_at (datetime.datetime): time stamp when instance was updated

    """

    def __init__(self, *args, **kwargs):
        """Create new instance of BaseModel"""
        if len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = datetime.datetime.now()
            storage.new(self)
        else:
            del(kwargs['__class__'])
            kwargs['created_at'] = datetime.datetime.strptime(
                kwargs['created_at'],
                '%Y-%m-%dT%H:%M:%S.%f'
            )
            kwargs['updated_at'] = datetime.datetime.strptime(
                kwargs['updated_at'],
                '%Y-%m-%dT%H:%M:%S.%f'
            )
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __str__(self):
        """Return the instance's ID, class name, and attributes as a string"""

        return '[{}] ({}) {}'.format(
            type(self).__name__,
            self.id,
            str(self.__dict__)
        )

    def save(self):
        """Update the instance's update time"""

        self.updated_at = datetime.datetime.now()
        storage.get(type(self), self.id).updated_at = self.updated_at
        storage.save()

    def to_dict(self):
        """Return this instance's attributes as a dict

        The returned dict also contains a key called "__class__" containing the
        instance's class name. datetime.datetime objects are converted to
        strings in ISO 8601 format.

        """

        ret = dict(self.__dict__)
        ret['__class__'] = type(self).__name__
        ret['created_at'] = ret['created_at'].isoformat()
        ret['updated_at'] = ret['updated_at'].isoformat()
        return ret
