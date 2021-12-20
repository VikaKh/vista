DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "$DB_NAME",
        "USER": "$DB_USER",
        "PASSWORD": "$DB_PASSWORD",
        "HOST": "$DB_HOST",
        "PORT": "$DB_PORT",
        "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_unicode_ci"},
    },
    "vista-med": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "$DB_NAME",
        "USER": "$DB_USER",
        "PASSWORD": "$DB_PASSWORD",
        "HOST": "$DB_HOST",
        "PORT": "$DB_PORT",
        "TEST": {"MIGRATE": False},
    },
}
CORS_ALLOWED_ORIGINS = [  # Add this to use react app running at localhost:3000
    "http://localhost:3000",
    "https://vista-frontend.herokuapp.com"
]

DEBUG = "False"
DEFAULT_ORG_ID = 300234
CSRF_TRUSTED_ORIGINS = ['vista-backend.herokuapp.com', 'https://vista-backend.herokuapp.com']
