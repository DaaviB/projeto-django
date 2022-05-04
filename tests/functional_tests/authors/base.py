import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser


class AuthorBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, qtd=5):
        time.sleep(qtd)
