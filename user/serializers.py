import string

from django.contrib.auth.models import Group
from rest_framework import serializers

from employee.models import Department
from project.models import Municipality, Ward
from project.serializers import (
    MunicipalitySerializer,
    SimpleMunicipalitySerializer,
    SimpleWardSerializer,
)
from user.choices import RoleLevelChoices
from user.models import Client, Permission, User, UserRole

LETTERS = string.ascii_letters + string.punctuation + string.digits


class PermissionSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ["level", "children", "name", "name_eng", "code", "title", "parent"]

    def get_children(self, obj):
        queryset = Permission.objects.none()
        request = self.context.get("request")
        context = {}
        if request and request.user.is_authenticated:
            user = request.user
            if user.is_superuser:
                queryset = obj.children.all()
            else:
                queryset = obj.children.filter(granted_roles__users=user).distinct()
            context["request"] = request
        return PermissionSerializer(queryset, context=context, many=True).data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserRoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="code"
    )
    grant_permissions = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )

    def validate(self, data):
        # permissions = data.get("grant_permissions", [])
        # disallowed_permissions = get_disallowed_permissions()
        # common_permission = set(permissions) & set(disallowed_permissions)
        # if common_permission:
        #     raise serializers.ValidationError(
        #         f"Permission {common_permission} cannot be granted"
        #     )
        return super().validate(data)

    def create(self, validated_data):
        permissions = validated_data.pop("grant_permissions", [])
        role = super().create(validated_data)
        role.permissions.clear()
        role.permissions.add(*Permission.objects.filter(code__in=permissions))
        role.save()
        return role

    def update(self, instance, validated_data):
        permissions = validated_data.pop("grant_permissions", [])
        role = super().update(instance, validated_data)
        role.permissions.clear()
        role.permissions.add(*Permission.objects.filter(code__in=permissions))
        role.save()
        return role

    class Meta:
        model = UserRole
        fields = "__all__"


class UserSerializerForToken(serializers.ModelSerializer):
    ward = SimpleWardSerializer(source="assigned_ward", read_only=True)
    municipality = SimpleMunicipalitySerializer(
        source="assigned_municipality", read_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        photo_uri = data["profile_picture"]
        if photo_uri:
            request = self.context.get("request")
            try:
                data["profile_picture"] = request.build_absolute_uri(photo_uri)

            except:
                data["profile_picture"] = photo_uri
        digital_signature_uri = data["digital_signature"]
        if digital_signature_uri:
            request = self.context.get("request")
            try:
                data["digital_signature"] = request.build_absolute_uri(
                    digital_signature_uri
                )

            except:
                data["digital_signature"] = digital_signature_uri

        return data

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "eoffice_reference_code",
            "notification_room_id",
            "email",
            "is_staff",
            "is_active",
            "verified",
            "role_level",
            "ward",
            "municipality",
            "profile_picture",
            "last_login",
            "ip_address",
            "full_name",
            "has_signature",
            "is_digital_signature_verified",
            "digital_signature",
            "status",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "is_staff": {"required": False, "allow_null": True},
            "is_active": {"required": False, "allow_null": True},
            "verified": {"required": False, "allow_null": True},
            "role_level": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "profile_picture": {"required": False, "allow_null": True},
            "last_login": {"required": False, "allow_null": True},
            "ip_address": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "has_signature": {"required": False, "allow_null": True},
            "is_digital_signature_verified": {"required": False, "allow_null": True},
            "digital_signature": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class UserSerializer(serializers.ModelSerializer):
    ward = SimpleWardSerializer(source="assigned_ward", read_only=True)
    municipality = MunicipalitySerializer(
        source="assigned_municipality", read_only=True
    )
    role = UserRoleSerializer(source="user_role", many=True, read_only=True)
    user_role = serializers.PrimaryKeyRelatedField(
        queryset=UserRole.objects.all(), many=True, required=False, write_only=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        photo_uri = data["profile_picture"]
        if photo_uri:
            request = self.context.get("request")
            try:
                data["profile_picture"] = request.build_absolute_uri(photo_uri)

            except:
                data["profile_picture"] = None

        return data

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_staff",
            "is_active",
            "verified",
            "role_level",
            "user_role",
            "ward",
            "municipality",
            "role",
            "assigned_ward",
            "assigned_municipality",
            "assigned_department",
            "detail",
            "profile_picture",
            "last_login",
            "ip_address",
            "full_name",
            "has_signature",
            "is_digital_signature_verified",
            "status",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "is_staff": {"required": False, "allow_null": True},
            "is_active": {"required": False, "allow_null": True},
            "verified": {"required": False, "allow_null": True},
            "role_level": {"required": False, "allow_null": True},
            "user_role": {"required": False, "allow_null": True},
            "ward": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "role": {"required": False, "allow_null": True},
            "assigned_ward": {"required": False, "allow_null": True},
            "assigned_municipality": {"required": False, "allow_null": True},
            "detail": {"required": False, "allow_null": True},
            "profile_picture": {"required": False, "allow_null": True},
            "last_login": {"required": False, "allow_null": True},
            "ip_address": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "has_signature": {"required": False, "allow_null": True},
            "is_digital_signature_verified": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = (
            "assigned_municipality",
            "is_staff",
            "assigned_department",
            "is_active",
            "verified",
            "assigned_ward",
            "has_signature",
            "is_digital_signature_verified",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def get_user(self):
        try:
            user = self.context.get("request").user
        except:
            raise serializers.ValidationError("Fuck")
        return user

    def validate_old_password(self, old_password):
        user = self.get_user()
        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid password provided")
        return old_password

    # def validate_new_password(self, new_password):
    #     import django.contrib.auth.password_validation as validators

    #     user = self.get_user()

    #     try:
    #         validators.validate_password(new_password, user=user)
    #     except Exception as e:
    #         print(e)
    #         raise serializers.ValidationError(f"Password too weak. {e}")

    #     return new_password

    def validate(self, data):
        new_password = data.get("new_password")
        old_password = data.get("old_password")
        confirm_password = data.get("confirm_password")
        print(new_password, old_password, confirm_password, data)
        if new_password == old_password:
            raise serializers.ValidationError(
                "New password cannot be same as old password"
            )
        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New passowrd and the confirmation should be the same"
            )
        return data


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializers class for User model
    """

    user_role = serializers.PrimaryKeyRelatedField(
        queryset=UserRole.objects.all(),
        many=True,
        required=False,
        write_only=True,
        allow_null=True,
    )
    assigned_municipality = serializers.PrimaryKeyRelatedField(
        queryset=Municipality.objects.all(),
        required=False,
        write_only=True,
        allow_null=True,
    )
    assigned_ward = serializers.PrimaryKeyRelatedField(
        queryset=Ward.objects.all(), required=False, write_only=True, allow_null=True
    )
    assigned_department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        required=False,
        write_only=True,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "role_level",
            "full_name",
            "assigned_municipality",
            "assigned_department",
            "assigned_ward",
            "user_role",
            "status",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_null": True},
            "role_level": {"required": False, "allow_null": True},
            "assigned_municipality": {"required": False, "allow_null": True},
            "full_name": {"required": False, "allow_null": True},
            "assigned_ward": {"required": False, "allow_null": True},
            "user_role": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def validate_email(self, email):
        users = User.objects.filter(username=email)

        if users.exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    def validate(self, data):
        role_level = data.get("role_level")
        if role_level == RoleLevelChoices.WARD:
            ward = data.get("assigned_ward")
            if ward is None:
                raise serializers.ValidationError("Ward is needed for ward user")
        if role_level == RoleLevelChoices.DEPARTMENT:
            department = data.get("assigned_department")
            if department is None:
                raise serializers.ValidationError(
                    "Department is needed for department user"
                )
        return super().validate(data)

    def create(self, validated_data):
        """
        If user type is partner  and is root user assign default created roles and same case for admin user as well
        """
        validated_data["username"] = validated_data["email"]
        # roles = validated_data.get("roles", None)

        user_role = validated_data.pop("user_role")

        user = User.objects.create(**validated_data)
        password = User.objects.make_random_password()
        password = "admin"
        # user.roles = roles
        user.set_password(password)
        user.verified = True
        user.user_role.set(user_role)
        user.save()

        # send_user_credentials_email(user, password)

        return user


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "status",
        )
        extra_kwargs = {
            "username": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ClientSerializer(serializers.ModelSerializer):
    municipality = SimpleMunicipalitySerializer(read_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "client_id",
            "municipality",
            "subdomain",
            "created_date",
            "status",
            "active",
            "logo",
        )
        extra_kwargs = {
            "municipality": {"required": False, "allow_null": True},
            "subdomain": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "active": {"required": False, "allow_null": True},
        }
        read_only_fields = ("active", "logo")


class ClientSuperAdminViewSerializer(serializers.ModelSerializer):
    municipality = SimpleMunicipalitySerializer(read_only=True)
    email = serializers.EmailField(read_only=True, source="main_admin.email")

    class Meta:
        model = Client
        fields = (
            "id",
            "municipality",
            "client_id",
            "subdomain",
            "created_date",
            "email",
            "valid_till",
            "status",
            "active",
            "logo",
            "database_host",
            "database_name",
            "database_user",
            "database_password",
            "database_port",
        )
        extra_kwargs = {
            "municipality": {"required": False, "allow_null": True},
            "subdomain": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "valid_till": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "active": {"required": False, "allow_null": True},
            "database_host": {"read_only": True},
            "database_name": {"read_only": True},
            "database_user": {"read_only": True},
            "database_password": {"read_only": True},
            "database_port": {"read_only": True},
        }


class ClientCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = Client
        fields = (
            "municipality",
            "subdomain",
            "email",
            "status",
            "database_host",
            "database_name",
            "database_user",
            "database_password",
            "database_port",
        )
        extra_kwargs = {
            "municipality": {"required": False, "allow_null": True},
            "subdomain": {"required": False, "allow_null": True},
            "email": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "database_host": {"required": False, "allow_null": True},
            "database_name": {"required": False, "allow_null": True},
            "database_user": {"required": False, "allow_null": True},
            "database_password": {"required": False, "allow_null": True},
            "database_port": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        user_creation_data = {
            "email": validated_data.pop("email"),
            "assigned_municipality": validated_data.get("municipality").pk,
            "assigned_ward": None,
            "user_role": [],
        }
        main_admin_user = UserCreateSerializer(data=user_creation_data)
        main_admin_user.is_valid(raise_exception=True)
        main_admin_user = main_admin_user.save()
        validated_data["main_admin"] = main_admin_user

        client = Client.objects.create(**validated_data)
        return client
