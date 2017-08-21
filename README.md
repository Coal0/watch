# watch ![watch icon](https://cdn0.iconfinder.com/data/icons/sport-2-android-l-lollipop-icon-pack/24/stopwatch-24.png "Logo Title Text 1")
Time-based sessions in Python 2 and 3

---

Using watch, it's easy to restrict access to sensitive databases and files.<br />
Watch is compatible with Python 2 and 3 and has been tested on Python 2.7.1 as well as Python 3.6.0.<br />
To get started with watch, check out [the guide](https://github.com/Coal0/watch/blob/master/guide.md).

<br />

### Testing
It's easy to test watch by running `test.py` [here](https://github.com/Coal0/watch/tree/master/tests).<br />
The tests should support Python 2 and 3.

<br />

### Bug reports

Watch is a newly released project. If you have any questions or remarks, please [open a new issue](https://github.com/Coal0/watch/issues/new).<br />

All bug reports must follow this format:

* **Name**: a relevant name which summarizes the problem
* **Date**: when did you first encounter the bug?
* **Topic**: pick any of "documentation error", "Python exception", "security problem", "other"
* **Project version**: what version of watch were you using when you encountered the bug? [\*]
* **Python version**: what version of Python were you using when you encountered the bug? [\*]
* **Cause**: what were you doing before you encountered the bug? What triggered the bug? [\*]
* **Problem**: paste the entire exception traceback or describe the problem.
* **Reproduction**: which steps must someone take to reproduce the bug? [\*]

[\*] May be left blank if the topic is "documentation error" or "security problem"

---

Example bug report:

* **Name**: `ValueError` raised when trying to access `has_expired`
* **Date**: 20th of August, 2017
* **Topic**: Python exception
* **Project version**: 1.0.0
* **Python version**: 3.6.0
* **Cause**: Accessing the `has_expired` property of a Session instance raises a `ValueError`.
* **Problem**:

```
Traceback (most recent call last):
  ...
ValueError: session has not been started yet
```

###### META: Omitted unrelated information for readability. Normal bug reports should not do this.

* **Reproduction**: Create a new `session.Session` class, and call its `has_expired` property

