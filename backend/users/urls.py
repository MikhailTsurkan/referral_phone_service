from django.urls import path

from users import views
from users.apps import UsersConfig


app_name = UsersConfig.name

urlpatterns = [
    path("auth/get-code", views.UserReceivesCodeAPIView.as_view(), name="get-code"),

]
