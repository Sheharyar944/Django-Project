from django.test import TestCase
import datetime
from django.test import TestCase
from django.utils import timezone
from . models import Question
from django.urls import reverse

# Create your tests here.
class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)
        
# def create_question(question_text, days):
    
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text = question_text, pub_date = time)


def create_question(question_text, days, choice = 1):
    
    time = timezone.now() + datetime.timedelta(days=days)
    question = Question.objects.create(question_text = question_text, pub_date = time)
    if choice == 1:
        question.choice_set.create(choice_text="text", votes=0)
        return question
    else:
        return question
    

    
class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question("Past Question.", -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        create_question("Future Question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        question = create_question("Past Question.", -30)
        create_question("Future Question.", 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        question1 = create_question("Past Question 1.", -30)
        question2 = create_question("Past Question 2.", -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])

    def test_question_without_choices(self):
        create_question("question_without_choices", -2, 0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'],[])

    def test_question_with_choices(self):
        question = create_question("question_with_choices", -2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'],[question])

                        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question("Future Question .", 5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        Past_question = create_question("Past Question .", -5)
        url = reverse('polls:detail', args=(Past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, Past_question.question_text)


class QuestionResultViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question("Future Question .", 5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404) 

    def test_past_question(self):
        Past_question = create_question("Past Question .", -5)
        url = reverse('polls:results', args=(Past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, Past_question.question_text)







        
