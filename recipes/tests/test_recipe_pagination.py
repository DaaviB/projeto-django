from django.http import HttpRequest
from utils.pagination import make_pagination

from .test_recipe_base import RecipeTestBase


class MakePaginationTest(RecipeTestBase):
    def test_make_pagination_shows_correct_number_of_recipe_per_page(self):  # noqa: E501

        request = HttpRequest()
        request.GET = {'page': 1}
        per_page = 9
        page_obj, pagination = make_pagination(
            request,
            range(1, 21),
            per_page
        )
        self.assertEqual(
            per_page,
            page_obj.paginator.per_page,
        )

    def test_make_pagination_raises_value_error_exception(self):
        request = HttpRequest()
        request.GET = {'page': ''}
        pagination = make_pagination(
            request,
            range(1, 21),
            1
        )

        self.assertEqual(1, pagination[1]['current_page'])
