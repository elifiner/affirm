affirm
======

This small library improves Python `assert` error messages to contain more useful information.

I like to use `assert`'s liberaly thoughout my code to document my assumptions and when one of them fails, I really like to know as much as possible about what failed and why.

Using the `assert` statement
----------------------------

Before affirm, if you run a simple script in Python:

    a = 1
    b = 2
    assert a > b

The result will be:

    Traceback (most recent call last):
      File "test.py", line 3, in <module>
        assert a > b
    AssertionError

We can see the traceback, but not the actuall values that caused the assert to fail, which is not very useful for debugging.

If you `import affirm` at the top of the script, like so:

    import affirm
    a = 1
    b = 2
    assert a > b

You'll get:

    Traceback (most recent call last):
      File "test.py", line 4, in <module>
        assert a > b
    AssertionError: assertion (a > b) failed with a=1, b=2

Which is much more useful.

Note that the standard behaviour of supplying a message with the assert statement still works:

    import affirm
    a = 1
    b = 2
    assert a > b, "something went wrong"

Will give you:

    Traceback (most recent call last):
      File "test.py", line 4, in <module>
        assert a > b
    AssertionError: something went wrong

Using the `affirm` function
---------------------------

There's only one problem with using the standard `assert` statement. If you catch the exception and print it yourself:

    import affirm
    a = 1
    b = 2
    try:
        assert a > b
    except Exception as e:
        print(str(e))

The result will be:

```
```

Yes, absolutely nothing. Calling `str` on `AssertionError` results in an empty string.

If you want to be able to catch the assertion errors and print the messages into e.g. log, you'll need to use the `affirm` function instead of the `assert` statement, like so:

    from affirm import affirm
    a = 1
    b = 2
    try:
        affirm(a > b)
    except Exception as e:
        print(str(e))

Now we get the expected:

    assertion (a > b) failed with a=1, b=2
