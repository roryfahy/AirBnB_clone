#!/usr/bin/python3
"""Set up a FileStorage singleton shared by data models"""


from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
