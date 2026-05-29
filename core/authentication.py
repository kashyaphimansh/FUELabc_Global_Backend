import firebase_admin

from firebase_admin import auth

from rest_framework.authentication import BaseAuthentication

from rest_framework.exceptions import AuthenticationFailed

from apps.users.models import User

from core.firebase import *

class FirebaseAuthentication(
    BaseAuthentication
):

    def authenticate(
        self,
        request,
    ):

        auth_header = request.META.get(
            'HTTP_AUTHORIZATION',
            '',
        )

        if not auth_header.startswith(
            'Bearer '
        ):
            return None

        token = auth_header.split(' ')[1]

        try:

            decoded_token = auth.verify_id_token(
                token
            )

            firebase_uid = decoded_token['uid']

            user, _ = User.objects.get_or_create(
                firebase_uid=firebase_uid
            )

            return (user, token)

        except Exception:

            raise AuthenticationFailed(
                'Invalid token'
            )
