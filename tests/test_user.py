import unittest
from mediaServer.user import User
from mediaServer.userconfig import Configuration
from mediaServer.userpolicy import Policy

class UserTestCase(unittest.TestCase):
    def test_user(self):
        testUser = User()
        self.assertIsInstance(testUser, User)
        self.assertIsInstance(testUser.Configuration, Configuration)
        self.assertIsInstance(testUser.Policy, Policy)

    def test_logout(self):
        #unit test completed within test_server
        pass

    def test_delete(self):
        #unit test completed within test_server
        pass

    def test_authenticate(self):
        #unit test completed within test_server
        pass

    def test_updatepassword(self):
        #unit test completed within test_server
        pass