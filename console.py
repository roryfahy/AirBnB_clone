#!/usr/bin/python3
"""Module for command interpreter class"""


from ast import literal_eval
import cmd
import functools
import models


class HBNBCommand (cmd.Cmd):
    """Interpret commands for a pseudo-API in the AirBnB clone"""

    def __init__(self, *args, **kwargs):
        """create the interpreter with a given data model and save it"""

        super().__init__(*args, **kwargs)
        self.prompt = '(hbnb) '
        self.use_rawinput = False
        self.__commands = [m[3:] for m in dir(self) if m.startswith('do_')]
        self.__print = print

    def default(self, line):
        """Check if the typed command looks like a Python method call"""

        cls, _, piece = line.partition('.')
        command, _, piece = piece.partition('(')
        piece = '(' + piece.replace(')', ',)')
        if piece != '(,)':
            try:
                piece = literal_eval(piece)
            except SyntaxError:
                return super().default(line)
        else:
            piece = None
        if command not in self.__commands:
            return super().default(line)
        if command == 'update':
            self.special_update(cls, piece)
        elif command == 'all':
            self.do_all(cls, quote_objs=False)
        else:
            line = command + ' ' + cls
            if piece is not None:
                line += ' ' + ' '.join(str(arg) for arg in piece)
            self.onecmd(line)

    def do_all(self, line, quote_objs=True):
        """Print all data model objects, optionally filtered by class"""

        cls = line.partition(' ')[0]
        if cls == '':
            objects = [
                str(models.classes[k.partition('.')[0]](**v.to_dict()))
                for k, v in models.storage.all().items()
            ]
        else:
            if cls not in models.classes:
                self.__print('** class doesn\'t exist **')
                return
            objects = [
                str(models.classes[cls](**v.to_dict()))
                for k, v in models.storage.all().items()
                if k.partition('.')[0] == cls
            ]
        if quote_objs:
            self.__print(objects)
        else:
            self.__print('[' + ', '.join(str(obj) for obj in objects) + ']')

    def do_count(self, line):
        """Count the number of instances of a given class"""

        if line == '':
            self.__print('** class name missing **')
            return
        cls = line.partition(' ')[0]
        if cls not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        count = 0
        for key, obj in models.storage.all().items():
            if key.partition('.')[0] == cls:
                count += 1
        self.__print(count)

    def do_create(self, line):
        """Create a new data model instance and store it"""

        cls = line.partition(' ')[0]
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        obj = models.classes[cls]()
        models.storage.save()
        self.__print(obj.id)

    def do_destroy(self, line):
        """Destroy an existing data model instance"""

        cls, _, id = line.partition(' ')
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        if id == '':
            self.__print('** instance id missing **')
            return
        id = id.partition(' ')[0]
        if models.storage.tryGet(cls, id, None) is None:
            self.__print('** no instance found **')
            return
        models.storage.delete(cls, id)
        models.storage.save()

    def do_show(self, line):
        """print string representation of an instance"""

        cls, _, id = line.partition(' ')
        if cls == '':
            self.__print('** class name missing **')
            return
        if cls not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        if id == '':
            self.__print('** instance id missing **')
            return
        id = id.partition(' ')[0]
        obj = models.storage.tryGet(cls, id, None)
        if obj is None:
            self.__print('** no instance found **')
            return
        self.__print(obj)

    def do_update(self, line):
        """Update or add an attribute to a data model instance"""

        if line == '':
            self.__print('** class name missing **')
            return
        line = line.split(maxsplit=3)
        if line[0] not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        if len(line) < 2:
            self.__print('** instance id missing **')
            return
        obj = models.storage.tryGet(line[0], line[1], None)
        if obj is None:
            self.__print('** no instance found **')
            return
        if len(line) < 3:
            self.__print('** attribute name missing **')
            return
        if len(line) < 4:
            self.__print('** value missing **')
            return
        if line[3].startswith('"'):
            value = line[3].partition('"')[2].partition('"')[0]
        else:
            value = literal_eval(line[3].partition(' ')[0])
        if hasattr(obj, line[2]):
            value = type(getattr(obj, line[2]))(value)
        setattr(obj, line[2], value)
        obj.save()

    def do_quit(self, empty):
        """The quit command exits the interpreter immediately"""

        return 1

    def do_EOF(self, empty):
        """The interpreter exits when EOF is reached on its input"""

        self.__print()
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
        if cls not in models.classes:
            self.__print('** class doesn\'t exist **')
            return
        if len(args) < 1:
            self.__print('** instance id missing **')
            return
        obj = models.storage.tryGet(cls, args[0], None)
        if obj is None:
            self.__print('** no instance found **')
            return
        if len(args) < 2:
            self.__print('** attribute name missing **')
            return
        if len(args) < 3 and not isinstance(args[1], dict):
            self.__print('** value missing **')
            return
        if len(args) > 2:
            value = args[2]
            if hasattr(obj, args[1]):
                value = type(getattr(obj, args[1]))(args[2])
            setattr(obj, args[1], value)
        else:
            for name, value in args[1].items():
                setattr(obj, name, value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
