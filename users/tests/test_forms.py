from users.forms import RegisterForm
from django.test import TestCase


class FormTest(TestCase):

    def setUp(self) -> None:
        self.form = RegisterForm

    def test_valid_form(self):
        valid_data = {
             "email": "user@email.com",
            'password1': "Test123@",
            'password2': "Test123@",
        }
        self.assertTrue(self.form(data=valid_data).is_valid())  

    def test_no_email_invalid_form(self):
        invalid_data = {
            "email": "",
            'password1': "Test123@",
            'password2': "Test123@",
        }

        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error)   
        self.assertEqual(form.fields['email'].error_messages['required'], "This field is required.")


    def test_bad_email_format(self):
        
        invalid_data = {
            "email": "test",
            'password1': "Test123@",
            'password2': "Test123@",
        }

        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error)   
        self.assertEqual(form.errors['email'].as_text(), "* Enter a valid email address.")

    def test_no_password(self):
        invalid_data = {
            "email": "test@email.com",
            'password1': "",
            'password2': ""
        }

        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error)   
        self.assertEqual(form.errors['password1'].as_text(), "* This field is required.")
        self.assertEqual(form.errors['password2'].as_text(), "* This field is required.")
       

    def test_confirm_password(self):
        invalid_data = {
            "email": "test@email.com",
            'password1': "Test123@",
            'password2': "Test12",
        }

        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error)   
        self.assertEqual(form.errors['password2'].as_text(), '* The two password fields didn’t match.')


    def test_validate_password(self):
        invalid_data = {
            "email": "test@email.com",
            'password1': "test",
            'password2': "test",
        }

        form = self.form(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error)        
        
    
