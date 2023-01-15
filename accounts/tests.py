from django.urls import reverse 
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from datetime import date

User = get_user_model()

class RegisterLoginTest(TestCase):
    """
    Contains two tests: `test_inactive_user_login` and `test_user_login`. \n
    First expects an error to be shown on the `login` page after an attempt to log in as inactive user,
    second test is created in order to check if `LoginFormView` works properly
    """
    def setUp(self):
        self.user1 = User.objects.create(
            email='test123@test.com',
            password='testpassword123321',
            first_name='Test',
            last_name='User1',
            town='Testvania',
            birth_date=date(year=2005, month=1, day=15),
            )
        self.user1.is_active = True
        self.client = Client()
    
    def test_inactive_user_login(self):
        """
        Signing up new user and trying to log in with his credentials. Expected the `error.message` appear on the
        login page, as the user is inactive (has unconfirmed/non-activated email).

        So, here we test the `RegisterFormView` (via creating new user and asserting the `User.objects.all().count()` 
        with value `2`), and test `LoginFormView` throw out error when inactive user provides its credentials.
        """
        testuser_password = 'testpass123321'
        self.client.post(
            path=reverse('register'),
            data={
                'email' : 'test2@test.com',
                'first_name' : 'Test',
                'last_name' : 'User2',
                'password1' : testuser_password,
                'password2' : testuser_password,
                'town' : 'Test-Angeles',
                'birth_date' : date(year=2002, month=11, day=11)
            }
        )
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

        response = self.client.post(
            path=reverse('login'),
            data={
                'username':'test2@test.com',
                'password' : testuser_password
            }
        )
        self.assertContains(
            response=response, 
            text=b'Please enter a correct email and password. Note that both fields may be case-sensitive.',
            )
        
    def test_user_login(self):
        """
        Creation superuser in order to test the `LoginFormView`. Check the access to `login` page for
        unauthenticated requests. 
        """
        User.objects.create_superuser('myuser@test.com', first_name='Test', last_name='SuperUser', password='testpass123')
        access = self.client.get(reverse('login'))
        self.assertContains(access, b'Sign in')
        self.client.post(
            path=reverse('login'),
            data={
                'username':'myuser@test.com',
                'password':'testpass123'
            },
        )
        response = self.client.get(reverse('edit_profile'))
        self.assertContains(response, b'SuperUser')

class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser('superuser@test.com', 'password123321', first_name='Test')

    def test_answer_list(self):
        response_unauth = self.client.get(reverse('answers-by-user', kwargs={'profile_id' : self.superuser.pk}))
        self.assertContains(
            response=response_unauth,
            text=b'Maybe your exact question will be the first for Test to be answered!')
            #i'll work on this later
    

        

