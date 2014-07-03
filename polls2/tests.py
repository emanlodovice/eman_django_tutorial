import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls2.models import Poll

def poll_creator(question, days=0, hours=0, choices=None):	
	p = Poll.objects.create(question=question, pub_date=timezone.now() + datetime.timedelta(days=days))
	if choices is not None:
		[p.choice_set.create(choice_text=choice, votes=0) for choice in choices]
	return p


class PollMethodTests(TestCase):

	def test_was_published_recently_with_future_poll(self):
		p = poll_creator(question="Future", days=30)
		self.assertEqual(p.was_published_recently(), False)

	def test_was_published_recently_with_old_poll(self):
		p = poll_creator(question="Old", days=-20)
		self.assertEqual(p.was_published_recently(), False)

	def test_was_published_recently_with_recent_poll(self):
		p = poll_creator(question="Recent", hours=1)
		self.assertEqual(p.was_published_recently(), True)


class PollIndexViewTests(TestCase):

	def test_index_view_with_no_polls(self):
		response = self.client.get(reverse('polls2:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_a_past_poll(self):
		poll_creator(question="Past", days=-30, choices=['no choice'])		
		response = self.client.get(reverse('polls2:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past>'])

	def test_index_view_with_a_future_poll(self):
		poll_creator(question="Future", days=2, choices=['no choice'])
		response = self.client.get(reverse('polls2:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])

	def test_index_view_with_a_future_and_past_poll(self):
		poll_creator(question="Future", days=2, choices=['no choice'])
		poll_creator(question="Past", days=-3, choices=['no choice'])
		response = self.client.get(reverse('polls2:index'))
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past>'])

	def test_index_view_with_two_past_polls(self):
		poll_creator(question="Past1", days=-2, choices=['no choice'])
		poll_creator(question="Past2", days=-10, choices=['no choice'])
		response = self.client.get(reverse('polls2:index'))
		self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past1>', '<Poll: Past2>'])

	def test_index_view_with_polls_with_no_choices(self):
		poll_creator(question="no choice", days=-3)
		response = self.client.get(reverse('polls2:index'))
		self.assertQuerysetEqual(response.context['latest_poll_list'], [])




class PollDetailViewTests(TestCase):

	def test_detail_view_with_a_future_poll(self):
		p = poll_creator(question="Future", days=2, choices=['no choice'])
		response = self.client.get(reverse('polls2:detail', args=(p.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_poll(self):
		p = poll_creator(question="Past", days=-3, choices=['no choice'])
		response = self.client.get(reverse('polls2:detail', args=(p.id,)))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, p.question)

	def test_detail_view_with_poll_with_no_choices(self):
		p = poll_creator(question="No choices", days=-3)
		response = self.client.get(reverse('polls2:detail', args=(p.id,)))
		self.assertEqual(response.status_code, 404)



