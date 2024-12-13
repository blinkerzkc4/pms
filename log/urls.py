from django.urls import include, path
from rest_framework.routers import DefaultRouter

from log.views import UserActivityChangesViewSet, UserActivityViewSet

from . import views

router = DefaultRouter()
router.register(r"user-activity", UserActivityViewSet, basename="user-activity")
router.register(
    r"user-activity-changes",
    UserActivityChangesViewSet,
    basename="user-activity-changes",
)

urlpatterns = [
    path("", include(router.urls)),
    path("", views.AccessLogListView.as_view(), name="log-list"),
    path("<int:pk>/", views.AccessLogDetailView.as_view(), name="log-detail"),
]
