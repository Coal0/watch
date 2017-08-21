import time


class Session:
    """Class representing a session.
    Methods:
    * __init__(): Set the session length (in seconds)
    * start_session(): Start the session
    * expire_session(): Expire the session
    * require_session(): Require the session to be alive

    Properties:
    * has_expired: Check if the session has expired
    * time_until_expiry: Time until expiry
    * time_since_expiry: Time since expiry
    """

    def __init__(self, session_duration):
        """Constructor.
        Set an initial session duration. Note that the session
        still needs to be started using start_session().

        Arguments:
        * session_duration: integer representing the length of
          The session in seconds.

        Example:
        >>> session = Session(session_duration=60)
        >>> # When started, the session will expire after 60 seconds
        """
        self._session_duration = session_duration
    
    def start_session(self):
        """Start the session.
        This method can be called multiple times, to restart the
        session.

        Example:
        >>> session = Session(session_duration=60)
        >>> session.start_session()
        >>> <activity here>

        Returns None
        """
        self._session_expiry = time.time() + self._session_duration

    def expire_session(self):
        """Expire the session.

        Example:
        >>> session = Session(session_duration=60)
        >>> <login>
        >>> session.start_session()
        >>> <activity here>
        >>> <logout>
        >>> session.expire_session()

        Returns None
        """
        self._session_expiry = time.time()

    @property
    def has_expired(self):
        """Check if the session has expired.

        Example:
        >>> session = Session(session_duration=60)
        >>> <login>
        >>> session.start_session()
        >>> while True:
        ...     if not session.has_expired:
        ...         <activity here>
        ...     else:
        ...         <logout>
        
        Raises:
        * ValueError if the session hasn't been started before

        Returns True if the session has expired, else False
        """
        try:
            return time.time() > self._session_expiry
        except AttributeError:
            raise ValueError("session has not been started yet")

    @property
    def time_until_expiry(self):
        """Return the time until the session expires, in seconds.
        
        Example:
        >>> session = Session(session_duration=60)
        >>> <login>
        >>> session.start_session()
        >>> while True:
        ...     if not session.has_expired:
        ...         <activity here>
        ...         print("Time left:", session.time_until_expiry)
        ...     else:
        ...         <logout>

        Returns <expiry> - <current time> if the session hasn't expired
        yet, else 0. Both are returned as strings.
        """
        if self.has_expired:
            return 0
        return int(self._session_expiry - time.time())

    @property
    def time_since_expiry(self):
        """Return the time since the session expired, in seconds.

        Example:
        >>> session = Session(session_duration=60)
        >>> <login>
        >>> session.start_session()
        >>> while True:
        ...     if not session.has_expired:
        ...         <activity here>
        ...     else:
        ...         <logout>
        >>> <activity here>
        >>> print("Expired", session.time_since_expiry, "seconds ago")

        Returns <current time> - <expiry> if the session hasn't expired
        yet, else 0.
        """
        if not self.has_expired:
            return 0
        return int(time.time() - self._session_expiry)

    def require_session(self):
        """Require the session to be alive.

        Example:
        >>> session = Session(session_duration=60)
        >>> <login>
        >>> session.start_session()
        >>> def permissive_action():
        ...     session.require_session()
        ...     <activity here>

        Raises:
        * ValueError if the session has expired

        Returns None
        """ 
        if self.has_expired:
            raise ValueError("session expired {} seconds ago".format(
                self.time_since_expiry
            ))
