import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_recipe_home_page_without_recipes_not_found_message(self):
        browser = self.browser
        browser.get(self.live_server_url)
        self.sleep()

        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(
            'No recipes available to display at the moment', body.text
        )
