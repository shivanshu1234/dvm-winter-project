import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'YourSecretKey'

DATABASES = {
    'default': {
        'ENGINE': 'Engine',
        'NAME': 'Name',
    }
}
