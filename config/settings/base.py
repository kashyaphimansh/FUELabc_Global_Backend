from pathlib import Path

from decouple import config

from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config(
    'DEBUG',
    cast=bool,
)

INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    'rest_framework',

    'corsheaders',

    'apps.users',

    'apps.vehicles',
  
    'apps.aem',

    "apps.tripanalytics",

    'apps.subscriptions',
    
    'apps.app_settings',

    "apps.co2",

    "apps.mileage_advisor", 
]

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [

    {

        'BACKEND':

            'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

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


ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL = 'static/'

FIREBASE_SERVICE_ACCOUNT_KEY_PATH = config(
    'FIREBASE_SERVICE_ACCOUNT_KEY_PATH'
)

AUTH_USER_MODEL = "users.User"

RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')

RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')

DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.postgresql',

        'NAME':
            config('DB_NAME'),

        'USER':
            config('DB_USER'),

        'PASSWORD':
            config('DB_PASS'),

        'HOST':
            config('DB_HOST'),

        'PORT':
            config(
                'DB_PORT',
                default=5432,
            ),
    }
}

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [

        'apps.users.authentication.CustomJWTAuthentication',
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),

    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",

    "SIGNING_KEY": config("JWT_SIGNING_KEY"),
}

CORS_ALLOW_ALL_ORIGINS = True

