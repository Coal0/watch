# Guide

### Abstract
To restrict access to data based on time, we can use 'sessions'.<br />
A session comes in any of three states:

* A session is *disabled*: it has not yet been started, but it has been initialized
* A session is *alive*: it has been initialized and started and it hasn't yet expired
* A session has *expired*: it has been initialized, started and it has been alive for a predefined period of time.

We call this predefined period of time a session's 'duration' and it is expressed in seconds.<br />
This guide will focus on getting you started with sessions by:

1. Providing abstract code snippets and explaining them; 
2. Providing a real-world example of sessions.
<br />

### Abstract | Code
This module treats each session as a seperate `Session` class.<br />
Each instance of this class can have a different duration and each behaves independently from one another.<br />
If you need two sessions (e.g. one for administrators and one for users), you need to define both as seperate objects.<br />

Sessions can run alongside your code, or as part of a class by subclassing `Session`.<br />
Both cases are equally valid, but one may fit your project's style better than the other.<br />

Code in this guide will be written to work in Python 3, but with little changes it should be compatible with Python 2 as well.<br />

**This particular implementation of sessions does *not* periodically check if a session has expired.**

<br />

### Abstract | Use cases
Sessions can be used for restricting access to files, databases, storage devices, websites and any platforms. This guide will end with a 'real-world' use case for sessions. Note that the examples in this guide will not necessarily enforce best practices. They serve as a demonstration only.<br />
<br />

### Usage | Side flow
To create a session, first import the `Session` class from `session.py`:

```python
from session import Session
```

Session's constructor only takes one argument; `session_duration`.<br />
As discussed above, this parameter will describe the length of the sessions' life.<br />
It is formally an integer, but a float may be passed as well if precision is crucial:

```python
foo = Session(10)
bar = Session(0.5)
```

###### NOTE: sessions don't start when initialized, they must be explicitly started. This allows for dynamic start / expire cycles and makes sessions reusable.

`foo` and `bar` will, respectively, when started, be alive for 10 and .5 seconds.<br />
To start a session, its `start_session` method must be called:

```python
session = Session(10)
session.start_session()
```

As soon as a session is started, it is marked as 'alive'. To check the status of a session, use the `has_expired` property:

```python
import time
from session import Session

session = Session(10)
session.start_session()

session.has_expired   # False
time.sleep(10)
session.has_expired   # True
```

Calling `has_expired` on a session that hasn't been started yet will raise a `ValueError`!<br />
In case you need to manually expire a session, use `expire_session`:

```python
from session import Session

session = Session(10)
session.start_session()

session.has_expired   # False
session.expire_session()
session.has_expired   # True
```

---
    
As you can imagine, functions that require the session to be alive could check `has_expired` each time they're called.<br />
A predefined method for this is `require_session`. You can call it to check if the session is alive:

```python
>>> from session import Session
>>>
>>> session = Session(10)
>>>
>>> session.start_session()
>>> session.require_session()
>>>
>>> session.expire_session()
>>> session.require_session()
Traceback (most recent call last):
...
ValueError: session expired 0 seconds ago
```

As you can see, when a session has expired and `require_session` is called, a `ValueError` is raised telling you how long ago
the session expired.<br />

If you want to know how much longer a session will be alive for, or how much time has passed since the session expired, you can check respectively `time_until_expiry` and `time_since_expiry`:

```python
import time
from session import Session
    
session = Session(10)
session.start_session()
    
session.time_until_expiry   # 10
time.sleep(5)
session.time_until_expiry   # 5
time.sleep(5)
session.time_since_expiry   # 0
time.sleep(5)
session.time_since_expiry   # 5
```

###### NOTE: calling `time_until_expiry` on a session that has already expired will return `0` and `time_since_expiry` for a session that hasn't yet expired will also return `0`. If you need to check *if* a session has expired, use `has_expired`, which just returns a boolean value.

This concludes the 'quickstart' introduction to this module.

<br />

### Usage | OOP
###### NOTE: the following sections assumes you are familiar with the basics of the `Session` class. If this is not the case, refer to the above section 'Usage | Side flow'.

To conform to OOP principles, you can make a class inherit from `Session` and reference `self` as `Session` object.<br />
This may be more straightforward if you're implementing a class which depends on a session:

```python
from session import Session


class Foo(Session):
    def __init__(self):
        """Constructor.
        Define a new session with a duration of 30 minutes.
        """
        super().__init__(1800)
        # Session duration = 30 minutes
    
    def start(self):
        """Start the session and authenticate the user.
        """
        self.start_session()
    
    def expire(self):
        """Expire the session and deauthenticate the user.
        """
        self.expire_session()
        
    def bar(self):
        """A method that can only be called by an authenticated user.
        """
        self.require_session()
        print("bar!")
```

And sample usage:

```python
>>> foo = Foo()
>>> 
>>> foo.bar()
Traceback (most recent call last):
...
ValueError: session has not been started yet
>>> foo.start()
>>> foo.bar()
bar!
>>> foo.expire()
>>> foo.bar()
Traceback (most recent call last):
...
ValueError: session expired 1 seconds ago
```

<br />

### Examples | Database
The following is a setup for a database which can be accessed at two levels: `user` level and `admin` level.<br />
A `user` can only view the database and an `admin` can view and modify the database.<br />

```python
from session import Session


class Database(Session):
    """A class representing a database connection.
    Constants defined here:
    
    USER_SESSION_LENGTH: The duration of a user's session in seconds.
                         Users have to reauthenticate every 1800
                         seconds (every half hour).
    ADMIN_SESSION_LENGTH: The duration of an admin's session in seconds.
                          Admins have deeper access to the database and
                          must reauthenticate every 900 seconds (every
                          15 minutes).
    """
    _USER_SESSION_LENGTH = 1800 
    _ADMIN_SESSION_LENGTH = 900

    def __init__(self, access_level: str, database_path: str) -> None:
        """Constructor.
        Create a new session based on `access_level` and start it.
        Loads the database into a dictionary object.
        
        Arguments:
        * access_level: Either 'user' or 'admin', the clearance level
                        for whoever is accessing the database.
        * database_path: The path to the database.
        """
        self._login(access_level=access_level)
        self._database = self._load(database_path=database_path)
        self._access_level = access_level
        self._database_path = database_path
    
    def _login(self, access_level: str) -> None:
        """Define a new session with a duration depending on `access_level`
        and start the session.
        
        Arguments:
        * access_level: Either 'user' or 'admin', the clearance level
                        for whoever is accessing the database.
        
        Raises:
        * ValueError if `access_level` is not 'user' or 'admin'.
        """
        if access_level == "user":
            super().__init__(session_duration=self._USER_SESSION_LENGTH)
        elif access_level == "admin":
            super().__init__(session_duration=self._ADMIN_SESSION_LENGTH)
        else:
            raise ValueError("Invalid access level: {level}".format(
                level=access_level
            ))
        self.start_session()
    
    def _load(self, database_path: str, flush: bool=False) -> dict:
        """Load the database into memory as a dictionary.
        This requires the session to be alive. If it is not, reauthenticate.
        
        Arguments:
        * database_path: The path to the database file
        * flush: Set this to True if you want to forcefully reload the database.
                 If set to False, a cached database will be returned if available.
        """
        try:
            self.require_session()
        except ValueError:
            print("Your session has expired. Please login again.")
            return
        try:
            self._database
        except AttributeError:
            pass
        else:
            if not flush:
                return
        database = {}
        with open(database_path) as f:
            database_lines = f.readlines()
            for line in database_lines:
                key, value = line.split(":")
                # Assuming the database is set up like this
                database[key] = value.strip()
        return database
    
    def view(self, key: str) -> str:
        """View a key in the database.
        If `key` does not exist in the database, return "Key does not exist.".
        Requires the session to be alive. If it is not, reauthenticate.
        
        Arguments:
        * key: The key to be accessed (as database.get(key))
        
        Returns:
        * database.get(key, "Key does not exist.")
        """
        try:
            self.require_session()
        except ValueError:
            print("Your session has expired. Please login again.")
            return
        return self._database.get(key, "Key does not exist")
        
    def modify(self, key: str, value: str) -> None:
        """Modify a key in the database.
        Requires the session to be alive. If it is not, reauthenticate.
        Requires 'admin' access level.
        
        Arguments:
        * key: The key to be modified
        * value: The new value of the key (database[key] = value)
        
        Raises:
        * PermissionError if access level is 'user', not 'admin'.
        """
        try:
            self.require_session()
        except ValueError:
            print("Your session has expired. Please login again.")
            return
        if self._access_level != "admin":
            raise PermissionError("Only admins can modify the database.")
        self._database[key] = value
        
    def logout(self) -> None:
        """Deauthenticate whoever is accessing the database.
        """
        self.expire_session()
        with open(self._database_path, "w") as f:
            for key in self._database:
                f.write(key)
                f.write(":")
                f.write(self._database[key])
```

###### NOTE: The above example skips over a lot of security principles. In a real world application, the database would require registered users to enter their username / password combination and the actual database interactions would be obscured. Reauthentication as implemented in this example is insecure. However, the purpose of time-based sessions in such an application still holds.

You can play around with this example [here](https://github.com/Coal0/watch/tree/master/sample). Note that it is compatible with Python 3 only.
