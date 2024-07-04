from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "phone"
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()
    invited_by_code = serializers.SerializerMethodField()

    def get_referrals(self, obj):
        return obj.referrals.values_list("phone", flat=True)

    def get_invited_by_code(self, obj):
        return obj.invited_by.invite_code

    class Meta:
        model = User
        fields = ["phone", "referrals", "invite_code", "invited_by_code"]
