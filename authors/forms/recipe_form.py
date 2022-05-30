from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = 'created_at', 'update_at', \
            'slug', 'preparation_steps_is_html', 'author', \
            'is_published', 'tags',

        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),

            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),

        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        cleaned_data = super_clean

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_time = cleaned_data.get('preparation_time')
        servings = cleaned_data.get('servings')
        preparation_steps = cleaned_data.get('preparation_steps')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must have at least 5 chars.')

        if len(description) < 10:
            self._my_errors['description'].append(
                'Description must have at least more than 20 characters.'
            )

        if title == description:
            self._my_errors['title'].append(
                'Title cannot be equal to description.')
            self._my_errors['description'].append(
                'Description cannot be equal to title.')

        if not is_positive_number(preparation_time):
            self._my_errors['preparation_time'].append(
                'Preparation time must be a positive number')

        if not is_positive_number(servings):
            self._my_errors['servings'].append(
                'Servings must be a positive number')

        if len(preparation_steps) < 30:
            self._my_errors['preparation_steps'].append(
                'Preparation_steps must have at least more than 20 characters.'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean
