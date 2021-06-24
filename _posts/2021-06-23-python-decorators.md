---
layout: post
title: "How to write better code with Python Decorators"
permalink: python-decorators
categories:
- Advanced Python
excerpt: "Learn how you can write your own decorators and improve the flow of your code."
---

Decorators are one my favorite feature in Python.
You can use them to extend the functionality of existing functions without touching the function
code.

Sounds like magic?

It sure is.

That is exactly the reason why we will cover everything you need to know about decorators in this blog post.
So you can harness this magic for your own code. ;-)

Here are the key lessons that you learn in this post:

> * What are decorators and how do they work?
> * How do I write decorator functions and decorator classes
> * How do I pass arguments to decorators?
> * What is `functools.wraps` and why should I use it?
> * How can I mutate function state in decorators?
> * What are good use cases for decorators, when should I use them?

As always, we will end the blog post with some juicy code examples that make use of descriptors.

### What is a Python Decorator?

Functions are **first class objects** in Python.
That means that functions can be used as parameters or return values for functions.

```python
def hello(func):
    print("hello")
    func()
    
def world():
    print("world")
    
hello(world)
```

    hello 
    world

Our example calls the `hello` function with `world` as a parameter.
We can even go a step further and return `world` again in the call of `hello`.

```python
def hello(func):
    return func
    
def world():
    print("world")
    
hello(world)()
```

    world

We can even define a function within a function.

```python
def outer():

    def inner():
        print("hello")
        
    inner()
    
    print("world")
    
outer()
```

    hello
    world

And that is already everything we need to know about Python functions to understand what decorators are and how they work.

Now to the decorators itself.

> A Python decorator is a **function that takes a function as parameter and returns a function**.

```python
def my_decorator(my_function):
    
    def wrapper():
        print("called before function")
        my_function()
        print("called after function")
        
    return wrapper
```

`my_decorator` takes a function parameter (`my_function`).
We call the passed function object inside our nested `wrapper` function.

Thus, `wrapper` becomes a function that behaves like `my_function` but adds a print line before and after the call of `my_function`.

And that is already the key concept of a decorator.

You define a `wrapper` function that adds some extra behavior (in our case the print lines) and calls the passed function object (in our case `my_function`).

Last but not least, we return the `wrapper` function.
Thus, you put a function into the decorator and get a function out.
The signature of the function that you put in should be the same as the function (in our case `wrapper`) that comes out.

That is also where the name decorator comes from.
We essentially **decorate** an existing function with some additional functionality around it.

Let us now have a look how we can apply our `my_decorator` decorator through the magic `@` syntax.

```python
@my_decorator
def greetings():
    print("greetings")
    
greetings()
```

    called before function
    greetings
    called after function

As you can see, we executed the `wrapper` function that we defined in `my_decorator` which in turn used the passed `greetings` function.

The annotation `@my_decorator` is just a syntactic sugar.
We can achieve the same result in a more explicit way.

```python
def greetings():
    print("greetings")
    
greetings = my_decorator(greetings)

greetings()
```

    called before function
    greetings
    called after function

This is actually what our python interpreter does when we use `@my_decorator`.
It overrides the greetings method with the enhanced version of `my_decorator`.

It is also possible to apply multiple decorators (decorator composition) to the same function.

```python
def decorator_hello(func):
    
    def wrapper():
        print("hello")
        func()
        
    return wrapper

def decorator_world(func):
    
    def wrapper():
        print("world")
        func()
    
    return wrapper
    
@decorator_hello
@decorator_world
def more_greetings():
    print("everyone")


more_greetings()
```

    hello
    world
    everyone

Please keep in mind that decorators get executed from **top to down** when you compose them.

### Why should I use `functools.wraps`?

We already established that a decorator takes a function and returns a function.
Furthermore, we know that the input and output function have the same signature (the take the same parameters and have the same return value).

But caveat: **they are not the same**

Let me demonstrate this with a little quiz.

What is the output of this print line?

```python
def fancy_decorator(func):
    
    def wrapper():
        return func()
    
    return wrapper

@fancy_decorator
def simple_function():
    pass
```

And here is our result.


```python
print(simple_function.__name__)
```

    wrapper

I guess if you think for a moment, you come to the conclusion that the result is `wrapper` because our decorator returns the `wrapper` function object and not the passed reference to `simple_function`.

But you have to see this also from the perspective of the caller of `simple_function`.
The caller does not know or care about the implementation details of `simple_function`.
Thus, it might really set the him off to find out that the `simple_function` references a function object with the name `wrapper`.

You might say now 
"come on Dennis, it is just a function name why do you even worry?".

But what if i tell you that we can use the function object to store state?
That would be really useful since we have access to the function from within our decorator.

Have a look at this example.

### Handle return values in decorators

### TODO

Includes:

* Python objects are first-class citizens
=> everything is a python object
=> higher procedures; pass function objects as function arguments 
=> method objects are mutable

* Decorators are functions that take a function as a parameter
=> @my_decorator is syntactic sugar for my_decorator(my_func)
=> basic decorator example; how to write the simple function decorator
=> how to combine multiple decorators; example with annotation and manual composition

* In-depth function decorator
=> decorator returns wrapper function
=> what and why @func.wraps
=> *args, **kwargs in decorator; basic example can't have method arguments
=> function decorator with parameters
=> persist in function object state
=> generator decorator
=> validation decorator; index-decorator - validate certain index - parameter; key-word decorator - validate certain keyword parameter
=> middleware decorator; logging decorator; access function.__name__
=> register decorator; annotated code registers at singleton data structure

* In-depth class decorator
=> motivation; easier state management; 
=> basic example; explain __init__ and __call__
=> explain decorator state
=> transfer example middleware decorator
=> transfer example validator decorator
=> transfer example register decorator

* Decorator Use Cases
=> Serialize parameter to JSON output
=> Endpoint logging
=> Validation
=> Error Handling
=> Caching
=> Singleton