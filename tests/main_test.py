import unittest

from main import flaskApp as app

class baseTests():
    def baseSetUp(self):
        app.testing = True
        self.app = app.test_client()

class StaticTests(unittest.TestCase, baseTests):
    def setUp(self):
        self.baseSetUp()

    def test_favicon(self):
        r = self.app.get('/image/favicon')
        self.assertEqual(200, r.status_code)


class ImageModuleTests(unittest.TestCase, baseTests):
    def setUp(self):
        self.baseSetUp()
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
        r = self.app.post(self.postUrl, data={"password": "<pw>"})
        self.assertEqual(400, r.status_code)

    #def test_upload_post_bad_type(self):
        #r = self.app.post(self.postUrl, data={"password": "<pw>"})

    #need real resources
    #def test_upload_post(self):
     #   r = self.app

if __name__ == '__main__':
    unittest.main()
