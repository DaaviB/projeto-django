from .installed_apps import INSTALLED_APPS
from .middleware import MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS += ['debug_toolbar', ]


MIDDLEWARE.insert(
    1, "debug_toolbar.middleware.DebugToolbarMiddleware",
)
