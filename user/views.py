import logging

from django.contrib.auth.models import Group
from django.http import HttpRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from user.email import send_digital_signature_verification_email
from user.models import Client, Permission, User, UserRole
from user.permissions import (
    ActiveUserPermission,
    AdminsOnlyPermission,
    LoggedInReadOnly,
    ReadOnly,
)
from user.serializers import (
    ChangePasswordSerializer,
    ClientCreateSerializer,
    ClientSerializer,
    ClientSuperAdminViewSerializer,
    GroupSerializer,
    PermissionSerializer,
    UserCreateSerializer,
    UserRoleSerializer,
    UserSerializer,
)

logger = logging.getLogger("user:views")


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # set_password also hashes the password that the user will get
            user.set_password(serializer.data.get("new_password"))
            user.verified = True
            user.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeactivateUserView(APIView):
    """
    An endpoint for deactivating a user,
    the id is the id of the user who needs to be deactivated
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            user.is_active = False
            user.verified = False
            user.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


class ActivateUserView(APIView):
    """
    An endpoint for activating a user,
    the id is the id of the user who needs to be activated
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk, *args, **kwargs):
        try:
            user = User.objects.get(id=pk)
            user.is_active = True
            user.verified = True
            user.save()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)


class PermissionListView(generics.ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        return Group.objects.all()


class PermissionViewSet(ReadOnlyModelViewSet):
    serializer_class = PermissionSerializer
    permission_classes = [LoggedInReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Permission.objects.none()
        return Permission.objects.user_permissions(self.request.user).filter(
            parent__isnull=True
        )

    @action(detail=False, methods=["get"])
    def codes(self, request):
        permissions = Permission.objects.user_permissions(request.user)
        return Response(
            [permission.code for permission in permissions],
            status=status.HTTP_200_OK,
        )


class UserRoleViewSet(ModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [AdminsOnlyPermission]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ("municipality",)
    search_fields = ("title",)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserRole.objects.filter(status=True)
        else:
            return UserRole.objects.filter(
                municipality=self.request.user.assigned_municipality, status=True
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.users.count() > 0:
            return Response(
                {
                    "success": False,
                    "message": "Cannot delete a role that is assigned to a user",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)


class UserListView(generics.ListCreateAPIView):
    search_fields = ["username", "email"]
    serializer_map = {"GET": UserSerializer, "POST": UserCreateSerializer}
    permission_classes = [ActiveUserPermission & AdminsOnlyPermission]
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    ordering_fields = (
        "username",
        "email",
    )
    ordering = ("pk",)
    filterset_fields = ("is_active", "verified", "role_level")

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(
                assigned_municipality=self.request.user.assigned_municipality,
            )

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.request.method, "GET")

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            if serializer.validated_data.get("assigned_ward"):
                if (
                    serializer.validated_data.get("assigned_ward").municipality
                    != self.request.user.assigned_municipality
                ):
                    raise ValidationError(
                        "You are not allowed to create a ward user outside your municipality"
                    )
            else:
                serializer.save(
                    assigned_municipality=self.request.user.assigned_municipality
                )
                return
        if serializer.validated_data.get("assigned_ward"):
            serializer.save(
                assigned_municipality=serializer.validated_data.get(
                    "assigned_ward"
                ).municipality
            )
            return
        serializer.save()


class UserView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    serializer_class = UserSerializer
    permission_classes = [
        ActiveUserPermission & AdminsOnlyPermission | LoggedInReadOnly
    ]

    def get_queryset(self):
        return User.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(
                assigned_municipality=self.request.user.assigned_municipality
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            return Response(
                {
                    "success": False,
                    "message": "Cannot delete a superuser",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if instance.client_details:
            return Response(
                {
                    "success": False,
                    "message": "Cannot delete a client user",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientListView(generics.ListCreateAPIView):
    serializer_map = {"POST": ClientCreateSerializer}
    permission_classes = [ActiveUserPermission & AdminsOnlyPermission | ReadOnly]
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ["municipality"]
    ordering = ("pk",)
    filterset_fields = ("municipality", "subdomain", "client_id")

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # TODO: Update it only for main superuser
            if self.request.method == "GET" and self.request.user.is_superuser:
                return ClientSuperAdminViewSerializer
        return self.serializer_map.get(self.request.method, ClientSerializer)


class ClientView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = "pk"
    permission_classes = [ActiveUserPermission & AdminsOnlyPermission | ReadOnly]

    def get_queryset(self):
        return Client.objects.all()

    def get_serializer_class(self):
        # TODO: Update it only for main superuser
        if self.request.user.is_authenticated and self.request.user.is_superuser:
            return ClientSuperAdminViewSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(municipality=self.request.user.assigned_municipality)


@api_view(["GET"])
def profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return Response(
            {"status": "error", "message": "Please login before continuing."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def add_digital_signature(request: HttpRequest):
    if not request.user.is_authenticated:
        return Response(
            {"status": "error", "message": "Please login before continuing."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    digital_signature = request.FILES.get("digital_signature")
    if not digital_signature:
        return Response(
            {"status": "error", "message": "Please upload a digital signature."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if request.user.digital_signature:
        return Response(
            {
                "status": "error",
                "message": "Digital Signature already uploaded. Please remove it before continuing.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    request.user.digital_signature = digital_signature
    request.user.save()
    send_digital_signature_verification_email(request)
    return Response(
        {
            "status": "success",
            "message": "Digital Signature uploaded successfully. Please check your email for further verification.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["DELETE"])
def remove_digital_signature(request: HttpRequest):
    if not request.user.is_authenticated:
        return Response(
            {"status": "error", "message": "Please login before continuing."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if not request.user.digital_signature:
        return Response(
            {
                "status": "error",
                "message": "Digital Signature not uploaded. Please upload it before continuing.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    request.user.digital_signature = None
    request.user.save()
    return Response(
        {
            "status": "success",
            "message": "Digital Signature removed successfully.",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def verify_digital_signature(request: HttpRequest, uid: str):
    try:
        user = User.objects.get(digital_signature_verification_token=uid)
        user.is_digital_signature_verified = True
        user.save()
        return Response(
            {
                "status": "success",
                "message": "Digital Signature Verified successfully.",
            },
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"status": "error", "message": "Invalid token."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        logger.error(e)
        return Response(
            {"status": "error", "message": "An error occured."},
            status=status.HTTP_400_BAD_REQUEST,
        )
