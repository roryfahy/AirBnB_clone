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
        self.__commands = [m[3:] for m in dir(self) if m.startswith('do_')]
        self.__print = functools.partial(print, file=self.stdout)
        self.__storage = FileStorage()

    def __getModels(self):
        ret = pkgutil.iter_modules(models.__path__)
        ret = (module[1] for module in ret if not module[2])
        ret = ((name.title().replace('_', ''), name) for name in ret)
        ret = ((cls, importlib.import_module('models.' + mod)) for cls, mod in ret)
        ret = {cls: getattr(mod, cls) for cls, mod in ret}
        return ret

    def default(self, line):
        """Check if the typed command looks like a Python method call"""

        cls, _, piece = line.partition('.')
        command, _, piece = piece.partition('(')
        piece = '(' + piece.replace(')', ',)')
        if piece != '(,)':
            try:
                piece = eval(piece)
            except SyntaxError:
                return super().default(line)
        else:
            piece = None
        if command not in self.__commands:
            return super().default(line)
        if command == 'update':
            self.special_update(cls, piece)
        else:
            line = command + ' ' + cls
            if piece is not None:
                line += ' ' + ' '.join(str(arg) for arg in piece)
            self.onecmd(line)

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

    def do_count(self, line):
        """Count the number of instances of a given class"""

        if line == '':
            self.__print('** class name missing **')
            return
        cls = line.partition(' ')[0]
        if cls not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        count = 0
        for key, obj in self.__storage.all().items():
            if key.partition('.')[0] == cls:
                count += 1
        self.__print(count)

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
        line = line.split(maxsplit=4)
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
        obj = self.__storage.all()[key]
        value = eval(line[3])
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

    def special_update(self, cls, args):
        """Update a data model instance using the advanced syntax"""

        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in self.__classes:
            self.__print('** class doesn\'t exist **')
            return
        if len(args) < 1:
            self.__print('** instance id missing **')
            return
        try:
            key = cls + '.' + args[0]
        except TypeError:
            key = None
        if key not in self.__storage.all():
            self.__print('** no instance found **')
            return
        if len(args) < 2:
            self.__print('** attribute name missing **')
            return
        if len(args) < 3 and not isinstance(args[1], dict):
            self.__print('** value missing **')
            return
        if len(args) > 2:
            obj = self.__storage.all()[key]
            value = args[2]
            if args[1] in obj:
                value = type(obj[args[1]])(args[2])
            obj[args[1]] = value
            self.__storage.save()
        else:
            obj = self.__storage.all()[key]
            obj.update(args[1])
            self.__storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
