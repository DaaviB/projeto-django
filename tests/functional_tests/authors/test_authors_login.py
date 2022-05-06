import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'password'
        user = User.objects.create_user(
            username='my_username', password=string_password)

        # Usuário abre a página de Login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário vê o formulário de login
        form = self.browser.find_element(
            By.CLASS_NAME,
            'main-form'
        )
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o formulario
        form.submit()

        self.assertIn(
            f'Your are logged in with {user.username}',
            self.browser.find_element(
                By.TAG_NAME,
                'body'
            ).text
        )
