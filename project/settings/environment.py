import os
from pathlib import Path
from typing import List

from utils.environment import get_env_variable, parse_comma_str_to_list

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: List[str] = parse_comma_str_to_list(
    get_env_variable('ALLOWED_HOSTS'))
CSRF_TRUSTED_ORIGINS: List[str] = parse_comma_str_to_list(
    get_env_variable('CSRF_TRUSTED_ORIGINS'))
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
