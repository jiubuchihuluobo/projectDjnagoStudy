"""
Django settings for permissionTest project.

Generated by 'django-admin startproject' using Django 3.2.18.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

from rest_framework.settings import api_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&%8lt#v(*)716k&v7^n67lu1$eotl5#9qhgbn3py4i(gcocthy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    # Django原生
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django扩展
    "django_extensions",

    # DRF原生
    "rest_framework",
    # 'rest_framework.authtoken',

    # DRF扩展
    # "knox",
    "rest_framework_simplejwt",
    # 'drf_yasg',
    'drf_spectacular',
    'rest_framework_simplejwt.token_blacklist',

    # App
    "customauth",
    # "demo",
    "todoapp",
    # "hr",
    # "drfauth",
    # "knoxauth",
    "jwtauth",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # 不检查csrf
    "utils.middleware.DisableCsrfMiddleware",

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'permissionTest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'permissionTest.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mytest',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'qiliu',
        'PASSWORD': '2wsxCvgy7',
        'OPTIONS': {
            'options': '-c search_path=mydjango'
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/4.1/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# https://docs.djangoproject.com/en/4.1/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / 'media'

# https://docs.djangoproject.com/en/4.1/ref/settings/#media-url
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Customizing authentication in Django
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/
AUTH_USER_MODEL = 'customauth.User'

# https://docs.djangoproject.com/en/4.1/ref/settings/#login-url
LOGIN_URL = 'myauth:mylogin'

# https://www.django-rest-framework.org/api-guide/settings/#settings
REST_FRAMEWORK = {
    # https://www.django-rest-framework.org/api-guide/settings/#datetime_format
    # "DATETIME_FORMAT": "iso-8601",

    # https://github.com/tfranzel/drf-spectacular
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # https://www.django-rest-framework.org/api-guide/authentication/
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        # 'utils.authentication.NoCsrfSessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'utils.authentication.BearerTokenAuthentication',
        # "knox.auth.TokenAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# https://james1345.github.io/django-rest-knox/settings/
REST_KNOX = {
    # cryptography.hazmat.primitives.hashes.Whirlpool
    # cryptography.hazmat.primitives.hashes.MD5
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',

    'AUTH_TOKEN_CHARACTER_LENGTH': 64,

    # 设置0或负时间将创建立即过期的令牌
    # 设置为None将创建永远不会过期的令牌
    'TOKEN_TTL': timedelta(hours=1),

    'USER_SERIALIZER': 'knox.serializers.UserSerializer',

    'TOKEN_LIMIT_PER_USER': None,

    # 每次使用令牌时是否自动延期令牌
    'AUTO_REFRESH': False,

    'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,

    "AUTH_HEADER_PREFIX": "Bearer",
}

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # 生成新的refresh token与access token
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    # User模型类last_login字段在登陆时更新
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    # 到期时间定义的回旋余地部分，这意味着您可以验证过去但不是很远的到期时间
    "LEEWAY": 0,

    # 授权头类型
    "AUTH_HEADER_TYPES": ("Bearer",),
    # 授权头名称HTTP_X_ACCESS_TOKEN与HTTP_AUTHORIZATION
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    # 是否允许用户进行身份验证，默认规则是检查is_active标志
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    # claim中的令牌唯一标识符名称
    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "jwtauth.serialziers.MyTokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# https://github.com/tfranzel/drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
