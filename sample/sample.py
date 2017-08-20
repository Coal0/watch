from context import Session


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
        Creates a new session based on `access_level` and starts it.
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
        This requires the session to be alive.
        
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
        Requires the session to be alive.
        
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
        Requires the session to be alive.
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
