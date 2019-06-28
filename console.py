#!/usr/bin/python3
"""Module for command interpreter class"""


import cmd
import functools
import models
import pkgutil
import importlib


class HBNBCommand (cmd.Cmd):
    """Interpret commands for a pseudo-API in the AirBnB clone
    
    Attributes:
        print (functools.partial): print with this interpreter's output stream
        
    """

    def __init__(self, *args, **kwargs):
        """create the interpreter with a given data model and save it"""

        super().__init__(*args, **kwargs)
        self.prompt = '(hbnb) '
        self.__classes = self.__getModels()

    def __getModels(self):
        ret = pkgutil.iter_modules(models.__path__)
        ret = (module[1] for module in ret if not module[2])
        ret = ((name.title().replace('_', ''), name) for name in ret)
        ret = ((cls, importlib.import_module('models.' + mod)) for cls, mod in ret)
        ret = {cls: getattr(mod, cls) for cls, mod in ret}
        print(ret)
        return ret
        
    def do_quit(self, empty):
        """The quit command exits the interpreter immediately"""

        return 1

    def do_EOF(self, empty):
        """The interpreter exits when EOF is reached on its input"""

        return 1

if __name__ == '__main__':
    HBNBCommand().cmdloop()
