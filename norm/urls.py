from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register("norms", views.NormViewSet, basename="norms")
router.register("norm-costs", views.NormExtraCostViewSet, basename="norm-costs")
router.register("norm-activity", views.NormActivityViewSet, basename="norm-activity")
router.register(
    "norm-activity-type", views.ActivityTypeViewSet, basename="norm-activity-type"
)
router.register(
    "norm-components", views.NormComponentViewSet, basename="norm-components"
)
urlpatterns = router.urls
