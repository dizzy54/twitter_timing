from django.test import TestCase
from django.test import Client


# Create your tests here.
class BestTimeApiTestCase(TestCase):
    def test_correct_user_id(self):
        """
        tests if api returns correct response given correct user_id
        """
        user_id = 'akshat54'
        c = Client()
        response = c.post('/timing/get_best_posting_time', {'username': '', 'user_id': user_id})
        print(response.content)
        print(response.status_code)
