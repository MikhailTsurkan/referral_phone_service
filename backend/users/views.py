from rest_framework import generics, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserRetrieveSerializer, UserPhoneSerializer
from django.contrib.auth import get_user_model

from users.services import create_invite_code, send_code, create_one_time_code


User = get_user_model()


class GetOrCreateModelMixin:
    def get_or_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_get_or_create(serializer)
        if created:
            headers = self.get_success_headers(request.data)
            return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(request.data, status=status.HTTP_200_OK)

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
    serializer_class = UserPhoneSerializer

    def perform_get_or_create(self, serializer):

        user, created = self.model.objects.get_or_create(**serializer.validated_data,
                                                         defaults={"invite_code": create_invite_code()})
        code = create_one_time_code()
        self.request.session[user.phone] = code
        send_code(user.phone, code)

        return created


class UserReceivesCodeAPIView(UserReceivesCodeMixin, generics.GenericAPIView):
    pass


class SetRefererAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        invite_code = request.data.get("invite_code")
        referral = request.user
        if referral.invite_code == invite_code:
            return Response({"message": "you cannot enter your own invite code"})
        if referral.invited_by is not None:
            return Response({"message": f"you have already been referral "
                                        f"of user with invite code {referral.invited_by.invite_code}"})

        referer = get_object_or_404(User.objects.filter(invite_code=invite_code))

        referral.invited_by = referer
        referral.save()
        return Response({"message": f"you have become referral of user with invite code {referer.invite_code}"})


class UserRetrieveItSelfAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
