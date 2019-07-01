# Holberton AirBnB Clone Engine Package

Jump to [`storage`](#storage-module) [`file_storage`](#file_storage-module)

## Storage Module

### Classes

#### Storage

```python
class Storage (ABC)
```

Known Subclasses:
* [`FileStorage`](#filestorage)

As `Storage` is an abstract class, it cannot be instantiated directly. Instead, it serves as the base class for the rest of the storage engine classes. It defines methods for adding, retrieving, deleting, and saving data model objects. Mutating objects can be achieved by retrieving them and modifying them afterward, since all known data model classes are fully mutable.

Keep in mind that changes to objects, as well as calls to [`new`](#storage-new) and [`delete`](#storage-delete), are not immediately reflected in persistent storage. Use [`save`](#storage-save) to commit your changes.

---

##### Method Summary

| Method | Description |
| ------ | ----------- |
| [`__contains__(self, obj)`](#storage-__contains__) | check if an object exists in storage |
| [`delete(self, cls, id)`](#storage-delete) | delete an object in storage |
| [`get(self, cls, id)`](#storage-get) | retrieve an object from storage |
| [`new(self, obj)`](#storage-new) | add a new object to storage |
| [`reload(self)`](#storage-reload) | reload objects and discard changes |
| [`save(self)`](#storage-save) | commit changes to stored objects |
| [`tryGet(self, cls, id, default)`](#storage-tryget) | try retrieving an object with a fallback vaulue |

---

##### Method Details

###### Storage. \_\_contains\_\_

```python
@abstractmethod
def __contains__(self, obj: models.base_model.BaseMode) -> bool
```

Exceptions:
* none

Check if an object exists in storage, returning `True` if that object is stored and `False` if it isn't. This method is called automatically when the `in` or `not in` operator is used, allowing you to write something like `if State(id='1234') in storage:`.

`Storage` subclasses must be able to find stored objects this way when `obj` has the same type and ID as a stored object. Subclasses may also support other types for `obj`.

---

###### Storage. delete

```python
@abstractmethod
def delete(self, cls: Union[type, str], id: [UUID, str]) -> None
```

Exceptions:
* `KeyError` if the identified object isn't in storage

Delete an object from storage. Since data model objects of different types are often stored in different locations, you must pass the object's class as well as its ID.

Remember that deleted objects are not removed from persistent storage immediately; see [`save`](#Storage-save).

---

###### Storage. get

```python
@abstractmethod
def get(self, cls: Union[type, str], id: Union[UUID, str]) -> models.base_model.BaseModel
```

Exceptions:
* `KeyError` if the identified object isn't in storage

Retrieve an object from storage. Since data model objects of different types are often stored in different locations, you must pass the object's class as well as its ID.

---

###### Storage. new

```python
@abstractmethod
def new(self, obj: models.base_model.BaseModel) -> None
```

Exceptions:
* none

Add a new object to storage. Using this method to modify stored objects is not recommended and may cause issues. Instead use the workflow described in the `Storage` class summary.

Remember that new objects aren't added to persistent storage immediately; see [`save`](#Storage-save).

---

###### Storage .reload

```python
@abstractmethod
def reload(self) -> None
```

Exceptions:
* varies depending on subclass

Reload objects from storage into memory, also discarding any un-saved changes.

Subclasses that use a sophisticated storage system like an SQL database may not do any work to load objects from storage, but must still discard changes.

---

###### Storage. save

```python
@abstractmethod
def save(self) -> None
```

Exceptions:
* varies depending on subclass

Commit in-memory changes to stored objects into some persistent storage medium. This allows you to bundle small changes together, removing the need to run expensive disk IO or database accesses for every change.

---

###### Storage. tryGet

```python
@abstractmethod
def tryGet(self, cls: Union[type, str], id: Union[UUID, str], default: Any) -> Any
```

Exceptions:
* none

Try to retrieve an object and return it, but return `default` instead if the identified object does not exist in storage. Since data model objects of different types are often stored in different locations, you must pass the object's class as well as its ID.

---

## File\_Storage Module

### Functions

#### file\_storage. key

```python
def key(cls: Union[type, str], id: Union[UUID, str]) -> str
```

Exceptions:
* none

Return a string formatted for use as a key with the `FileStorage` class. These keys are used internally, but it can also be convenient to use this function with `FileStorage.__contains__` rather than construct a dummy data model object.

---

### Classes

#### FileStorage

```python
class FileStorage (models.engine.storage.Storage)
```

`FileStorage` implements all abstract method of [`Storage`](#storage) and thus can be instantiated. However, this isn't very useful, since it uses class fields to keep track of stored objects and none of the methods use the `self` parameter. Using this class like `FileStorage.get(None, 'BaseModel', '1234')` works just fine. This means the entire project shares a storage file, so be wary of conflicting changes between multiple pieces of code that use this class.

This storage engine uses a local JSON file in the working directory of the project with a fixed name: "storage.json". All stored objects are loaded into memory at once and kept in a single dictionary, where they keys are strings consisting the object's class name, then a dot, then the object's ID.

This storage engine is slow and is a memory hog, but it is easy to implement and easy to debug, so it's useful when testing other parts of the project.

---

##### Method Summary

| Method | Description |
| ------ | ----------- |
| [`__contains__(self, obj)`](#filestorage-__contains__) | check if an object is in storage |
| [`all(self)`](#filestorage-all) | get all stored objects |
| [`delete(self, cls, id)`](#storage-delete) | delete an object from storage |
| [`get(self, cls, id)`](#storage-get) | retrieve an object from storage |
| [`new(self, obj)`](#storage-new) | add a new object to storage |
| [`reload(self)`](#filestorage-reload) | reload objects from storage and discard changes |
| [`save(self)`](#filestorage-save) | save changes to storage |
| [`tryGet(self, cls, id, default)`](#storage-tryget) | try to retrieve an object from storage with a fallback value |

---

##### Method Details

###### FileStorage. \_\_contains\_\_

```python
def __contains__(self, obj: Union[models.base_model.BaseModel, str])
```

Exceptions:
* none

In addition to the mandatory behavior of [`Storage.__contains__`](#storage-__contains__), this method allows `obj` to be a string in the format returned by [`key`](#filestorage-key).

---

###### FileStorage. all

```python
def all(self) -> Dict[str, models.base_model.BaseModel]
```

Return all stored data model objects as a dictionary. The keys in this dictionary are strings that consist of the object's class name, then a dot, then the object's ID. This dictionary is the same one used internally in `FileStorage`, so adding and removing items in it will change what ends up in the storage file.

---

###### FileStorage. reload

```python
def reload(self) -> None
```

Exceptions:
* `OSError` if the storage file cannot be read
* `ValueError` if the storage file is not valid JSON

Reload all objects from a file called "storage.json" in the working directory into an internal dictionary, discarding any un-saved changes. If this file does not exist, instead do nothing.

---

###### FileStorage. save

```python
def save(self) -> None
```

Exceptions:
* `OSError` if the storage file cannot be written to
* `TypeError` if one of the objects contains a value that is not JSON-serializable

Save all objects in memory to a file called "storage.json" in the working directory. If this file doesn't exist, create it first. If it exists, first truncate it so it is empty.
