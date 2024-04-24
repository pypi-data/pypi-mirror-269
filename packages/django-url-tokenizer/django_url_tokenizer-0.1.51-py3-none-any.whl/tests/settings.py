import os
from pathlib import Path

SECRET_KEY = "secret"

BASE_DIR = Path(__file__).resolve().parent

AUTH_USER_MODEL = "testapp.TestUser"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_db",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "urltokenizer",
    "tests.testapp.apps.TestAppConfig",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
        },
    },
    "loggers": {
        "root": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

URL_TOKENIZER_SETTINGS = {
    "USER_SERIALIZER": "tests.testapp.serializers.UserSerializer",
    # token
    "VALIDATE_TOKEN_TYPE": True,
    "ENCODING_FIELD": "pk",
    "TIMEOUT": 60,
    # url
    "DOMAIN": "localhost",
    "PROTOCOL": "https",
    "PORT": "443",
    # sending
    "SEND_ENABLED": True,
    # "CHANNEL": "email",
    # email
    "EMAIL_FIELD": "email",
    "NAME_FIELD": "full_name",
    # sms
    "PHONE_FIELD": "phone",
    # logging
    "LOGGING_ENABLED": True,
    "CHECK_LOGS": True,
    # error handling
    "FAIL_SILENTLY_ON_GENERATE": True,
    "FAIL_SILENTLY_ON_BULK_GENERATE": True,
    "FAIL_SILENTLY_ON_CHECK": False,
    "FAIL_SILENTLY_ON_CALLBACKS": False,
    # token config
    # todos los parametros anteriores (excepto 'VALIDATE_TOKEN_TYPE')
    # pueden ser sobreescritos en cada configuracion de token de forma individual
    # con el mismo nombre de parametro en minusculas
    "TOKEN_CONFIG": {
        "default": {
            "path": "/",
        },
        "set-password": {
            "path": "set-password/",
            "attributes": ["password"],
            "preconditions": {
                "has_no_email": lambda user: user.email,
                "has_password": lambda user: not user.password,
            },
            "callbacks": [
                {
                    "method": "_set_password",
                    "defaults": {"raise_exception": True},
                },
                {
                    "lambda": lambda user: user.verify(user.last_channel),
                },
                {
                    "method": "generate_tokens",
                    "defaults": {"as_dict": True},
                    "return_value": True,
                },
            ],
            "email_subject": "Completa tu registro en Flexza",
        },
        "pre-register": {
            "path": "pre-register/",
            "attributes": ["email", "phone"],
            "preconditions": {
                "has_email": lambda user: not user.email,
                "has_password": lambda user: not user.password,
            },
            "callbacks": [
                {
                    "lambda": lambda user: user.verify(user.last_channel),
                },
                {
                    "method": "generate_tokens",
                    "defaults": {"as_dict": True},
                    "return_value": True,
                },
            ],
            "email_subject": "Completa tu registro en Flexza",
        },
        "password-recovery": {
            "path": "password-recovery/",
            "attributes": ["password", "last_login"],
            # "send_preconditions": [lambda user: user.email_verified],
            # "check_preconditions": [lambda user: user.email_verified],
            "callbacks": [
                {
                    "method": "_set_password",
                    "defaults": {"raise_exception": True},
                }
            ],
            "email_subject": "Recupera tu contraseña de Flexza con el siguiente link",
        },
    },
}
