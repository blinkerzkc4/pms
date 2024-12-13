from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.serializers import UserSerializer, UserSerializerForToken


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_detail"] = UserSerializerForToken(user).data
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializerForToken(self.user).data

        return data
