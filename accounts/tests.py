from django.urls import reverse 
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from datetime import date

User = get_user_model()

class RegisterLoginTest(TestCase):
    """
    Contains three tests: `test_inactive_user_login`, `test_logout` and `test_user_login`. \n
    First expects an error to be shown on the `login` page after an attempt to log in as inactive user,
    second and third tests are created in order to check if `LogoutView` and `LoginFormView` viewws work properly
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

    def test_logout(self):
        """
        Check the content of header dropdown: in first case we should get current username, in the second case 
        we should get the "Login" text, as we called `LogoutView`
        """
        self.client.force_login(self.user1)
        home_auth = self.client.get(reverse("home"))
        username = bytes(self.user1.first_name, encoding="UTF-8")
        self.assertContains(
            response=home_auth,
            text=username
        )

        self.client.get(reverse("logout"))
        home_unauth = self.client.get(reverse("home"))
        self.assertContains(
            response=home_unauth,
            text=b"Login"
        )

class ProfileViewsTest(TestCase):
    """
    Contains tests of all `/accounts` views and urls.
    """
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser('superuser@test.com', 'password123321', first_name='Test')
        self.client.force_login(self.superuser)

    def test_answer_list(self):
        """
        Check the message shown on the `answers-by-user` page when no answers given by user.
        """
        
        response_auth = self.client.get(reverse('answers-by-user', kwargs={'profile_id' : self.superuser.pk}))
        self.assertContains(
            response=response_auth,
            text=b'Maybe you want to check out whether someone asked you some important question')
            
        self.client.logout()
        response_unauth = self.client.get(reverse('answers-by-user', kwargs={'profile_id' : self.superuser.pk}))
        self.assertContains(
            response=response_unauth,
            text=b'Maybe your exact question will be the first for Test to be answered!')
    
    
    def test_profile_page(self):
        """
        Check whether the button on the `check-profile` page is changed from "Edit profile" while `request.user.id`
        is identical to `profile_id`, to the "Ask a question to `self.superuser.first_name`" otherwise  
        """

        uid = self.superuser.id
        text_unath = "Ask a question to %s" % self.superuser.first_name
        text_content_unauth = bytes(text_unath, encoding="UTF-8")
        text_content = bytes("Edit profile", encoding="UTF-8")

        response_auth = self.client.get(reverse("check_profile", kwargs={"profile_id": uid}))
        self.assertContains(
            response=response_auth,
            text=text_content
        )

        self.client.logout()
        response_unauth = self.client.get(reverse("check_profile", kwargs={"profile_id": uid}))
        self.assertContains(
            response=response_unauth,
            text=text_content_unauth
        )

    def test_edit_profile(self):
        """
        Changing `self.superuser` info via `EditProfileView`, check if data is updated. Check if `404` status code
        is set after requesting with no user authenticed
        """

        uid = self.superuser.id
        self.client.post(
            path=reverse("edit_profile"),
            data={
                "first_name" : "Kevin",
                "last_name" : "Kavinsky",
                "town" : "Catsburg",
                "birth_date" : date(year=2005, month=1, day=30)
            }
        )
        profile_page = self.client.get(reverse("check_profile", kwargs={"profile_id" : uid}))

        self.assertContains(profile_page, b"First name: Kevin")
        self.assertContains(profile_page, b"Last name: Kavinsky")
        self.assertContains(profile_page, b"Occupation: Catsburg")
        self.assertContains(profile_page, b"Birth date: Jan. 30, 2005")

        self.client.logout()
        error_page = self.client.get(reverse("edit_profile"))
        self.assertEqual(error_page.status_code, 404)
