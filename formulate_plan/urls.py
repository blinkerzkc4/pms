"""
-- Created by Bikash Saud
--
-- Created on 2023-06-18
"""

from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(
    "work-class",
    views.WorkClassViewSet,
    basename="work_class",
)
router.register(
    "project-work-type",
    views.ProjectWorkTypeViewSet,
    basename="project_work_type",
)
router.register("project-work", views.WorkProjectViewSet, basename="project_work")
router.register(
    "project-work-document",
    views.WorkProjectDocumentViewSet,
    basename="project_work_document",
)

urlpatterns = router.urls
