from django.test import TestCase
from django.urls import reverse
from Pyfhel import Pyfhel
# Create your tests here.
from django.contrib.auth import get_user_model
from bankingApp.models import *
from datetime import datetime
from django.http import Http404
from django.core.exceptions import ValidationError


class Login(TestCase):
    def setUp(self):
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass")

    def test_login_success(self):
        response = self.client.post("/login/", data={
            "username": "testuser",
            "password": "testpass"
        })
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 302)
        # Check if user is authenticated
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(
            response, "http://127.0.0.1:5173/", fetch_redirect_response=False)

    def test_login_fail(self):
        response = self.client.post("/login/", data={
            "username": "testuser",
            "password": "abcde"
        })

        self.assertEqual(response.status_code, 200)
        # Check if user is authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class Register(TestCase):

    def test_register_success(self):
        User = get_user_model()
        response = self.client.post(reverse("register"), data={
            "first_name": "test",
            "last_name": "tests",
            "username": "testuser",
            "email": "test@example.com",
            "password1": "Random345",
            "password2": "Random345"
        })
        # Check that the response status code is 302
        self.assertEqual(response.status_code, 302)
        # Check that the user is created and authenticated
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        # Check that the response redirects to the success page
        self.assertRedirects(
            response, "http://127.0.0.1:5173/", fetch_redirect_response=False)

    def test_register_fail(self):
        User = get_user_model()
        response = self.client.post(reverse("register"), data={
            "first_name": "test",
            "last_name": "tests",
            "username": "testuser",
            "email": "test@example.com",  # invalid email format
            "password1": "Random3456",
            "password2": "Random345"
        })
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class Account(TestCase):
    def setUp(self):
        # Create a user for testing
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpass", balance=b"")

    def test_withdraw_success(self):
        response = self.client.post("/login/", data={
            "username": "testuser",
            "password": "testpass"
        })
    #    response = self.client.post(reverse('transaction_api',kwargs={'userID': 1}), data={'amount': 0, 'type': 'w','desc':"",'date':})
        # Get the current date and time
        date_obj = datetime.now()
        # Get a string representation in ISO 8601 format
        date_string = date_obj.isoformat()
        # Replace the 'T' character with a space
        date_string = date_string.replace('T', ' ')
    #    response = self.client.post(reverse('transaction_api', kwargs={'userID': 1}),json={'amount': 12.50, 'type':'D','desc':'','date':date_string},content_type='application/json')
        response = self.client.post(reverse('transaction_api', kwargs={
                                    'userID': 1}), content_type='application/json', data=json.dumps({'amount': 0, 'type': 'D', 'date': date_string}))
        HE = Pyfhel()  # Create a Pyfhel object
        # Load context from file
        HE.load_context(
            "C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/context")
        # Load context from file
        HE.load_public_key(
            "C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/public.key")
        # Load context from file
        HE.load_secret_key(
            "C:/Users/ritik/OneDrive/Documents/University Computer Science/Year 3/Project/Project Code/bankingApp/secret.key")

        self.assertEqual(response.status_code, 200)
        # Check if the account balance is updated correctly
        self.user.refresh_from_db()
        val = pickle.loads(self.user.balance)
        val = (HE.decryptInt(val)/100)[0]
        self.assertEqual(val, 0)

    def test_withdraw_fail(self):
        response = self.client.post("/login/", data={
            "username": "testuser",
            "password": "testpass"
        })
        # Get the current date and time
        with self.assertRaisesMessage(ValidationError, 'Amount cannot be negative'):

            date_obj = datetime.now()
            # Get a string representation in ISO 8601 format
            date_string = date_obj.isoformat()
            # Replace the 'T' character with a space
            date_string = date_string.replace('T', ' ')
            response = self.client.post(reverse('transaction_api', kwargs={
                                        'userID': 1}), content_type='application/json', data=json.dumps({'amount': "-10", 'type': 'D', 'date': date_string}))
       
        # Check if the account balance is updated correctly
        self.user.refresh_from_db()

        self.assertEqual(self.user.balance,b"")

    def test_deposit(self):
        pass

    def test_transfer(self):
        pass
