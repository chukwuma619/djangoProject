from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterViewTest(TestCase):

    def setUp(self) -> None:
        self.client = Client(enforce_csrf_checks=True)


    def test_user_registration_with_csrf(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Get CSRF Token from the response token
        csrf_token = response.cookies['csrftoken'].value

        registration_data = {
            "email": "test@email.com",
            'password1': "Test123@",
            'password2': "Test123@",
            'csrfmiddlewaretoken': csrf_token,
        }

        # Simulate a POST request with registration data with CSRF Token
        response = self.client.post(reverse('register'), data=registration_data)
        self.assertRedirects(response, reverse('login'))





    def test_user_registration_without_csrf(self):
        registration_data = {
            "email": "test@email.com",
            'password1': "Test123@",
            'password2': "Test123@",
        }

        # Simulate a POST request with registration data without CSRF Token
        response = self.client.post(reverse('register'), data=registration_data)
        self.assertEqual(response.status_code, 403)


class LoginViewTest(TestCase):

    def setUp(self) -> None:
        self.client = Client(enforce_csrf_checks=True)
        # Create a User Instance
        User.objects.create_user(
            email="test@email.com",
            password="Test123@",
        )

    def test_user_login_with_csrf(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Get CSRF Token from the response token
        csrf_token = response.cookies['csrftoken'].value

        login_data = {
            "username": "test@email.com",
            'password': "Test123@",
            'csrfmiddlewaretoken': csrf_token,
        }

        # Simulate a POST request with login data with CSRF Token
        response = self.client.post(reverse('login'), data=login_data)
        self.assertRedirects(response, reverse('secret'))  # Expect a redirect

    def test_user_login_without_csrf(self):
        login_data = {
            "email": "test@email.com",
            'password': "Test123@",
        }
        # Simulate a POST request with registration data without CSRF Token
        response = self.client.post(reverse("login"), data=login_data)
        self.assertEqual(response.status_code, 403)



class ProtectedViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        User.objects.create_user(
            email="test@email.com",
            password="Test123@",
        )

    def test_protected_page_require_login(self):
        response = self.client.get(reverse('secret'))
        self.assertRedirects(response, expected_url=f'{reverse("login")}?next={reverse("secret")}')

    def test_protected_page_after_login(self):
        user = User.objects.get(email="test@email.com")
        self.client.login(email="test@email.com",
            password="Test123@")
        response = self.client.get(reverse('secret'))
        self.assertEqual(response.status_code, 200)
