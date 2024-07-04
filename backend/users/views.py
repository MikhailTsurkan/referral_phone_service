from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from users.serializers import SendCodeSerializer
from django.contrib.auth import get_user_model

from users.services import create_invite_code, send_code, create_one_time_code


User = get_user_model()


class GetOrCreateModelMixin:
    def get_or_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_get_or_create(serializer)
        if created:
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_get_or_create(self, serializer):
        raise NotImplementedError

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        return self.get_or_create(request, *args, **kwargs)


class UserReceivesCodeMixin(GetOrCreateModelMixin):
    model = User
    serializer_class = SendCodeSerializer

    def perform_get_or_create(self, serializer):
        data = serializer.validated_data
        user, created = self.model.objects.get_or_create(**data, defaults={"invite_code": create_invite_code()})
        code = create_one_time_code()
        self.request.session["one_time_code"] = code
        send_code(user.phone, code)

        return created


class UserReceivesCodeAPIView(UserReceivesCodeMixin, generics.GenericAPIView):
    pass
