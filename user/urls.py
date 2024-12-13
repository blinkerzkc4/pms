from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"permissions", views.PermissionViewSet, basename="permission")
router.register(r"user-roles", views.UserRoleViewSet, basename="user-roles")

urlpatterns = router.urls
urlpatterns += [
    path("profile/", views.profile, name="profile"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path(
        "permissions_old/", views.PermissionListView.as_view(), name="permission-list"
    ),
    path("users/<int:pk>/", views.UserView.as_view(), name="users"),
    path(
        "users/deactivate/<int:pk>/",
        views.DeactivateUserView.as_view(),
        name="deactivate-user",
    ),
    path(
        "users/activate/<int:pk>/",
        views.ActivateUserView.as_view(),
        name="activate-user",
    ),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("clients/", views.ClientListView.as_view(), name="client-list"),
    path("clients/<int:pk>/", views.ClientView.as_view(), name="client"),
    # digital signature stuffs
    path(
        "verify-digital-signature/<uuid:uid>/",
        views.verify_digital_signature,
        name="verify-digital-signature",
    ),
    path(
        "add-digital-signature/",
        views.add_digital_signature,
        name="add-digital-signature",
    ),
    path(
        "remove-digital-signature/",
        views.remove_digital_signature,
        name="remove-digital-signature",
    ),
]
