import logging
from typing import List, Optional, TypedDict

from django.db.models import Model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from project.models import BaseModel

logger = logging.getLogger("Base Model Viewsets")


class MunicipalityFilteredViewSet(ModelViewSet):
    model: BaseModel
    filter_by_municipality = False
    filter_inactive_models = False
    municipality_field_name = "municipality"
    block_deleting_if_used_in_relation = True

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if self.block_deleting_if_used_in_relation and instance.is_used_in_relation:
            return Response(
                {
                    "success": False,
                    "message": f"You cannot delete this {self.model._meta.verbose_name} as it is used in other forms.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        filter_kwargs = {}
        queryset = self.model.objects.all()
        display_inactive_models = (
            self.request.query_params.get("display_inactive_models") == "1"
        )
        if self.filter_by_municipality:
            filter_kwargs[
                f"{self.municipality_field_name}__project__municipality"
            ] = self.request.user.assigned_municipality
        if self.filter_inactive_models and not display_inactive_models:
            filter_kwargs["status"] = True
        return queryset.filter(**filter_kwargs)


class MunicipalityAndProjectFilteredViewSet(MunicipalityFilteredViewSet):
    project_required = False
    return_only_one = False
    send_data_directly = False
    is_project_process = False
    block_multiple_object_creation = False
    project_execution_field_name = "project"
    municipality_field_name = f"{project_execution_field_name}__municipality"

    def get_queryset(self):
        project_id = self.request.query_params.get("project_id")
        display_all = self.request.query_params.get("display_all") == "1"
        queryset = super().get_queryset()
        if project_id and not display_all:
            queryset = self.filter_with_project(queryset)
        return queryset

    def filter_with_project(self, queryset=None):
        project_id = self.request.query_params.get("project_id")
        if project_id:
            queryset = queryset.filter(
                **{(f"{self.project_execution_field_name}__id"): project_id}
            )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.order_by("id")
        # Checking if the request if is for a single object
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if (
            lookup_url_kwarg not in self.kwargs.keys()
            and self.return_only_one
            and not self.send_data_directly
        ):
            queryset = queryset[:1]
        return queryset

    def create(self, request, *args, **kwargs):
        if (
            self.is_project_process
            and self.block_multiple_object_creation
            and self.model.objects.filter(
                **{
                    (f"{self.project_execution_field_name}__id"): request.data.get(
                        "project"
                    )
                }
            ).exists()
        ):
            return Response(
                {
                    "success": False,
                    "message": f"You cannot create more than one object for this form.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        project_id = self.request.query_params.get("project_id")
        if self.project_required and not project_id:
            return Response(
                {"detail": "project_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if self.is_project_process and self.send_data_directly:
            queryset = self.filter_queryset(self.get_queryset())
            if queryset.exists():
                serializer = self.get_serializer(queryset.first())
                return Response(serializer.data)
            return Response(
                {"detail": "No data found"}, status=status.HTTP_404_NOT_FOUND
            )
        return super().list(request, *args, **kwargs)


class MultipleObjectSupportViewSet(MunicipalityAndProjectFilteredViewSet):
    class ForeignKeyFields(TypedDict):
        field_name_in_model: str
        pk_field_name: str

    foreign_key_fields: List[ForeignKeyFields] = []

    def get_object_payloads(self, request):
        operation_with_object_payloads = {
            "new": request.data.get("new", []),
            "updated": request.data.get("updated", []),
            "deleted": request.data.get("deleted", []),
        }
        object_payloads = []
        # Adding new object payloads to processes_payloads
        object_payloads.extend(
            [
                {**object_data, "id": None, "object_payload_task": "new"}
                for object_data in operation_with_object_payloads["new"]
            ]
        )
        # Adding updated object payloads to processes_payloads
        object_payloads.extend(
            [
                {**object_data, "object_payload_task": "updated"}
                for object_data in operation_with_object_payloads["updated"]
            ]
        )
        # Adding deleted object payloads to processes_payloads
        object_payloads.extend(
            [
                {**object_data, "object_payload_task": "deleted"}
                for object_data in operation_with_object_payloads["deleted"]
            ]
        )

        for object_payload in object_payloads:
            for foreign_key_field in self.foreign_key_fields:
                if isinstance(
                    object_payload.get(foreign_key_field["field_name_in_model"]), dict
                ):
                    object_payload[
                        foreign_key_field["field_name_in_model"]
                    ] = object_payload.get(
                        foreign_key_field["field_name_in_model"], {}
                    ).get(
                        foreign_key_field["pk_field_name"]
                    )

        return object_payloads

    def create_object(self, object_payload_data):
        serializer = self.get_serializer(data=object_payload_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return True

    def update_object(self, object_payload_data):
        try:
            instance = self.model.objects.get(id=object_payload_data["id"])
        except self.model.DoesNotExist or KeyError as e:
            logger.error(e)
            return False
        serializer = self.get_serializer(
            instance, data=object_payload_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return True

    def delete_object(self, object_payload_data):
        try:
            instance = self.model.objects.get(id=object_payload_data["id"])
        except self.model.DoesNotExist as e:
            logger.error(e)
            return False
        self.perform_destroy(instance)
        return True

    def get_object_payload_message(self, object_payload_data, status):
        if status:
            if object_payload_data["object_payload_task"] == "new":
                return f"Created {self.model._meta.verbose_name}"
            elif object_payload_data["object_payload_task"] == "updated":
                return f"Updated {self.model._meta.verbose_name} with id {object_payload_data['id']}"
            elif object_payload_data["object_payload_task"] == "deleted":
                return f"Deleted {self.model._meta.verbose_name} with id {object_payload_data['id']}"
        else:
            if object_payload_data["object_payload_task"] == "new":
                return f"Failed to create {self.model._meta.verbose_name}"
            elif object_payload_data["object_payload_task"] == "updated":
                return f"Failed to update {self.model._meta.verbose_name} with id {object_payload_data['id']}"
            elif object_payload_data["object_payload_task"] == "deleted":
                return f"Failed to delete {self.model._meta.verbose_name} with id {object_payload_data['id']}"

    def process_payload(self, request):
        object_payloads = self.get_object_payloads(request)
        payload_process_message = []
        # Processing object payloads
        for object_data in object_payloads:
            status = False
            object_payload_task = object_data.get("object_payload_task")
            if object_payload_task == "deleted":
                status = self.delete_object(object_data)
            elif object_payload_task == "updated":
                status = self.update_object(object_data)
            elif object_payload_task == "new":
                status = self.create_object(object_data)
            payload_process_message.append(
                self.get_object_payload_message(object_data, status)
            )
        return payload_process_message

    def create(self, request, *args, **kwargs):
        payload_process_messages = self.process_payload(request)
        for payload_process_message in payload_process_messages:
            print(payload_process_message)
        return Response(
            {"success": True, "message": payload_process_messages},
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        payload_process_messages = self.process_payload(request)
        for payload_process_message in payload_process_messages:
            print(payload_process_message)
        return Response(
            {"success": True, "message": payload_process_messages},
            status=status.HTTP_200_OK,
        )


class ChildCreationSupportViewSet(MunicipalityAndProjectFilteredViewSet):
    class ChildPayloadProperty(TypedDict):
        model: Model
        serializer_class: ModelSerializer
        child_name: str
        parent_name: str
        key_in_payload: Optional[str]

    child_payload_properties: List[ChildPayloadProperty] = []

    def get_child_payloads(self, request, parent_id):
        if parent_id is None:
            parent_id = request.data.get("id")
        all_child_payloads = []
        for child_payload_property in self.child_payload_properties:
            child_payload = request.data.get(
                child_payload_property.get(
                    "key_in_payload", child_payload_property["child_name"]
                ),
                {},
            )
            if isinstance(child_payload, list):
                continue
            child_payloads = {
                "new": child_payload.get("new", []),
                "updated": child_payload.get("updated", []),
                "deleted": child_payload.get("deleted", []),
            }
            processed_child_payloads = []
            # Adding new child payloads to processed_child_payloads
            processed_child_payloads.extend(
                [
                    {
                        **child_data,
                        "id": None,
                        child_payload_property["parent_name"]: str(parent_id),
                        "child_payload_task": "new",
                        "child_payload_property": child_payload_property,
                    }
                    for child_data in child_payloads["new"]
                ]
            )
            # Adding updated child payloads to processed_child_payloads
            processed_child_payloads.extend(
                [
                    {
                        **child_data,
                        "child_payload_task": "updated",
                        "child_payload_property": child_payload_property,
                    }
                    for child_data in child_payloads["updated"]
                ]
            )
            # Adding deleted child payloads to processed_child_payloads
            processed_child_payloads.extend(
                [
                    {
                        **child_data,
                        "child_payload_task": "deleted",
                        "child_payload_property": child_payload_property,
                    }
                    for child_data in child_payloads["deleted"]
                ]
            )
            all_child_payloads.extend(processed_child_payloads)
        return all_child_payloads

    def get_child_payload_message(self, child_payload_data, status):
        child_model = child_payload_data.get("child_payload_property").get("model")
        if status:
            if child_payload_data["child_payload_task"] == "new":
                return f"Created {child_model._meta.verbose_name}"
            elif child_payload_data["child_payload_task"] == "updated":
                return f"Updated {child_model._meta.verbose_name} with id {child_payload_data['id']}"
            elif child_payload_data["child_payload_task"] == "deleted":
                return f"Deleted {child_model._meta.verbose_name} with id {child_payload_data['id']}"
        else:
            if child_payload_data["child_payload_task"] == "new":
                return f"Failed to create {child_model._meta.verbose_name}"
            elif child_payload_data["child_payload_task"] == "updated":
                return f"Failed to update {child_model._meta.verbose_name} with id {child_payload_data['id']}"
            elif child_payload_data["child_payload_task"] == "deleted":
                return f"Failed to delete {child_model._meta.verbose_name} with id {child_payload_data['id']}"

    def delete_child(self, child_payload_data):
        child_model = child_payload_data.get("child_payload_property").get("model")
        try:
            instance = child_model.objects.get(id=child_payload_data["id"])
        except child_model.DoesNotExist as e:
            logger.error(e)
            return False
        self.perform_destroy(instance)
        return True

    def update_child(self, child_payload_data):
        print(child_payload_data)
        child_model = child_payload_data.get("child_payload_property").get("model")
        child_serializer_class = child_payload_data.get("child_payload_property").get(
            "serializer_class"
        )
        try:
            instance = child_model.objects.get(id=child_payload_data["id"])
        except child_model.DoesNotExist or KeyError as e:
            logger.error(e)
            return False
        serializer = child_serializer_class(
            instance, data=child_payload_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return True

    def create_child(self, child_payload_data):
        child_serializer_class = child_payload_data.get("child_payload_property").get(
            "serializer_class"
        )
        serializer = child_serializer_class(data=child_payload_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return True

    def process_child_payloads(self, request, parent_id=None):
        child_payloads = self.get_child_payloads(request, parent_id)
        payload_process_message = []
        # Processing child payloads
        for child_data in child_payloads:
            status = False
            child_payload_task = child_data.get("child_payload_task")
            if child_payload_task == "deleted":
                status = self.delete_child(child_data)
            elif child_payload_task == "updated":
                status = self.update_child(child_data)
            elif child_payload_task == "new":
                status = self.create_child(child_data)
            payload_process_message.append(
                self.get_child_payload_message(child_data, status)
            )
        return payload_process_message

    def create(self, request, *args, **kwargs):
        if self.is_project_process and self.block_multiple_object_creation:
            if self.model.objects.filter(
                project__id=request.data.get("project")
            ).exists():
                return Response(
                    {
                        "success": False,
                        "message": f"You cannot create more than one object for this form.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent_object = serializer.save()
        headers = self.get_success_headers(serializer.data)
        payload_process_messages = self.process_child_payloads(
            request, parent_object.id
        )
        for payload_process_message in payload_process_messages:
            print(payload_process_message)
        logger.info(payload_process_messages)
        return Response(
            self.get_serializer(parent_object).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def update(self, request, *args, **kwargs):
        payload_process_messages = self.process_child_payloads(request)
        for payload_process_message in payload_process_messages:
            print(payload_process_message)
        return super().update(request, *args, **kwargs)
