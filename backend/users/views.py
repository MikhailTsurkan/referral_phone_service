from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from users.serializers import SendCodeSerializer, UserRetrieveSerializer
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


class SetRefererAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invite_code = request.data.get("invite_code")
        referral = request.user

        if referral.invited_by is not None:
            return Response({"message": f"you have already been referral "
                                        f"of user with invite code {referral.invited_by.invite_code}"})

        referer = get_object_or_404(User.objects.filter(invite_code=invite_code))

        referral.invited_by = referer
        referral.save()
        return Response({"message": f"you have become referral of user with invite code {referer.invite_code}"})


class UserRetrieveItSelfAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user
