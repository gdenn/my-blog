---
layout: post
title: "Why should you use the Python Descriptor Protocol?"
permalink: python-descriptors
categories:
- Advanced Python
excerpt: "Find out what makes the descriptor protocol such a great addition to Python's data model and how you can apply it in your code"

---

## Abstract

The python descriptor protocol offers a neat, yet powerful way to handle the access of class and instance attributes.
 

### Key Points

* What is the descriptor protocol?

* How do I apply the descriptor protocol?

* Close look at the descriptor API

* Applications of the descriptor protocol.

* Use descriptors and decorators to implements the `@property` annotation


### Descriptor Protocol

The Python descriptor protocol is an addition to the Python data model. You can use descriptors to customize the **access** of class and object instance attributes.

Sounds pretty abstract, doesn't it? ;-)


```python
class Person:
    
    name = "Mustermann"
    
    def __init__(self):
        self.first_name = "Max"
        
        
person = Person()

# read
person.name
person.first_name

# write
person.name = "Mareike"
person.first_name = "Maike"

# delete
del person.name
del person.first_name
```

Our `Person` class contains two attributes.

* The class attribute `name`

* The object instance attribute `first_name`

The code above demonstrates how we can access these two attributes through the **read**, **write**, and **delete** operations.

Most of you already know this syntax. 
But it is interesting to have a deeper look into the Python data model to see how the access truly works.

Python stores methods and attributes in a special variable called `__dict__`. 
The `__dict__` variable is a dictionary. 
The dictionary keys reference the name of an attribute or method, and the value is the attribute value or method object.


```python
person = Person()

print(person.__dict__.keys())

print(Person.__dict__.keys())
```

    dict_keys([])
    dict_keys(['__module__', 'name', '__dict__', '__weakref__', '__doc__'])


As you can see, object instances and class objects have their own `__dict__` variable.

This separation is necessary to have independent object instance attributes and methods (state).

You can spot the `name` class attribute in the output of `Person.__dict__` and the `first_name` object instance attribute in the output of `person.__dict__`. 

This is a very simple, yet powerful concept. 

The read, write and delete operations that we demonstrated above are just **syntactic sugar**. 
Your interpreter will operate on the respective `__dict__` data structures to carry out the operations.

The accessor functions that the interpreter uses therefore are `getattr`, `setattr`, and `delattr`.


```python
person = Person()

# read
getattr(Person, "name")
getattr(person, "first_name")

# write
setattr(Person, "name", "Mareike")
setattr(person, "name", "Maike")

# delete
delattr(Person, "name")
delattr(person, "first_name")
```

I guess some of you are already familiar with those methods. 

They become very useful when refactoring code and make class and object instance attributes dynamically accessible.

But why do we not operate on the `__dict__` variables directly?


```python
# read
Person.__dict__["name"]

# write
Person.__dict__["name"] = "Mareike"

# delete
del Person.__dict__["name"]
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-68-7ab3e836bd7a> in <module>
          3 
          4 # write
    ----> 5 Person.__dict__["name"] = "Mareike"
          6 
          7 # delete


    TypeError: 'mappingproxy' object does not support item assignment


You cannot write to the `__dict__` data structure directly. 

The reason for this becomes clear when we have a look at the descriptor protocol.

Descriptors allow us to **customize** the way `getattr`, `setattr` and `delattr` **access** instance or class attributes.

Here is a simplified version of the `Person` example with a descriptor class attribute.


```python
import logging

logging.basicConfig(level=logging.INFO)

class MyStringField:
        
    def __get__(self, obj, obj_type=None):
        logging.info("__get__: self._name -> %r", obj._name)
        return obj._name
    
    def __set__(self, obj, value):
        logging.info("__set__: self._name <- %r", value)
        obj._name = value
        
    def __delete__(self, obj):
        logging.info("__delete__: self._name")
        del obj._name
        

class Person:
    
    name = MyStringField()
```

What do you think? Does our name descriptor attribute customize the access for an **instance** or for a **class attribute**?


```python
person = Person()

person.name = "Max Mustermann"
person.name
del person.name
```

    INFO:root:__set__: self._name <- 'Max Mustermann'
    INFO:root:__get__: self._name -> 'Max Mustermann'
    INFO:root:__delete__: self._name


The descriptor attribute `name` is a **class attribute** but it handles the **access** of the **instance attribute** `_name`.

What happens when we put our descriptor in an instance attribute?


```python
class Person:
    
    def __init__(self):
      self.name = MyStringField()
        
person = Person()

person.name = "Max Mustermann"
person.name
del person.name
```

You can see on the missing log output that our descriptor methods `__get__`, `__set__` and `__delete__` do not get invoked.

This is one of the descriptor protocol oddities, **descriptors only work on class attributes**!

### Descriptor API

I guess by now you understood how the descriptor methods `__get__`, `__set__` and `__delete__` is connected to the attribute access.

The accessor methods `getattr`, `setattr` and `delattr` invoke the descriptor methods if they exist. 
That is also the reason why we cannot modify the `__dict__` data structures directly. 
Modifying the `__dict__` data structures directly would not invoke the descriptor methods of an attribute.

Here is a listing of all descriptor protocol methods.

```python

"""
Override read access behavior.

:param obj: reference to the object instance (nullable)
:param obj_type: reference to the object instance type (nullable)
"""
__get__(self, obj, obj_type=None) -> object

"""
Override write access behavior.

:param obj: @see __get__
:param value: the next value that the caller assigns
"""
__set__(self, obj, value) -> None

"""
Inform the Descriptor about its name.

E.g.
class MyDescriptor:

   __set_name__(self, obj_type, name):
       ...

class Person:
  first_name = MyDescriptor()
  

The call `name = MyDescriptor()` invokes 
__set_name__ with the name="first_name".

:param obj: @see __get__
:param name: descriptor name

"""
__set_name(self, obj_type, name) -> None


"""
Override delete behavior

:param obj: @see __get__
"""
__delete__(self, obj) -> None
```

The listing contains a new function `__set_name__` which we will explore in the next section.

But for now, let us have a look at the `obj` and `obj_type` parameters.

`obj` yields a reference to the object instance on which the descriptor got invoked while
`obj_type` references the type.

Sounds confusing? Let's explain it with an example:


```python
import logging

logging.basicConfig(level=logging.INFO)

class MyStringField:
        
    def __get__(self, obj, obj_type=None):
        logging.info("__get__: obj: %r, obj_type: %r", obj, obj_type)
        return obj._name
    
    def __set__(self, obj, value):
        logging.info("__set__: obj: %r", obj)
        obj._name = value
        
    def __delete__(self, obj):
        logging.info("__delete__: obj: %r", obj)
        del obj._name
        

class Person:
    
    name = MyStringField()
    
    
person = Person()

person.name = "Max Mustermann"
person.name
del person.name
```

    INFO:root:__set__: obj: <__main__.Person object at 0x7f4bf024b7f0>
    INFO:root:__get__: obj: <__main__.Person object at 0x7f4bf024b7f0>, obj_type: <class '__main__.Person'>
    INFO:root:__delete__: obj: <__main__.Person object at 0x7f4bf024b7f0>


You can see in the log output that `obj` references a `person` object instance, while `obj_type` references the `Person` type.

Our descriptors can customize the access to class and instance attributes through the `obj` and `obj_type` parameters.

### `__set_name__`

All descriptors that we wrote so far had to know the name of the property for which they handle the access. 
So to say, the property name was **hardcoded**. 

The `__set_name__` descriptor method is there to make our descriptors more generic.


```python
import logging


class MyProperty:
    
    def __init__(self, prop_type):
        self._type = prop_type
    
    def __set_name__(self, obj_type, name):
        logging.info("__set_name__ with name: %r", name)
        self.property_name = "_name"
        
    def __get__(self, obj, obj_type=None):
        value = getattr(obj, self.property_name)
        logging.info("__get__: self.%r -> %r", self.property_name, value)
        return value
    
    def __set__(self, obj, value):
        
        if type(value) is not self._type:
            raise ValueError("expected type {} but got {} instead".format(self._type, type(value)))
            
        setattr(obj, self.property_name, value)
        logging.info("__set__: self.%r <- %r", self.property_name, value)

class Person:
    
    name = MyProperty(prop_type=str)
    first_name = MyProperty(prop_type=str)
    
    
person = Person()

person._name = "Mustermann"
person._first_name = 5

logging.info("attributes (after): %r", person.__dict__.keys())

logging.info("person.name: %r", person._name)
logging.info("person.first_name: %r", person._first_name)
    
```

    INFO:root:__set_name__ with name: 'name'
    INFO:root:__set_name__ with name: 'first_name'
    INFO:root:attributes (after): dict_keys(['_name', '_first_name'])
    INFO:root:person.name: 'Mustermann'
    INFO:root:person.first_name: 5


`MyProperty` saves the attribute name that we received through the `__set_name__` call as an instance attribute.

Note, we prefixed the property name with a `_` which is a common practice to name private instance attributes in Python.

And that's it. 
You now know how to apply the descriptor protocol!

Let us dedicate the rest of the blog post to practical examples that incorporate the descriptor protocol.

### Validator Descriptor

This example demonstrates how we can build our own property types. 

We want to build an abstract `Validator` attribute class that executes the `validate` method before the attribute gets modified.


```python
import logging
import re
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)


class ValidationException(Exception):
    pass

class PropertyWithValidator(ABC):

    def __set_name__(self, owner, name):
        self.property_name = "_" + name
        
    def __get__(self, obj, obj_type=None):
        value = getattr(obj, self.property_name)
        logging.info("__get__: %r -> %r", self.property_name, value)
        return value
        
    def __set__(self, obj, value):
        self.validate(value)
        logging.info("__set__: %r <- %r", self.property_name, value)
        setattr(obj, self.property_name, value)

    @abstractmethod
    def validate(self, value):
        pass
    
    
class IPv4(PropertyWithValidator):
    
    def validate(self, value):
        
        if type(value) is not str:
            raise ValidationException("{} must be a string to be a valid ipv4 address".format(value))
        
        ipv4_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
        if not ipv4_pattern.match(value):
            raise ValidationException("{} is not a valid ipv4 address".format(value))
    
class Flow:

    src_ipv4 = IPv4()
    dst_ipv4 = IPv4()
```

`PropertyWithValidator` is an abstract class (@see `ABC`) that invokes the abstract `validate` method before you can assign a new value to the descriptor attribute.

We used this abstract class in `IPv4` to implement a concrete Validator class. 
All we had to do for this was to implement a validate method. 

In our case, the method validate method uses the Python regexp lib `re` to ensure that values meet the IPv4 standard.


```python
flow = Flow()

logging.info("attributes: %r", flow.__dict__.keys())

flow.src_ipv4 = "2.2.2.2"
flow.dst_ipv4 = "5.5.5.5"
flow.src_ipv4
flow.dst_ipv4
```

    INFO:root:attributes: dict_keys([])
    INFO:root:__set__: '_src_ipv4' <- '2.2.2.2'
    INFO:root:__set__: '_dst_ipv4' <- '5.5.5.5'
    INFO:root:__get__: '_src_ipv4' -> '2.2.2.2'
    INFO:root:__get__: '_dst_ipv4' -> '5.5.5.5'





    '5.5.5.5'



As you can see, we can assign valid IPv4 addresses to `flow.src_ipv4` and `flow.dst_ipv4`.

But see what happens when we assign an invalid IPv4 string:


```python
flow.src_ipv4 = "5.5.5."
```


    ---------------------------------------------------------------------------

    ValidationException                       Traceback (most recent call last)

    <ipython-input-53-86168850f280> in <module>
    ----> 1 flow.src_ipv4 = "5.5.5."
    

    <ipython-input-48-f8c1cbfc54dd> in __set__(self, obj, value)
         20 
         21     def __set__(self, obj, value):
    ---> 22         self.validate(value)
         23         logging.info("__set__: %r <- %r", self.property_name, value)
         24         setattr(obj, self.property_name, value)


    <ipython-input-48-f8c1cbfc54dd> in validate(self, value)
         38         ipv4_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
         39         if not ipv4_pattern.match(value):
    ---> 40             raise ValidationException("{} is not a valid ipv4 address".format(value))
         41 
         42 class Flow:


    ValidationException: 5.5.5. is not a valid ipv4 address


### Runtime Access Protection

Our next example uses the descriptor protocol to implement a runtime access protection for a password attribute.


```python
from abc import ABC, abstractmethod

class UnauthorizedAccessException(Exception):
    REASON_UNAUTHORIZED_CALLER = "Caller is not authorized to perform {operation} operation on attribute {attribute}"

class ProtectedAttribute(ABC):
    
    def __set_name__(self, obj, name):
        self._property_name = "_" + name
    
    def __get__(self, obj, obj_type=None):
        
        if not self.is_access_authorized(obj):
            self._raise_unauthorized("read")
            
        return getattr(obj, self._property_name)
    
    def __set__(self, obj, value):
        
        if not self.is_access_authorized(obj):
            self._raise_unauthorized("write")
        
        setattr(obj, self._property_name, value)
        
    def _raise_unauthorized(self, operation):
        raise UnauthorizedAccessException(
                UnauthorizedAccessException.REASON_UNAUTHORIZED_CALLER.format(
                    operation=operation, 
                    attribute=self._property_name
                )
            )
        
    @abstractmethod
    def is_access_authorized(self, obj):
        pass
    
class SecurityContext:
    
    current_session = { "user_name": "Max Mustermann" }
    
class Password(ProtectedAttribute):
    
    def __init__(self, authorized_users):
        self._authorized_users = authorized_users
        
    def is_access_authorized(self, obj):
        
        return SecurityContext.current_session["user_name"] in self._authorized_users
    
class User:
    
    password = Password(authorized_users=["Maike Mareike"])
```

The `__set__` and `__get__` descriptor methods invoke the abstract `is_access_authorized` method before accessing the descriptor attribute value. 


```python
user = User()

user.password = "my_secret"
```


    ---------------------------------------------------------------------------

    UnauthorizedAccessException               Traceback (most recent call last)

    <ipython-input-80-b925f049f61b> in <module>
          1 user = User()
          2 
    ----> 3 user.password = "my_secret"
    

    <ipython-input-79-2e1ac42e3056> in __set__(self, obj, value)
         19 
         20         if not self.is_access_authorized(obj):
    ---> 21             self._raise_unauthorized("write")
         22 
         23         setattr(obj, self._property_name, value)


    <ipython-input-79-2e1ac42e3056> in _raise_unauthorized(self, operation)
         24 
         25     def _raise_unauthorized(self, operation):
    ---> 26         raise UnauthorizedAccessException(
         27                 UnauthorizedAccessException.REASON_UNAUTHORIZED_CALLER.format(
         28                     operation=operation,


    UnauthorizedAccessException: Caller is not authorized to perform write operation on attribute _password


This is a very simple example of runtime protection through the descriptor protocol.
But the idea behind it is very powerful.
Especially if you consider that the Python language lacks encapsulation.

Programming languages such as Java offer modifiers like `private` to encapsulate your code access.

While we cannot achieve an encapsulation through the typing system in Python, we can ensure it through descriptors at runtime.

There is no clean way to circumvent the `is_access_authorized` method while accessing the `user.password` field.

(We have to relativize this expression.
Python makes it possible to change the method implementation at runtime, also called "monkey patching".

Thus, it is possible to override the `setattr` and `getattr` implementation for the `Password` class at runtime.)

### Invoke Side Effects

Our next example is a `Configuration` attribute class. The `Configuration` gets represented as a dictionary data structure in memory, and as a JSON file on the file system.

The challenge with the `Configruation` attribute class is to keep it's value in memory in sync with the JSON file on disk.


```python
import json
import logging

logging.basicConfig(level=logging.INFO)

class JSONConfiguration:
    
    def __init__(self, file_path):
        self._file_path = file_path
        
    def __set_name__(self, obj, name):
        self._property_name = "_" + name
        
    def _write_to_disk(self, config_dict):
        
        logging.info("write config back to disk on path %r", self._file_path)
        json_str = json.dumps(config_dict)
        
        with open(self._file_path) as config_file:
            confoig_file.write(json_str)
        
    def __get__(self, obj, obj_type=None):
        return getattr(obj, self._property_name)
    
    def __set__(self, obj, value):
        setattr(obj, self._property_name, value)
        self._write_to_disk(value)
        

class Application:
    
    config = JSONConfiguration(
        file_path="/tmp/config.json", 
    )
```

The `Application.config` object behaves like a dictionary from the perspective of the caller. 

It completely hides the `_write_to_disk` method that gets invoked by the `__set__` descriptor method. 
This simplifies the contract between the `Application.config` attribute and the caller.

Without the use of descriptors, the contract would make the caller responsible for calling the `_write_to_disk` method after modifying the config dictionary data structure.


```python
application = Application()
application.config = { "host": "localhost", "port": "8088"}
```

    INFO:root:write config back to disk on path '/tmp/config.json'



    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    <ipython-input-70-0ccf8f4311f0> in <module>
          1 application = Application()
    ----> 2 application.config = { "host": "localhost", "port": "8088"}
    

    <ipython-input-64-06078f3aa6fa> in __set__(self, obj, value)
         25     def __set__(self, obj, value):
         26         setattr(obj, self._property_name, value)
    ---> 27         self._write_to_disk(value)
         28 
         29 


    <ipython-input-64-06078f3aa6fa> in _write_to_disk(self, config_dict)
         17         json_str = json.dumps(config_dict)
         18 
    ---> 19         with open(self._file_path) as config_file:
         20             confoig_file.write(json_str)
         21 


    FileNotFoundError: [Errno 2] No such file or directory: '/tmp/config.json'


(These code examples come from a Jupyter notebook, so please ignore the `FileNotFoundError` exception.)

### @property 

You may remember that I told you in the abstract how the descriptor protocol may help you understand the python standard library code?

This example demonstrates how the popular `@popular` annotation can be implemented through the descriptor and decorator protocols.


```python
import logging

logging.basicConfig(level=logging.INFO)

class prop:
    
    def __init__(self, fget=None, fset=None, fdel=None):
        self._fget = fget  
        self._fset = fset
        self._fdel = fdel
        
    def __get__(self, obj, obj_type):
        value = self._fget(obj)
        logging.info("read: {}".format(value))
        return value
    
    def __set__(self, obj, value):
        logging.info("write: {}".format(value))
        self._fset(obj, value)
        
    def __del__(self, obj):
        logging.info("del")
        self._fdel(obj)
        
    def __call__(self, fget):
        return type(self)(fget, self._fset, self._fdel)

    def setter(self, fset):
        return type(self)(self._fget, fset, self._fdel)

    def deleter(self, fdel):
        return type(self)(self._fget, self._fset, fdel)
        
class Person:
    
    @prop
    def name(self):
        return self._name
    
    @name.setter
    def set_name(self, value):
        self._name = value
    
    @name.deleter
    def delete_name(self):
        del self._name
        
    @prop
    def first_name(self):
        return self._first_name
        
    @first_name.setter
    def set_first_name(self, value):
        self._first_name = value
        
    @first_name.deleter
    def delete_first_name(self):
        del self._first_name
```

This code may look scary for you at first. 
Especially if you are not accustomed to the decorator protocol.

(Spoiler alert, we will have a blog post for the decorator protocol next ;-) )

I'll walk you through the code quickly.

First, let us understand how the decorator notion of the code works.

The `__init__` method gets called when you annotate the `@property` decorator. 
The arguments of the `__init__` method are the parameters that you pass to the decorator call.

We use a little trick in our example.

Our `@property` descriptor requires `getter`, `setter`, and `deleter` methods for our property.
But we do not want to pass all of the methods right away `@property(fget=..., fset=..., fdel=...)`.

We want to annotate the `getter`, `setter` and `deleter` separately to make our API even more elegant. 
Thus, we use `None` as the default parameter for our `fget`, `fset`, and `fdel` methods. 

Let us now see how we fill the decorator attributes `fget`, `fset`, and `fdel` with real methods.

The `__call__` method gets invoked when the decorator gets called. The `__call__` method takes a method as an argument (in our case the `fget` => getter method) and returns a method again.

Our `__call__` methods returns a new decorator that uses `fget` as getter method. The line
`type(self)(fget, self._fset, self._fdel)` returns the decorator instance itself while adding the `fget` method.

Last but not least, our descriptor methods invoke the `fget`, `fset`, and `fdel` methods.


```python
person = Person()
person.set_name = "Max"
person.set_first_name = "Mustermann"

logging.info("attributes: %r", person.__dict__.keys())
```

    INFO:root:write: Max
    INFO:root:write: Mustermann
    INFO:root:attributes: dict_keys(['_name', '_first_name'])


### Summary

So, that's it.
My first ever blog post and you made it right to the end, thank you! :-)

In this post, we learned a few things about the Python data model.
We demonstrated the accessor methods `getattr`, `setattr`, and `delattr` and explained how they relate to the Python `__dict__` data structure and to the descriptor protocol.

Later on, we saw applications of the descriptor protocol.
Finally, we saw how the popular `@property` annotation can be implemented through a synergy of the decorator and descriptor protocol.

Learning new protocols and syntaxes in a programming language is very exciting.
But we should not get carried away by this excitement.

The descriptor protocol proves useful in very specific scenarios, some of which we showed in the blog post.
Personally, I see the strength of the descriptor protocol especially in the design of APIs in Python libraries.

The protocol does a very good job at hiding implementation details and thus simplifying the contract between descriptor attribute and caller.

But it is not a **golden hammer**!

**Do not** write every attribute as descriptor attribute.

In general, programming should be about working yourself **from the problem to the solution**, not the other way around.

Thus, do not use design patterns or language constructs wherever you see fit!

I hope you could learn one or two things about Python through this post.
I surely did!

Please consider sharing a link to the post if you enjoyed reading it.
It helps me to build an audience and is greatly appreciated.

cheers,
Dennis



