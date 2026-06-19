from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        print("AUTH HEADER:", auth)
        return super().authenticate(request)

    def get_user(self, validated_token):
        print("TOKEN TYPE:", validated_token.get("token_type"))

        user = super().get_user(validated_token)

        token_session_id = validated_token.get("session_id")

        if user.current_session_id != token_session_id:
            raise AuthenticationFailed(
                "Session expired. Please login again."
            )

        return user