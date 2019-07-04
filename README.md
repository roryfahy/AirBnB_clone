# Holberton AirBnB Clone

[The data models](models) and [the storage engine](models/engine), the two major components of the project at this time, are documented in their own READMEs.

## Project Concepts

* How to create a Python package
* How to create a command interpreter in Python using the cmd module
* What is Unit testing and how to implement it in a large project
* How to serialize and deserialize a Class
* How to write and read a JSON file
* How to manage datetime
* What is an UUID
* What is \*args and how to use it
* What is \*\*kwargs and how to use it
* How to handle named arguments in a function

## Unit Tests

The unit tests can be easily run by doing `python3 -m unittest discover tests` from the root directory of this repository.

Be careful when running the tests, as they'll delte your "storage.json" file in order to test it. Back it up or only run these tests when you set up the project.

## The Console

The project includes a simple command interpreter that links the storage system and the data models together. You can use it by running the executable script "console.py". Run it from the root directory of this repository.

The console is usable interactively and non-interactively, although it will still print a command prompt in non-interactive mode.

### General Syntax

Commands are separated by line breaks.

There are two formats for commands that you can use:
* A command-shell style syntax. Arguments to commands are separated by spaces unless stated otherwise. Arguments are always interpreted in the order they're written, and if there are more arguments passed to a command than that command accepts, the additional arguments are ignored. Example: `show City 1234-567`
* A syntax made to look like Python method calls. This form is only valid for commands that take a `CLASS` argument. Here, the class name is written first, then a dot, then the name of the command, then a set of parentheses. Within the parentheses are all the other arguments to the command, each one surrounded by quotes and separated by a comma and a space. Example: `City.show("1234-567")`

### The `all` Command

Usage:
* `all [CLASS]`
* `CLASS.all()`

Prints all data model objects in storage, or all objects in storage of a particular class if the optional CLASS argument is supplied.

The output looks like a Python list of strings (`["object1", "object2"...]`). Each string is the result of [`BaseModel.__str__`](models#basemodel-__str__). If no objects are found, the result is "\[\]".

### The `count` Command

Usage:
* `count CLASS`
* `CLASS.count()`

Prints the number of data model objects in storage for the given class.

The output is a simple integer on its own line.

### The `create` Command

Usage:
* `create CLASS`
* `CLASS.create()`

Creates a new instance of the given class and saves it.

After saving the object, this command prints the ID of the new object. The ID is a random UUID. You can use this ID for other commands that require one.

### The `destroy` Command

Usage:
* `destroy CLASS ID`
* `CLASS.destroy(ID)`

Destroys a specific data model object.

Since data model objects of different types are often stored in different locations, supplying the ID isn't enough to easily identify an object, hence the syntax here.

### The `show` Command

Usage:
* `show CLASS ID`
* `CLASS.show(ID)`

Prints a description of the specified data model object.

The output is produced by [`BaseModel.__str__`](models#basemodel-__str__).

Since data model objects of different types are often stored in different locations, supplying the ID isn't enough to easily identify an object, hence the syntax here.

### The `update` Command

Usage:
* `update CLASS ID NAME VALUE`
* `CLASS.update(ID, NAME, VALUE)`
* `CLASS.update(ID, ATTRIBUTES)`

Updates one or more attributes on the specified data model object.

The interpretations of the CLASS, ID, and NAME arguments for this command are normal, but the VALUE argument is parsed uniquely.

When used in the first form shown above, the VALUE argument may or may not be surrounded with double quotes. If it is, then the argument is interpreted as a string that may contain spaces but may not contain double quotes. The argument is assumed to end when the second double quote character is found. If VALUE does not start with a double quote character, then it is interpreted as a Python literal value that may not contain spaces (such as a number if you write `2.5`).

When used in the second form shown above, the VALUE argument is interpreted as a Python literal value. It may contain spaces and it may contain escape characters within strings as supported by Python.

In both of these cases, the result depends on whether an attribute named NAME already exists on the specified object. If it doesn't, then the type of VALUE is kept the way you wrote it. If it does, then an attempt is made to case your value to the type of the existing attribute. For example, if you type `"5"` as the VALUE argument to update the `rooms` attribute a `Place` object that already has a `rooms` attribute with an integer value `3`, then the result will be the integer value `5`, not the string value `"5"`.

When used in the third form shown above, the VALUE argument must be a Python literal dictionary. The types within the dictionary can be mixed freely, and no attempt is made to convert the given types to the ones already contained within the object. For example, a command of this form could be `Place.update("1234-567", {'rooms': 4, 'name': "My House", 'amenities': [201, 202, 203]})`
