import unittest, json, os, chardet

from main import flaskApp


def ImagesDir(extra):
    return os.path.join(os.getcwd(), 'public', 'images', extra)


def TestDir(extra):
    return os.path.join(os.getcwd(), 'tests', extra)


class BaseTest(unittest.TestCase):
    flaskApp = None
    postUrl = None

    def setUp(self):
        flaskApp.testing = True
        self.flaskApp = flaskApp.test_client()


class MainSiteTests(BaseTest, unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_favicon(self):
        r = self.flaskApp.get("/favicon")
        self.assertEqual(200, r.status_code)

    def test_favicon_post(self):
        r = self.flaskApp.post("/favicon")
        self.assertEqual(405, r.status_code)

    def test_sp_logo(self):
        r = self.flaskApp.get("/public/sp_logo")
        self.assertEqual(200, r.status_code)

    def test_sp_logo_post(self):
        r = self.flaskApp.post("/public/sp_logo")
        self.assertEqual(405, r.status_code)

    def test_css(self):
        r = self.flaskApp.get("/public/assets/w3.css")
        self.assertEqual(200, r.status_code)
        with open("public/assets/w3.css", "r") as f:
            file = "".join(f.readlines())
            data = r.data.decode("utf-8").rstrip().replace('\r', '')
            self.assertEqual(file, data)

    def test_css_post(self):
        r = self.flaskApp.post("/public/assets/w3.css")
        self.assertEqual(405, r.status_code)

    def test_css_bad(self):
        r = self.flaskApp.get("/public/assets/../favicon.ico.css")
        self.assertEqual(404, r.status_code)

class ImageModuleTests(BaseTest, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.postUrl = '/upload/image'

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
        with open(TestDir('resources/image.png'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(200, r.status_code)
            url = r.data.decode("utf-8")
            self.assertRegex(url, '\/image\/[A-Za-z0-9]+\.(png|jpg|jpeg)')

            fileName = url.split("/")[-1]
            self.assertTrue(os.path.isfile('public/images/{}'.format(fileName)))

    def test_upload_post_bad_name(self):
        with open(TestDir('resources/image.svg'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(200, r.status_code)
            url = r.data.decode("utf-8")
            self.assertRegex(url, '\/image\/[A-Za-z0-9]+\.svg')

            fileName = url.split("/")[-1]
            self.assertTrue(os.path.isfile('public/images/{}'.format(fileName)))

    def test_upload_post_good_name_bad_type(self):
        with open(TestDir('resources/image.jpg'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(400, r.status_code)
            result = json.dumps(r.data.decode("utf-8"))
            self.assertRegex(result, "Invalid File Type")

    def test_upload_post_bad(self):
        with open(TestDir('resources/image.sh'), 'rb') as file:
            r = self.flaskApp.post(self.postUrl, data={"password": "<pw>", "upload": file})

            self.assertEqual(400, r.status_code)
            result = json.dumps(r.data.decode("utf-8"))
            self.assertRegex(result, "Invalid File Type")


if __name__ == '__main__':
    unittest.main()
