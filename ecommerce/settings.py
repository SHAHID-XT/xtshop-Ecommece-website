from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-h+boc09nn^q)$unrvemcixk%bo78+u8bhc_a88!jhf6wy)x&l8"

# SESSION_COOKIE_AGE = 36000  # cookies timeout in seconds
# SESSION_COOKIE_HTTPONLY = True
# CSRF_COOKIE_HTTPONLY = True
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "DENY"
# SECURE_HSTS_SECONDS = 3600 
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True


DEBUG = True


PAYPAL_CLIENT_ID = (
    "Aci91OiJZB05ZlJCz4SKAZ4Ju07F85eexyI_ApNuhWmnqC6OkvZ2h01kKOU6Hw9XJIjq_mPdGEBm9fl7"
)
PAYPAL_CLIENT_SECRET = (
    "ED5N-8TNla-98bKAHWxLBkk4X2x3ztlF23X6l_8kaNItRdpGgsJ_PGHUaSN08L1Gwb1FYTivKC2DsZOK"
)
# List of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "auths",
    # 'django_extensions', # for htttps
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "products",
    "analytics",
    "seller",
    "django_user_agents", #pip
]

# Middleware classes to use
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise for serving static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "ecommerce.middleware.NotFoundMiddleware",  # custom context processors
    "django_user_agents.middleware.UserAgentMiddleware", #pip

]


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# If DEBUG is False, this will automatically be set to True.
if not DEBUG:
    WHITENOISE_USE_FINDERS = True

# Root URL configuration module
ROOT_URLCONF = "ecommerce.urls"

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates")
        ],  
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "ecommerce.context_processors.global_variables",  # custom context processors
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = "ecommerce.wsgi.application"

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"  # Set timezone to India (IST)
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/public/"

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "public"),
]

# URL to use when referring to static files located in MEDIA_ROOT
MEDIA_URL = "/media/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static root directory for collecting static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Add your custom static directories to STATICFILES_DIRS
staticsdir = [
    os.path.join(BASE_DIR, str(f), "public") for f in INSTALLED_APPS if "." not in f
]
STATICFILES_DIRS.extend(staticsdir)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
# AUTH_USER_MODEL = "auths.CustomUser"
