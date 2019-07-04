#!/usr/bin/python3
"""Tests for the console"""


import console
import functools
import importlib
import io
import models
import models.engine.file_storage
import os
import os.path
import unittest


class TestConsole (unittest.TestCase):
    """Tests for the console"""

    @classmethod
    def setUpClass(cls):
        """Create the console and hook it up to a StringIO input and output"""

        if os.path.exists('storage.json'):
            os.remove('storage.json')
        TestConsole.i = io.StringIO()
        TestConsole.o = io.StringIO()
        TestConsole.cmd = console.HBNBCommand(
            stdin=TestConsole.i,
            stdout=TestConsole.o
        )
        TestConsole.cmd._HBNBCommand__print = \
            functools.partial(print, file=TestConsole.cmd.stdout)

    def tearDown(self):
        """Remove the JSON file after each test"""

        with open('storage.json', 'wt') as file:
            file.write('{}')
        models.storage.reload()

    def assertWrites(self, expected, command):
        """Check if a command causes some text to be written"""

        start = self.o.tell()
        self.cmd.onecmd(command)
        end = self.o.tell()
        self.o.seek(start)
        actual = self.o.read(end - start)
        self.assertEqual(actual, expected)

    def capture(self, command):
        """Check if a command causes some text to be written"""

        start = self.o.tell()
        self.cmd.onecmd(command)
        end = self.o.tell()
        self.o.seek(start)
        return self.o.read(end - start)

    def test_all(self):
        """all command"""

        with self.subTest(msg='no content'):
            self.assertWrites('[]\n', 'all')
        with self.subTest(msg='no content with filter'):
            for fake in models.classes.keys():
                for real in models.classes.keys():
                    if real != fake:
                        self.cmd.onecmd('create ' + real)
                        self.cmd.onecmd('create ' + real)
                self.assertWrites('[]\n', 'all ' + fake)
                self.assertWrites('[]\n', fake + '.all()')
                models.storage.all().clear()
        with self.subTest(msg='one object'):
            for cls in models.classes.keys():
                id = self.capture('create ' + cls)[:-1]
                expected = str([str(models.storage.get(cls, id))]) + '\n'
                self.assertWrites(expected, 'all')
                models.storage.all().clear()
        with self.subTest(msg='one object with filter'):
            for real in models.classes.keys():
                id = self.capture('create ' + real)[:-1]
                expected = str([str(models.storage.get(real, id))]) + '\n'
                self.assertWrites(expected, 'all ' + real)
                expected = '[' + str(models.storage.get(real, id)) + ']\n'
                self.assertWrites(expected, real + '.all()')
                models.storage.all().clear()
            for real in models.classes.keys():
                for fake in models.classes.keys():
                    if real != fake:
                        self.cmd.onecmd('create ' + fake)
                        self.cmd.onecmd('create ' + fake)
                id = self.capture('create ' + real)[:-1]
                expected = str([str(models.storage.get(real, id))]) + '\n'
                self.assertWrites(expected, 'all ' + real)
                expected = '[' + str(models.storage.get(real, id)) + ']\n'
                self.assertWrites(expected, real + '.all()')
                models.storage.all().clear()
        with self.subTest(msg='multiple objects'):
            for cls in models.classes.keys():
                self.cmd.onecmd('create ' + cls)
                self.cmd.onecmd('create ' + cls)
            objs = list(models.storage.all().values())
            expected = str([str(o) for o in objs]) + '\n'
            self.assertWrites(expected, 'all')
            models.storage.all().clear()
        with self.subTest(msg='multiple objects with filter'):
            for cls in models.classes.keys():
                self.cmd.onecmd('create ' + cls)
                self.cmd.onecmd('create ' + cls)
            for name, cls in models.classes.items():
                objs = [
                    o
                    for o in models.storage.all().values()
                    if type(o) is cls
                ]
                expected = str([str(o) for o in objs]) + '\n'
                self.assertWrites(expected, 'all ' + name)
                expected = '[' + ', '.join(str(o) for o in objs) + ']\n'
                self.assertWrites(expected, name + '.all()')

    def test_allErrors(self):
        """Errors with the all command"""

        self.assertWrites("** class doesn't exist **\n", 'all NotAClass')
        self.assertWrites("** class doesn't exist **\n", 'NotAClass.all()')

    def test_notACommand(self):
        """Try running a command that doesn't exist"""

        self.assertWrites('*** Unknown syntax: notacommand\n', 'notacommand')

    def test_count(self):
        """count command"""

        with self.subTest(msg='no objects'):
            self.assertWrites('0\n', 'State.count()')
        with self.subTest(msg='some objects'):
            self.cmd.onecmd('create State')
            self.cmd.onecmd('create State')
            self.assertWrites('2\n', 'State.count()')

    def test_create(self):
        """create command"""

        with self.subTest(msg='valid class'):
            self.cmd.onecmd('create State')
            self.assertEqual(len(models.storage.all()), 1)
            self.cmd.onecmd('State.create()')
            self.assertEqual(len(models.storage.all()), 2)
            classes = []
            for key in models.storage.all():
                classes.append(key.partition('.')[0])
            self.assertEqual(classes.count('State'), 2)
        with self.subTest(msg='invalid class'):
            self.assertWrites("** class doesn't exist **\n", 'create None')
            self.assertWrites("** class doesn't exist **\n", 'None.create()')
            classes = []
            for key in models.storage.all():
                classes.append(key.partition('.')[0])
            self.assertEqual(classes.count('None'), 0)

    def test_destroy(self):
        """destroy command"""

        with self.subTest(msg='object exists'):
            self.cmd.onecmd('create City')
            obj = next(iter(models.storage.all().values()))
            self.cmd.onecmd('create City')
            self.assertWrites('', 'destroy City ' + obj.id)
            key = 'City.' + obj.id
            self.assertNotIn(key, models.storage.all())
            obj = next(iter(models.storage.all().values()))
            self.assertWrites('', 'City.destroy("' + obj.id + '")')
        with self.subTest(msg='object doesn\'t exist'):
            command = 'destroy City ' + obj.id
            self.assertWrites('** no instance found **\n', command)
            command = 'City.destroy("' + obj.id + '")'
            self.assertWrites('** no instance found **\n', command)
        with self.subTest(msg='missing arguments'):
            self.assertWrites('** instance id missing **\n', 'destroy City')
            self.assertWrites('** instance id missing **\n', 'City.destroy()')
            self.assertWrites('** class name missing **\n', 'destroy')
            self.assertWrites("** class doesn't exist **\n", 'destroy None')
            self.assertWrites("** class doesn't exist **\n", 'None.destroy()')

    def test_prompt(self):
        """Check the command prompt"""

        self.i.write('quit\n')
        start = self.o.tell()
        self.cmd.cmdloop()
        end = self.o.tell()
        self.o.seek(start)
        self.assertEqual(self.o.read(end - start), '(hbnb) \n')

    def test_show(self):
        """show command"""

        with self.subTest(msg='object exists'):
            self.cmd.onecmd('create User')
            obj = next(iter(models.storage.all().values()))
            self.assertWrites(str(obj) + '\n', 'show User ' + obj.id)
            self.assertWrites(str(obj) + '\n', 'User.show("' + obj.id + '")')
        with self.subTest(msg='object doesn\'t exist'):
            self.assertWrites('** no instance found **\n', 'show User hi')
            self.assertWrites('** no instance found **\n', 'User.show("hi")')
        with self.subTest(msg='missing arguments'):
            self.assertWrites('** instance id missing **\n', 'show User')
            self.assertWrites('** instance id missing **\n', 'User.show()')
            self.assertWrites('** class name missing **\n', 'show')
            self.assertWrites("** class doesn't exist **\n", 'show None hi')
            self.assertWrites("** class doesn't exist **\n", 'None.show("hi")')

    def test_update(self):
        """update command"""

        with self.subTest(msg='new attribute'):
            self.cmd.onecmd('create Place')
            obj = next(iter(models.storage.all().values()))
            self.assertWrites('', 'update Place ' + obj.id + ' name "place"')
            self.assertEqual(obj.name, 'place')
            command = 'Place.update("{}", "city", "New Haven")'.format(obj.id)
            self.assertWrites('', command)
            self.assertEqual(obj.city, 'New Haven')
        with self.subTest(msg='change attribute'):
            obj.rooms = 5
            obj.save()
            command = 'update Place {} rooms "2"'.format(obj.id)
            self.assertWrites('', command)
            self.assertEqual(obj.rooms, 2)
            command = 'Place.update("{}", "rooms", "3")'.format(obj.id)
            self.assertWrites('', command)
            self.assertEqual(obj.rooms, 3)
        with self.subTest(msg='update from dictionary'):
            attrs = {'state': 'CT', 'number': 27, 'latitude': 2.2}
            command = 'Place.update("{}", {})'.format(obj.id, str(attrs))
            self.assertWrites('', command)
            self.assertEqual(obj.state, 'CT')
            self.assertEqual(obj.number, 27)
            self.assertEqual(obj.latitude, 2.2)

    def test_updateInvalid(self):
        """Invalid update command lines"""
        self.assertWrites("** class name missing **\n", "update")
        self.assertWrites("** class doesn't exist **\n", "update MyModel")
        self.assertWrites("** instance id missing **\n", "update BaseModel")
        self.assertWrites("** no instance found **\n",
                          "update BaseModel notanid")
        id = self.cls_id('create BaseModel')
        self.assertWrites("** attribute name missing **\n",
                          "update BaseModel {}".format(id))
        self.assertWrites("** value missing **\n",
                          "update BaseModel {} first_name".format(id))
        self.assertWrites("",
                          'update BaseModel {} first_name "bet" ex'.format(id))
