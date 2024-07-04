from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


User = get_user_model()


class OneTimeCodeBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        phone = kwargs.get("phone")
        one_time_code = kwargs.get("password")

        if phone is None or one_time_code is None:
            return None

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        right_one_time_code = request.session.pop(phone, None)
        if one_time_code == right_one_time_code:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
