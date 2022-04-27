from unittest import TestCase

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('email', 'Your e-mail'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username',
         'Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.'),  # noqa: E501
        ('email', 'The e-mail must be valid'),
        ('password',
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
         ),
    ])
    def test_fields_help_text_is_correct(self, field, needed):
        form = RegisterForm()
        current_help_text = form[field].field.help_text
        self.assertEqual(needed, current_help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Confirm password'),
    ])
    def test_fields_label_is_correct(self, field, needed):
        form = RegisterForm()
        current_label = form[field].field.label
        self.assertEqual(needed, current_label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):

        self.form_data = {
            'username': 'user',
            'first_name': 'steve',
            'last_name': 'jones',
            'email': 'email12@email.com',
            'password': 'aBc12345678',
            'password2': 'aBc12345678',
        }

        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))
