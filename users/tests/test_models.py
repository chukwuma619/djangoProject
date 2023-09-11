from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class TestUserCreation(TestCase):
    def setUp(self) -> None:
        # Create two user: normal user and Superuser
        User.objects.create_user(email="testuser@email.com",
                            password="foo")

        User.objects.create_superuser(email="superuser@email.com",
                            password="foo",)

    def test_create_user(self):
        """
        This checks for all possible error
        that might occur during user creation
        """
        user = User.objects.get(email="testuser@email.com")
        self.assertEqual(user.email, "testuser@email.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # username does not exist
        try:
            self.assertIsNone(user.username)

        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create_user()

        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_superuser(self):
        """
        This test checks for all possible error
        that might occur during superuser creation
        """
        user = User.objects.get(email="superuser@email.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

        # username does not exist
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='super@email.com', password="foo", is_superuser=False)
