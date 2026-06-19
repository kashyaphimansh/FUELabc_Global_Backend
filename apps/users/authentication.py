from rest_framework_simplejwt.authentication import (
    JWTAuthentication
)

from rest_framework.exceptions import (
    AuthenticationFailed
)

class CustomJWTAuthentication(
    JWTAuthentication
):

    def get_user(
        self,
        validated_token
    ):

        user = super().get_user(
            validated_token
        )

        token_session_id = validated_token.get(
            "session_id"
        )

        if (
            user.current_session_id
            != token_session_id
        ):

            raise AuthenticationFailed(
                "Session expired. Please login again."
            )

        return user