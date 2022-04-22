from unittest import TestCase

from django.http import HttpRequest

from utils.pagination import make_pagination


class MakePaginationTest(TestCase):
    def test_make_pagination_raises_value_error_exception(self):
        request = HttpRequest()
        request.GET = {'page': ''}  # If ValueError Exception, Page = 1.
        pagination = make_pagination(
            request,
            range(1, 21),
            1
        )
        pagination = pagination[1]

        self.assertEqual(1, pagination['current_page'])
