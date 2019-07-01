#!/usr/bin/python3
"""Set up a FileStorage singleton shared by data models"""


from models.engine.file_storage import FileStorage
import pkgutil
import importlib


storage = FileStorage()

classes = pkgutil.iter_modules(__path__)
classes = (module[1] for module in classes if not module[2])
classes = ((name.title().replace('_', ''), name) for name in classes)
classes = (
    (cls, importlib.import_module('models.' + mod))
    for cls, mod in classes
)
classes = {cls: getattr(mod, cls) for cls, mod in classes}

storage.reload()
