import pytest
from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        browser = self.browser
        browser.get(self.live_server_url)
        self.sleep()

        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn(
            'No recipes available to display at the moment', body.text
        )
