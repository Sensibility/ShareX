import unittest

from app.main import app

class ImageModuleTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.postUrl = '/upload/image'

    def test_upload_get(self):
        r = self.app.get(self.postUrl)
        self.assertEqual(405, r.status_code)

    def test_upload_post_empty(self):
        r = self.app.post(self.postUrl)
        self.assertEqual(403, r.status_code)

    def test_upload_post_bad_pw(self):
        r = self.app.post(self.postUrl, data={"password": "not"})
        self.assertEqual(403, r.status_code)

    def test_upload_post_no_file(self):
        r = self.app.post(self.postUrl, data={"password": "not124"})
        self.assertEqual(400, r.status_code)

    #def test_upload_post_bad_type(self):

    #need real resources
    #def test_upload_post(self):
     #   r = self.app

if __name__ == '__main__':
    unittest.main()
