from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from user.models import ExternalUser


@api_view(["POST"])
@permission_classes([])
def get_token(request):
    app_name = request.data.get("app_name")
    password = request.data.get("password")

    external_user = get_object_or_404(ExternalUser, external_app_name=app_name)

    user = authenticate(username=external_user.username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})
