import unittest, json, os, chardet
from os.path import realpath, dirname, join, isfile

from main import flaskApp

cwd = join(dirname(realpath(__file__)))


def images_dir(extra):
    return join(cwd, '..', 'app', 'resources', 'images', extra)

def static_url(extra):
    return 'static/' + extra

def test_dir(extra=""):
    return join(cwd, extra)

def resources_dir(extra):
    return join(test_dir(), 'resources', extra)

def asset_url(extra):
    return 'assets/' + extra

def asset_dir(extra):
    return join('app', 'assets', extra)


class BaseTest(unittest.TestCase):
    flaskApp = None
    postUrl = None

    def setUp(self):
        flaskApp.testing = True
        self.flaskApp = flaskApp.test_client()



class MainSiteTests(BaseTest, unittest.TestCase):
    def setUp(self):
        super().setUp()

    def get_and_assert(self, url, status):
        r = self.flaskApp.get(url)
        self.assertEqual(status, r.status_code)
        r.close()

    def post_and_assert(self, url, status):
        r = self.flaskApp.post(url)
        self.assertEqual(status, r.status_code)
        r.close()

    def test_favicon(self):
        self.get_and_assert(static_url('favicon.ico'), 200)

    def test_favicon_post(self):
        self.post_and_assert(static_url('favicon.ico'), 405)

    def test_sp_logo(self):
        self.get_and_assert(static_url('sp_logo.svg'), 200)

    def test_sp_logo_post(self):
        self.post_and_assert(static_url('sp_logo.svg'), 405)

    def test_css(self):
        self.get_and_assert(asset_url("w3.css"), 200)

    def test_css_post(self):
        self.post_and_assert(asset_url('w3.css'), 405)

    def test_css_bad(self):
        self.get_and_assert(asset_url('../favico.ico.css'), 404)

class ImageModuleTests(BaseTest, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.postUrl = '/upload'

    def test_upload_get(self):
        r = self.flaskApp.get(self.postUrl)
        self.assertEqual(405, r.status_code)

    def test_upload_post_empty(self):
        r = self.flaskApp.post(self.postUrl)
        self.assertEqual(403, r.status_code)

    def test_upload_post_bad_pw(self):
        r = self.flaskApp.post(self.postUrl, data={"password": "not"})
        self.assertEqual(403, r.status_code)

    def test_upload_post_no_file(self):
        r = self.flaskApp.post(self.postUrl, data={"password": "<pw>"})
        self.assertEqual(400, r.status_code)

    def test_upload_post(self):
        with open(resources_dir('image.png'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(200, r.status_code)
            url = r.data.decode("utf-8")
            self.assertRegex(url, '\/[A-Za-z0-9]+\.(png|jpg|jpeg)')

            fileName = url.split("/")[-1]
            self.assertTrue(isfile(images_dir(fileName)))

    def test_upload_post_bad_name(self):
        with open(resources_dir('image.svg'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(400, r.status_code)

    def test_upload_post_good_name_bad_type(self):
        with open(resources_dir('image.jpg'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(400, r.status_code)

    def test_upload_post_bad(self):
        with open(resources_dir('image.sh'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(400, r.status_code)


if __name__ == '__main__':
    unittest.main()
