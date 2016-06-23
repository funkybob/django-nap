from django.test import TestCase
import json
from nap.http import STATUS

from .models import Poll


class ListRestViewTest(TestCase):

    def setUp(self):
        self.question_1 = {'question': 'Question 1', 'pub_date': '2016-05-13 00:00:00'}
        self.question_2 = {'question': 'Question 2', 'pub_date': '2015-05-13 00:00:00'}
        Poll.objects.create(question=self.question_1['question'], pub_date=self.question_1['pub_date'])
        Poll.objects.create(question=self.question_2['question'], pub_date=self.question_2['pub_date'])

    def test_get(self):
        response = self.client.get('/rest/polls/')
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data[0], self.question_1)
        self.assertEqual(data[1], self.question_2)

    def test_post(self):
        request_data = {}
        response = self.client.post('/rest/polls/', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'question': 'Question 1'}
        response = self.client.post('/rest/polls/', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'pub_date': '2016-05-13 00:00:00'}
        response = self.client.post('/rest/polls/', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'question': 'Question 1', 'pub_date': '2016-05-13 00:00:00'}
        response = self.client.post('/rest/polls/', data=json.dumps(request_data), content_type='application/json')
        self.assertEqual(response.status_code, STATUS.CREATED)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, request_data)


class SingleObjectRestViewTest(TestCase):

    def setUp(self):
        self.default_question = 'Default question'
        self.default_pub_date = '2015-01-01 00:00:00'
        self.poll = Poll.objects.create(question=self.default_question, pub_date=self.default_pub_date)

    def test_get(self):
        response = self.client.get('/rest/polls/{}'.format(self.poll.pk))
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data['question'], self.default_question)
        self.assertEqual(data['pub_date'], self.default_pub_date)

    def test_put(self):
        # put requires all fields
        request_data = {}
        response = self.client.put('/rest/polls/{}'.format(self.poll.pk),
                                   data=json.dumps(request_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'question': 'A new question'}
        response = self.client.put('/rest/polls/{}'.format(self.poll.pk),
                                   data=json.dumps(request_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'pub_date': '2014-06-01 12:30:30'}
        response = self.client.put('/rest/polls/{}'.format(self.poll.pk),
                                   data=json.dumps(request_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, STATUS.BAD_REQUEST)

        request_data = {'question': 'A new question', 'pub_date': '2014-06-01 12:30:30'}
        response = self.client.put('/rest/polls/{}'.format(self.poll.pk),
                                   data=json.dumps(request_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, request_data)
        # reload poll from db and see that it's updated
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.question, request_data['question'])
        self.assertEqual(poll.pub_date.isoformat(' '), request_data['pub_date'])

    def test_patch(self):
        # patch can have any combination of fields
        request_data = {}
        response = self.client.patch('/rest/polls/{}'.format(self.poll.pk),
                                     data=json.dumps(request_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, {'question': self.default_question, 'pub_date': self.default_pub_date})
        # reload poll from db and see that it's updated
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.question, self.default_question)
        self.assertEqual(poll.pub_date.isoformat(' '), self.default_pub_date)

        # one field
        request_data = {'question': 'One field question'}
        response = self.client.patch('/rest/polls/{}'.format(self.poll.pk),
                                     data=json.dumps(request_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, {'question': request_data['question'], 'pub_date': self.default_pub_date})
        # reload poll from db and see that it's updated
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.question, request_data['question'])
        self.assertEqual(poll.pub_date.isoformat(' '), self.default_pub_date)

        request_data = {'question': 'A new question', 'pub_date': '2014-06-01 12:30:30'}
        response = self.client.patch('/rest/polls/{}'.format(self.poll.pk),
                                     data=json.dumps(request_data),
                                     content_type='application/json')
        self.assertEqual(response.status_code, STATUS.OK)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(data, request_data)
        # reload poll from db and see that it's updated
        poll = Poll.objects.get(pk=self.poll.pk)
        self.assertEqual(poll.question, request_data['question'])
        self.assertEqual(poll.pub_date.isoformat(' '), request_data['pub_date'])

    def test_delete(self):
        response = self.client.delete('/rest/polls/{}'.format(self.poll.pk))
        self.assertEqual(response.status_code, STATUS.NO_CONTENT)
        # make sure the poll isn't in the db
        self.assertFalse(Poll.objects.filter(pk=self.poll.pk).exists())
