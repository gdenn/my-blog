---
layout: post
title: Python Descriptors
categories: [Python]
---

## Abstract

The Python descriptor protocols makes it possible to customize the **access** of attributes.
We will have in depth look at the descriptor protocol in this post. 
We will not only learn how to apply descriptors to our own attributes but will also have a look at potential use cases.

### What are Descriptors?

Any class that defines *at least one* of the methods `__get__`, `__set__` or `__delete__` is called a descriptor.
The idea behind these methods is to override the **read**, **write** and **delete** behavior of an attribute.

Let us have a look at an concrete example.

```python
class Dog:
    def __init__(self.name):
        self.name = name
```

The `Dog` class yields a single instance attribute `name`. 

We can **access** this attribute with this syntax:

```python
my_dog = Dog(name="Max")

# read
my_dog.name

# write
my_dog.name = "Martin"

# delete
del my_dog.name
```

```python
class MyString:

    def __init__(self, initial_value):
        self.value = initial_value

    def __get__(self, parent, type):
        print("read: {}".format(self.value))
        return self.value

    def __set__(self, parent, value):
        print("write: {}".format(new_value))
        self.value = new_value

    def __del__(self):
        print("delete")
        del self.value

class Dog:
    def __init__(self, name):
        self.name = MyString(initial_value="Max")
```
ow imaging we want to print log lines for every **read**, **write** and **delete** operation to the stdout.

We can achieve that with the **descriptor** protocol. 


You can see that our string attribute `name` using now the `MyString` type instead of a simple string literal class.

We had to implement the `MyString` class to define the `__get__`, `__set__` and `__del__` methods which override the default **read**, **write** and **delete** behavior.

Now, we perform the same operations as before again and have a look at the output that our modified descriptor code produces.

```python
my_dog = Dog("Max")

# read
my_dog
> read: Max

# write
my_dog.name = "Martin"
> write: Martin

# delete
del my_dog.name
> delete
```

## Descriptor API

Let us have a look at the function parameters that each of the descriptor protocol methods takes.

`__get__` takes two arguments.
The first parameter is the reference to the parent object (we called it `parent`) instance to which your descriptor attribute belongs.
In our example it was an instance of the `Dog` class that hosts the `name` parameter.

The seconds argument is the type of the parent class (we called this argument `type`) which in our case was the class type `Dog`.

`__set__` takes also two parameters.
The first one is the reference to the parent object instance while the second one is the new value that we want to set (we called it `value`).

Last but not least the `__del__` method. 
It takes no arguments and gets called **before** your attribute instance gets destroyed.

Thus, the `__del__` methods gives you the opportunity to apply some cleanup procedures before the attribute instance gets destroyed.

## Descriptor Protocol on class instances

Our example demonstrated the descriptor protocol with a object instance attribute.

But the protocol can be used with class instance attributes too.

```python
class MyString:

    def __init__(self, initial_value):
        self.value = initial_value

    def __get__(self, parent, type):
        print("read: {}".format(self.value))
        return self.value

    def __set__(self, parent, value):
        print("write: {}".format(new_value))
        self.value = new_value

    def __del__(self):
        print("delete")
        del self.value

class Dog:
    name = MyString(initial_value="Max")
```

`name` is now a class attribute in the code above.

We can access it this way.

```python
# read
Dog.name

# write
Dog.name = "Martin"

# delete
del Dog.name
```

## Use Case Scenarios for Descriptors

Now, we know how to create descriptors for both class and instance attributes.

Let us explore a couple of use cases where we could make use of the descriptor protocol.


### Protected Attributes

We want to protect the access for a specific attribute in our first use case.

This is actually not so easy to do in Python since the language design does not offer encapsulation.
Thus, you may access any attribute of any object instance however you like.

In contrast, languages like Java offer modifiers like the `private` modifier to encapsulate access to object instance attributes.


```python
class Password:

    def __init__(self, password=None):
        self.password = password

    def has_permission(self):
        # code that decides whether the caller can
        # access the attribute or not

    def __get__(self, parent, type):

        if self.has_permission():
            return self.password
        else:
            raise UnauthorizedAccessError(...))

    def __set__(self, parent, new_password):
        if self.has_permission():
            password = value
        else:
            raise UnauthorizedAccessError(...)

class User:
    def __init__(...)
        ...
        self.active_userpassword = MyProtectedPassword()
```

We used the descriptor protocol in our example to protect the access to the `password` attribute in our `User` object instances.

What we achieved here is a **runtime protection** of the attribute.
Thus, you can still write valid Python code that acesses the `password` attribute of any `User` object instance but unauthorized accesses result in a UnauthorizedAcessError.

### Injecting Middleware

Middleware is a very common term in web programming.
It means that we can add behavior before or after a method call.

We actually already made an example for a logging middleware.
The `name` attribute of our `Dog` class used a logging middleware for the descriptor methods `__get__`, `__set__` and `__del__`.

But let us have a look at another example.

```python
class Config:

    def __init__(self, initial_config=None, file_path):
        self.config_str = initial_config if initial_config is not None else Config._read_from_disk(file_path)
        self.file_path = file_path

    @staticmethod
    def _write_to_disk(file_path, new_config_str):
        # code that writes the new_config_str into the file on path file_path

    @staticmethod
    def _read_from_disk(file_path):
        # code that reads the file on file_path into a string

    def __get__(self, parent, type):
        return self.config_str

    def __set__(self, parent, new_config_str):
        self.config_str = new_config_str
        Config._write_to_disk(self.file_path, new_config_str)

class Application:
    app_config = Config(None, "/tmp/config.txt")
```

Our `Application` class uses a class attribute `app_config` of type `Config`.
The descriptor methods in `Config` make sure that our in memory config changes get written to the disk.

This is really neat because there is no way that a caller modifies the in memory value of `app_config` without writing the changes back to the disk.

Furthermore, our `Config` attribute hides the logic that deals with the disk from the caller.
The callers only concern is to access the in memory value of `app_config`.

## Wrap Up

We saw how we can write our own descriptor attributes for both object instance and class attributes. 
Furtermore, we saw a few use cases that benefitted from he application of the descriptor protocol.

As always, the descriptor protocol is a design choice that targets specific use cases.

It is not a golden hammer!

Do not use it for every attribute that you write.
You should always work from the problem to the solution and not the other way around.

What do I mean by that?

Learning new design patterns and language constructs is very exciting.
But we should not be carried away by this excitment and apply the new techniques wherever we see fit.
Thus, working from the solution => the design pattern or language construct to the problem.

Instead, you should always analyze your problem first and try to come up with the **simplest** solution available.

Just keep a pragmatic mindset, the rest will come with experience!




What is your opinion about the descriptor protocol and in which cases would you apply it?

I look forward the here your suggestion.

cheers, Dennis