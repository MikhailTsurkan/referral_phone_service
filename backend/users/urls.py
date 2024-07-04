from django.urls import path

from users import views
from rest_framework_simplejwt.views import token_refresh, token_obtain_pair
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path("auth/get-code/", views.UserReceivesCodeAPIView.as_view(), name="get-code"),
    path("auth/send-code/", token_obtain_pair, name="send-code"),
    path("auth/refresh/", token_refresh, name="token-refresh"),

    path("set-referer/", views.SetRefererAPIView.as_view(), name="set-referral"),
    path("retrieve-current/", views.UserRetrieveItSelfAPIView.as_view(), name="retrieve-current"),
]
