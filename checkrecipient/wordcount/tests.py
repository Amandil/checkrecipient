from django.test import TransactionTestCase, Client

import json

UPLOAD_EMAILS = "/api/upload_emails"

class TestUploadEmails(TransactionTestCase):

    '''
    Creating client to run against test database
    '''
    def setUp(self):
        self.client = Client()

    def test_small_sample(self):
        input_file = open('./wordcount/test_data/mini.json', 'r')
        input_data = json.loads(input_file.read())

        for upload in input_data["uploads"]:
            response = self.client.post(UPLOAD_EMAILS,content_type="application/json", data=json.dumps(upload))
            self.assertEqual(200, response.status_code, response.content)

    def test_big_sample(self):
        input_file = open('./wordcount/test_data/uploads.json', 'r')
        input_data = json.loads(input_file.read())

        for upload in input_data["uploads"]:
            response = self.client.post(UPLOAD_EMAILS,content_type="application/json", data=json.dumps(upload))
            self.assertEqual(200, response.status_code, response.content)
