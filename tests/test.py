import time
import unittest

from context import Session


class TestSession(unittest.TestCase):
    def test_setup(self):
        session = Session(5)
        with self.assertRaises(ValueError):
            session.has_expired
        session.start_session()
        self.assertFalse(session.has_expired)
        self.assertEqual(session.time_since_expiry, 0)
        time.sleep(5)
        self.assertTrue(session.has_expired)
        session.expire_session()

    def test_flow(self):
        session = Session(5)

        def permissive_function():
            session.require_session()

        session.start_session()
        permissive_function()
        time.sleep(5)
        session.expire_session()
        with self.assertRaises(ValueError):
            permissive_function()
        session.start_session()
        permissive_function()
    
    def test_flow_values(self):
        session = Session(5)
        session.start_session()
        self.assertTrue(3.5 <= session.time_until_expiry <= 5)
        time.sleep(6)
        self.assertGreaterEqual(session.time_since_expiry, 1)

    def test_inheritance(self):
        class PermissiveClass(Session, object):
            def __init__(self):
                super(PermissiveClass, self).__init__(10)
            
            def _start(self):
                self.start_session()

            def _permissive_function(self):
                self.require_session()

            def _stop(self):
                self.expire_session()

        permissive_class = PermissiveClass()
        with self.assertRaises(ValueError):
            permissive_class.has_expired
        permissive_class._start()
        permissive_class._permissive_function()
        permissive_class._stop()
        with self.assertRaises(ValueError):
            permissive_class._permissive_function()

if __name__ == "__main__":
    unittest.main()
