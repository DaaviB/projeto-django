from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

    @patch('recipes.views.PER_PAGE', new=4)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This os what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto 'Search for recipes'
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipes"]'
        )

        #  Clica neste input e digita o termo de busca
        #  para encontrar a receita com o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        #  Usuário encontra o que desejava na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )
