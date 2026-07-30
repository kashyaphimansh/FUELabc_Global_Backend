from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from django.conf import settings

path = Path(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)

if path.exists() and not firebase_admin._apps:
    cred = credentials.Certificate(str(path))
    firebase_admin.initialize_app(cred)