from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import User
from core.models import Question, Answer


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

    def test_answer_create(self):
        """
        Testing the creation of answer with posted form-data. Testing of `add_like(request.user)`
        method (like creation and like removal) 
        """

        self.client.force_login(self.user2)
        response = self.client.post(    #Creating an answer with pk=1 via POST form
            path = reverse('quest_detail', kwargs={'index' : self.question.pk}),
            data = {'body' : 'answer test body 1'},
            )
        self.assertNotIn(b'Form message error', response.content)

        answer = Answer.objects.get(pk=1)
        self.client.post(   # Like an answer
            path=reverse('like_answer'),
            data={'answer_id' : 1, 'url' : reverse('home')}
        )
        self.assertEqual(answer.likes_count(), 1)
        self.client.post(   #Remove like from the answer
            path=reverse('like_answer'),
            data={'answer_id' : 1, 'url' : reverse('home')}
        )
        self.assertEqual(answer.likes_count(), 0)
        
    def test_unauth_like(self):
        """
        Attempting to create like-instance with no user authenticated. Check, whether `message.ERROR, 
        'Sign in to like answers'` message is shown on the `home` and `detail` page.
        """
        answer = Answer.objects.create(
            author = self.question.adressant,
            question = self.question,
            body = 'test answer body 1'
        )
        self.client.post(   #Like answer from home page
            path=reverse('like_answer'),
            data={'answer_id' : answer.pk, 'url' : reverse('home')}
        )
        response_home = self.client.get('/')    #Manually redirecting to the home page
        self.assertIn(b'Sign in to like answers', response_home.content)
        #Check if error message disappears after being shown once
        response_home_repeat = self.client.get('/')
        self.assertNotIn(b'Sign in to like answers', response_home_repeat.content)

        #Same procedure from answer detail page
        answer_detail_page = reverse('quest_detail', kwargs={'index' : answer.question.pk})
        self.client.post(   
            path=reverse('like_answer'),
            data={'answer_id' : answer.pk, 'url' : answer_detail_page}
        )
        response_detail = self.client.get(answer_detail_page)
        self.assertIn(b'Sign in to like answers', response_detail.content)

        response_detail_repeat = self.client.get(answer_detail_page)
        self.assertNotIn(b'Sign in to like answers', response_detail_repeat.content)

    def test_question_create(self):
        """
        Consists of two parts: 
        1. Check whether `You must sign in to ask a question` message is shown when we try to visit 
        `quest_create` page with no user authenticated
        2. Authencticating as one of the test users and asking a question to another test user.
        """
        #first part: unauth
        question_create_page = reverse('quest_create', kwargs={'adressant_id' : self.user1.pk})
        response_unauth = self.client.get(question_create_page)
        self.assertContains(response_unauth, b'You must sign in to ask a question', status_code=404)

        #second part: question creation
        self.client.force_login(self.user2)
        question_body = 'Test question body id2'
        self.client.post(
            path=question_create_page,
            data={'body' : question_body}
        )
        new_question = Question.objects.get(body=question_body)
        response_created = self.client.get(reverse('quest_detail', kwargs={'index' : new_question.pk}))
        self.assertContains(
            response=response_created,
            text=question_body,
            status_code=200
        )
