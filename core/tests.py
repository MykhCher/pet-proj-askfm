from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from core.models import Question


class QuestionCreateTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(email='test1@test.com',
                                    password='test123', 
                                    first_name='Test', 
                                    last_name='User1')
        self.user2 = User.objects.create(email='test2@test.com',
                                    password='test123', 
                                    first_name='Test', 
                                    last_name='User2')

        self.client = Client()
        self.question = Question.objects.create(author=self.user1,
                                                adressant=self.user2,
                                                body='test question body')

    def test_create_question(self):
        question_id = self.question.pk
        self.client.force_login(self.user2)
        url = reverse('quest_detail', kwargs={'index': question_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_question_create_un_auth(self):
        url = reverse('quest_create', kwargs={'adressant_id': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_question_list_auth(self):
        self.client.force_login(self.user1)
        url = reverse('quest_list', kwargs={'profile_id': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_question_list_un_auth(self):
        url = reverse('quest_list', kwargs={'profile_id': self.user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
