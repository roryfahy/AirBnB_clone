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
        
    def do_quit(self, empty):
        """The quit command exits the interpreter immediately"""

        return 1

    def do_EOF(self, empty):
        """The interpreter exits when EOF is reached on its input"""

        return 1

if __name__ == '__main__':
    HBNBCommand().cmdloop()
