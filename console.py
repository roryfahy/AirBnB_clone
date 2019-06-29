#!/usr/bin/python3
"""Module for command interpreter class"""


import cmd
import functools
import models
from models.engine.file_storage import FileStorage
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
        self.__print = functools.partial(print, file=self.stdout)
        self.__storage = FileStorage()

    def __getModels(self):
        ret = pkgutil.iter_modules(models.__path__)
        ret = (module[1] for module in ret if not module[2])
        ret = ((name.title().replace('_', ''), name) for name in ret)
        ret = ((cls, importlib.import_module('models.' + mod)) for cls, mod in ret)
        ret = {cls: getattr(mod, cls) for cls, mod in ret}
        return ret

    def do_all(self, line):
        """Print all data model objects, optionally filtered by class"""

        cls = line.partition(' ')[0]
        if cls == '':
            objects = [
                str(self.__classes[k.partition('.')[0]](**v))
                for k, v in self.__storage.all().items()
            ]
        else:
            if cls not in self.__classes:
                self.__print('** class doesn\'t exist **')
                return
            objects = [
                str(self.__classes[cls](**v))
                for k, v in self.__storage.all().items()
                if k.partition('.')[0] == cls
            ]
        self.__print(objects)

    def do_create(self, line):
        """Create a new data model instance and store it"""

        cls = line.partition(' ')[0]
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        self.__storage.new(self.__classes[cls]())
        self.__storage.save()

    def do_destroy(self, line):
        """Destroy an existing data model instance"""

        cls, _, id = line.partition(' ')
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        if id is None:
            self.__print('** instance id missing **')
            return
        key = cls + '.' + id
        if key not in self.__storage.all():
            self.__print('** no instance found **')
            return
        del self.__storage.all()[key]
        self.__storage.save()

    def do_show(self, line):
        """print string representation of an instance"""

        cls, _, id = line.partition(' ')
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        if id == '':
            self.__print('** instance id missing **')
            return
        key = cls + '.' + id
        if key not in self.__storage.all():
            self.__print('** no instance found **')
            return
        print(self.__classes[cls](**self.__storage.all()[key]))

    def do_update(self, line):
        """Update or add an attribute to a data model instance"""

        if line == '':
            self.__print('** class name missing **')
            return
        line = line.split(maxsplit=3)
        if line[0] not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        if len(line) < 2:
            self.__print('** instance id missing **')
            return
        key = line[0] + '.' + line[1]
        if key not in self.__storage.all():
            self.__print('** no instance found **')
            return
        if len(line) < 3:
            self.__print('** attribute name missing **')
            return
        if len(line) < 4:
            self.__print('** value missing **')
            return
        value = line[3].partition('"')[2].partition('"')[0]
        obj = self.__storage.all()[key]
        if line[2] in obj:
            value = type(obj[line[2]])(value)
        obj[line[2]] = value
        self.__storage.save()

    def do_quit(self, empty):
        """The quit command exits the interpreter immediately"""

        return 1

    def do_EOF(self, empty):
        """The interpreter exits when EOF is reached on its input"""

        return 1

    def emptyline(self):
        """Do nothing if an empty line is typed"""

        return 0

    def help_all(self):
        """Help for all command"""

        self.__print(
            'Usage: all [CLASS]',
            'Prints a list of data model instances. If CLASS is given, print',
            'only instances of that class. Otherwise, print them all.',
            sep='\n'
        )

    def help_create(self):
        """Help for create command"""

        self.__print(
            'Usage: create CLASS',
            'Creates a new instance of the given data model class.',
            sep='\n'
        )

if __name__ == '__main__':
    HBNBCommand().cmdloop()
