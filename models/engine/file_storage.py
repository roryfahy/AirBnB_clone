#!/usr/bin/python3
"""module for FileStorage class"""

import os.path
import json


class FileStorage:
    """class used to store and retrieve data model instances using JSON"""

    __file_path = "storage.json"
    __objects = {}
    
    def all(self):
        """return __objects dictionary"""
        return FileStorage.__objects

    def new(self, obj):
        """add dictionary rep of obj to dictionary __objects"""
        value = obj.to_dict()
        key = value['__class__'] + '.' + value['id']
        FileStorage.__objects[key] = value

    def reload(self):
        """retreive repr of objects from JSON file and store in __objects"""
        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, 'rt') as file:
            FileStorage.__objects = json.load(file)

    def save(self):
        """save the instances to the storage file"""

        with open(FileStorage.__file_path, 'wt') as file:
            json.dump(FileStorage.__objects, file)
