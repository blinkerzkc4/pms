from rest_framework import serializers

from base_model.base_serializers import BaseSerializer
from utils.serializers import RecursiveField
from .models import (
    District,
    Estimate,
    EstimationRate,
    FederalType,
    FinancialYear,
    JDComment,
    JobDescription,
    JobDescriptionFile,
    Municipality,
    Project,
    ProjectCategory,
    Province,
    Quantity,
    Rate,
    RateArea,
    RateCategory,
    RateSource,
    SummaryExtra,
    Topic,
    Unit,
    Ward,
)


class FederalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederalType
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "code",
            "status",
            "upper_federal_type",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProvinceSerializer(serializers.ModelSerializer):
    federal_type = FederalTypeSerializer(read_only=True)

    class Meta:
        model = Province
        fields = (
            "id",
            "name",
            "name_eng",
            "province_number",
            "name_unicode",
            "code",
            "federal_type",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "province_number": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class DistrictSerializer(serializers.ModelSerializer):
    federal_type = FederalTypeSerializer(read_only=True)

    class Meta:
        model = District
        fields = (
            "id",
            "name",
            "federal_type",
            "name_eng",
            "name_unicode",
            "code",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SimpleWardSerializer(BaseSerializer):
    class Meta:
        model = Ward
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "ward_number",
            "status",
        )
        extra_kwargs = {
            "ward_number": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SimpleProvinceSerializer(serializers.ModelSerializer):
    federal_type = serializers.CharField(source="federal_type.code", read_only=True)

    class Meta:
        model = Province
        fields = (
            "id",
            "name",
            "federal_type",
            "name_eng",
            "name_unicode",
            "code",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SimpleDistrictSerializer(serializers.ModelSerializer):
    federal_type = serializers.CharField(source="federal_type.code", read_only=True)

    class Meta:
        model = District
        fields = (
            "id",
            "name",
            "federal_type",
            "name_eng",
            "name_unicode",
            "code",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SimpleMunicipalitySerializer(serializers.ModelSerializer):
    district = SimpleDistrictSerializer(read_only=True)
    province = SimpleProvinceSerializer(source="district.province", read_only=True)
    federal_type = serializers.CharField(source="federal_type.code", read_only=True)

    class Meta:
        model = Municipality
        fields = (
            "id",
            "code",
            "name",
            "name_eng",
            "federal_type",
            "name_unicode",
            "district",
            "province",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "district": {"required": False, "allow_null": True},
            "province": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class WardSerializer(BaseSerializer):
    municipality = SimpleMunicipalitySerializer(read_only=True)
    district = DistrictSerializer(source="municipality.district", read_only=True)
    province = ProvinceSerializer(
        source="municipality.district.province", read_only=True
    )

    class Meta:
        model = Ward
        fields = (
            "id",
            "ward_number",
            "name",
            "name_eng",
            "name_unicode",
            "created_by",
            "created_date",
            "updated_date",
            "status",
            "municipality",
            "district",
            "province",
        )
        extra_kwargs = {
            "ward_number": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "updated_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "district": {"required": False, "allow_null": True},
            "province": {"required": False, "allow_null": True},
        }
        read_only_fields = (
            "created_by",
            "created_date",
            "updated_date",
            "status",
        )


class MunicipalitySerializer(serializers.ModelSerializer):
    wards = SimpleWardSerializer(source="ward_set", many=True, read_only=True)

    district = DistrictSerializer(read_only=True)
    province = ProvinceSerializer(source="district.province", read_only=True)
    federal_type = FederalTypeSerializer(read_only=True)

    class Meta:
        model = Municipality
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "created_by",
            "created_date",
            "federal_type",
            "code",
            "updated_date",
            "status",
            "wards",
            "district",
            "province",
            "number_of_wards",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "updated_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "wards": {"required": False, "allow_null": True},
            "district": {"required": False, "allow_null": True},
            "province": {"required": False, "allow_null": True},
            "number_of_wards": {"required": False, "allow_null": True},
        }
        read_only_fields = (
            "district",
            "created_by",
            "created_date",
            "updated_date",
            "ward_set",
            "status",
        )


class JobDescriptionFileBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescriptionFile

        fields = (
            "id",
            "file_type",
            "file",
            "status",
        )
        extra_kwargs = {
            "file_type": {"required": False, "allow_null": True},
            "file": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class JobDescriptionBasicSerializer(serializers.ModelSerializer):
    files = JobDescriptionFileBasicSerializer(many=True, read_only=True)

    class Meta:
        model = JobDescription
        fields = (
            "id",
            "title",
            "files",
            "description",
            "status",
        )
        extra_kwargs = {
            "title": {"required": False, "allow_null": True},
            "files": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class JobDescriptionSerializer(serializers.ModelSerializer):
    files = JobDescriptionFileBasicSerializer(many=True, read_only=True)

    file = serializers.FileField(allow_empty_file=True, write_only=True)
    file_type = serializers.CharField(max_length=255, allow_blank=True, write_only=True)

    class Meta:
        model = JobDescription
        fields = (
            "id",
            "title",
            "project",
            "description",
            "status",
            "files",
            "created_date",
            "file",
            "file_type",
            "status_of_model",
        )
        extra_kwargs = {
            "title": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
            "files": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "file": {"required": False, "allow_null": True},
            "file_type": {"required": False, "allow_null": True},
            "status_of_model": {"required": False, "allow_null": True},
        }
        read_only_fields = ("files", "status")

    def create(self, validated_data):
        file = validated_data.pop("file", None)
        file_type = validated_data.pop("file_type", None)
        instance = super().create(validated_data)
        if file and file_type:
            JobDescriptionFile.objects.create(
                job_description=instance, file_type=file_type, file=file
            )
        return instance


class JobDescriptionFileSerializer(serializers.ModelSerializer):
    job_description = JobDescriptionBasicSerializer()

    class Meta:
        model = JobDescriptionFile

        fields = (
            "id",
            "file",
            "file_type",
            "job_description",
            "created_date",
            "status",
        )
        extra_kwargs = {
            "file": {"required": False, "allow_null": True},
            "file_type": {"required": False, "allow_null": True},
            "job_description": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = (
            "id",
            "name",
            "name_unicode",
            "name_eng",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    category = ProjectCategorySerializer()

    job_descriptions = JobDescriptionBasicSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.financial_year:
            data["financial_year"] = {
                "id": instance.financial_year.id,
                "start_year": instance.financial_year.start_year,
                "end_year": instance.financial_year.end_year,
                "fy": instance.financial_year.fy,
            }
        return data

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "category",
            "job_descriptions",
            "created_date",
            "financial_year",
            "estimate",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "category": {"required": False, "allow_null": True},
            "job_descriptions": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "estimate": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class ProjectCopySerializer(serializers.Serializer):
    from_project = serializers.IntegerField()
    to_project = serializers.IntegerField()


class JDCommentSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source="created_by.username")

    class Meta:
        model = JDComment

        fields = (
            "id",
            "text",
            "job_description",
            "created_by",
            "created_date",
            "updated_date",
            "created_by",
            "status",
        )
        extra_kwargs = {
            "text": {"required": False, "allow_null": True},
            "job_description": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "created_date": {"required": False, "allow_null": True},
            "updated_date": {"required": False, "allow_null": True},
            "created_by": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("created_by",)


class TopicSerializer(serializers.ModelSerializer):
    parent = RecursiveField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["full_name_eng"] = instance._name_eng
        data["full_name"] = instance._name
        data["full_name_unicode"] = instance._name_unicode
        return data

    class Meta:
        model = Topic
        fields = (
            "id",
            "name_eng",
            "name",
            "name_unicode",
            "parent",
            "status",
        )
        extra_kwargs = {
            "name_eng": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ("id", "name", "name_unicode", "name_eng", "remarks", "status", "code")
        read_only_fields = ("municipality",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["name"] = instance.name or instance.name_eng
        return data


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateArea
        fields = ("id", "name", "name_unicode", "name_eng", "remarks", "status")
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class RateSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateSource
        fields = (
            "id",
            "name",
            "name_unicode",
            "name_eng",
            "remarks",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class RateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCategory
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "municipality",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("municipality",)


class SimpleRateSerializer(serializers.ModelSerializer):
    fy = serializers.CharField(source="financial_year.fy", read_only=True)
    rate_category = RateCategorySerializer(read_only=True)

    topic = serializers.SerializerMethodField()
    sub_topic = serializers.SerializerMethodField()
    item = serializers.SerializerMethodField()

    topic_unicode = serializers.SerializerMethodField()
    sub_topic_unicode = serializers.SerializerMethodField()
    item_unicode = serializers.SerializerMethodField()

    topic_id = serializers.SerializerMethodField()
    sub_topic_id = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()

    level = serializers.IntegerField(source="topic.level")

    class Meta:
        model = Rate
        fields = (
            "id",
            "financial_year",
            "fy",
            "rate_category",
            "item",
            "item_id",
            "item_unicode",
            "sub_topic",
            "sub_topic_id",
            "sub_topic_unicode",
            "topic",
            "topic_id",
            "topic_unicode",
            "level",
            "amount",
            "status",
        )
        extra_kwargs = {
            "financial_year": {"required": False, "allow_null": True},
            "fy": {"required": False, "allow_null": True},
            "rate_category": {"required": False, "allow_null": True},
            "item": {"required": False, "allow_null": True},
            "item_id": {"required": False, "allow_null": True},
            "item_unicode": {"required": False, "allow_null": True},
            "sub_topic": {"required": False, "allow_null": True},
            "sub_topic_id": {"required": False, "allow_null": True},
            "sub_topic_unicode": {"required": False, "allow_null": True},
            "topic": {"required": False, "allow_null": True},
            "topic_id": {"required": False, "allow_null": True},
            "topic_unicode": {"required": False, "allow_null": True},
            "level": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def get_object(self, obj, obj_type, field):
        try:
            level = obj.topic.level
            ot = (obj_type, level)
            if ot == ("ITEM", 2):
                topic = obj.topic
            elif ot == ("ITEM", 3):
                topic = obj.topic
            elif ot == ("TOPIC", 1):
                topic = obj.topic
            elif ot == ("TOPIC", 2):
                topic = obj.topic.parent
            elif ot == ("TOPIC", 3):
                topic = obj.topic.parent.parent
            elif ot == ("SUB_TOPIC", 3):
                topic = obj.topic.parent
            else:
                topic = None
        except Exception as e:
            print(e)
            topic = None
        return getattr(topic, field, "")

    def get_topic(self, obj):
        return self.get_object(obj, "TOPIC", "name_eng")

    def get_sub_topic(self, obj):
        return self.get_object(obj, "SUB_TOPIC", "name_eng")

    def get_item(self, obj):
        return self.get_object(obj, "ITEM", "name_eng")

    def get_topic_unicode(self, obj):
        return self.get_object(obj, "TOPIC", "name_unicode")

    def get_sub_topic_unicode(self, obj):
        return self.get_object(obj, "SUB_TOPIC", "name_unicode")

    def get_item_unicode(self, obj):
        return self.get_object(obj, "ITEM", "name_unicode")

    def get_topic_id(self, obj):
        return self.get_object(obj, "TOPIC", "id")

    def get_sub_topic_id(self, obj):
        return self.get_object(obj, "SUB_TOPIC", "id")

    def get_item_id(self, obj):
        return self.get_object(obj, "ITEM", "id")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data[
            "rate_eng"
        ] = f'{data["topic"]}  {data["sub_topic"]}  {data["item"]}'.strip()
        data[
            "rate_unicode"
        ] = f'{data["topic_unicode"]}  {data["sub_topic_unicode"]}  {data["item_unicode"]}'.strip()
        return data


class EstimationRateSerializer(serializers.ModelSerializer):
    """
    Amount is the amount in Paisa
    """

    unit_value = UnitSerializer(source="unit", read_only=True)
    rate_value = SimpleRateSerializer(source="rate", read_only=True)

    class Meta:
        model = EstimationRate
        fields = (
            "id",
            "rate",
            "rate_value",
            "length",
            "breadth",
            "height",
            "area",
            "quantity",
            "unit",
            "amount",
            "amount_rs",
            "project",
            "road_1_distance",
            "road_2_distance",
            "road_3_distance",
            "road_1_amount",
            "road_2_amount",
            "road_3_amount",
            "transportation_rate",
            "total_rate",
            "part_name",
            "unit_value",
            "status",
        )
        extra_kwargs = {
            "rate": {"required": False, "allow_null": True},
            "rate_value": {"required": False, "allow_null": True},
            "length": {"required": False, "allow_null": True},
            "breadth": {"required": False, "allow_null": True},
            "height": {"required": False, "allow_null": True},
            "area": {"required": False, "allow_null": True},
            "quantity": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "amount_rs": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "road_1_distance": {"required": False, "allow_null": True},
            "road_2_distance": {"required": False, "allow_null": True},
            "road_3_distance": {"required": False, "allow_null": True},
            "road_1_amount": {"required": False, "allow_null": True},
            "road_2_amount": {"required": False, "allow_null": True},
            "road_3_amount": {"required": False, "allow_null": True},
            "transportation_rate": {"required": False, "allow_null": True},
            "total_rate": {"required": False, "allow_null": True},
            "part_name": {"required": False, "allow_null": True},
            "unit_value": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("unit_value", "rate_value")

    def get_transportation_rate(self, obj):
        return obj.transportation_rate

    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            data["transportation_rate"] = instance.transportation_rate
        except:
            pass
        return data


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = (
            "id",
            "title",
            "project",
            "file",
            "road_1_rate",
            "road_2_rate",
            "road_3_rate",
            "summary_of_project",
            "abstract_of_cost",
            "summary_of_rates",
            "district_rate",
            "transportation_of_material",
            "rate_analysis_of_general_work",
            "detailed_quantity_calculation",
            "material_cost_with_transport",
            "status",
        )
        extra_kwargs = {
            "title": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "file": {"required": False, "allow_null": True},
            "road_1_rate": {"required": False, "allow_null": True},
            "road_2_rate": {"required": False, "allow_null": True},
            "road_3_rate": {"required": False, "allow_null": True},
            "summary_of_project": {"required": False, "allow_null": True},
            "abstract_of_cost": {"required": False, "allow_null": True},
            "summary_of_rates": {"required": False, "allow_null": True},
            "district_rate": {"required": False, "allow_null": True},
            "transportation_of_material": {"required": False, "allow_null": True},
            "rate_analysis_of_general_work": {"required": False, "allow_null": True},
            "detailed_quantity_calculation": {"required": False, "allow_null": True},
            "material_cost_with_transport": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = (
            "id",
            "start_year",
            "end_year",
            "name",
            "status",
        )
        extra_kwargs = {
            "start_year": {"required": False, "allow_null": True},
            "end_year": {"required": False, "allow_null": True},
            "name": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class RateSerializer(serializers.ModelSerializer):
    fy = serializers.CharField(source="financial_year.fy", read_only=True)
    topic_name = serializers.CharField(source="topic._name", read_only=True)
    rate_category = RateCategorySerializer(read_only=True)

    class Meta:
        model = Rate
        fields = (
            "unit",
            "area",
            "source",
            "id",
            "district",
            "municipality",
            "financial_year",
            "fy",
            "topic_name",
            "topic",
            "title",
            "title_eng",
            "amount",
            "category",
            "rate_category",
            "status",
        )
        extra_kwargs = {
            "unit": {"required": False, "allow_null": True},
            "area": {"required": False, "allow_null": True},
            "source": {"required": False, "allow_null": True},
            "district": {"required": False, "allow_null": True},
            "municipality": {"required": False, "allow_null": True},
            "financial_year": {"required": False, "allow_null": True},
            "fy": {"required": False, "allow_null": True},
            "topic_name": {"required": False, "allow_null": True},
            "topic": {"required": False, "allow_null": True},
            "title": {"required": False, "allow_null": True},
            "title_eng": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "category": {"required": False, "allow_null": True},
            "rate_category": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
        read_only_fields = ("fy", "topic_name", "rate_category")


class DistrictRateSerializer(serializers.ModelSerializer):
    area = AreaSerializer(read_only=True)
    source = RateSourceSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)
    category = RateCategorySerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    item = TopicSerializer(source="topic.parent", read_only=True)
    current_rate = serializers.DecimalField(
        source="amount", max_digits=20, decimal_places=2, read_only=True
    )
    rate_one_year_ago = serializers.SerializerMethodField()
    rate_two_years_ago = serializers.SerializerMethodField()

    class Meta:
        model = Rate
        fields = (
            "id",
            "level",
            "category",
            "area",
            "source",
            "unit",
            "topic",
            "item",
            "current_rate",
            "rate_one_year_ago",
            "rate_two_years_ago",
            "status",
        )
        extra_kwargs = {
            "level": {"required": False, "allow_null": True},
            "category": {"required": False, "allow_null": True},
            "area": {"required": False, "allow_null": True},
            "source": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "topic": {"required": False, "allow_null": True},
            "item": {"required": False, "allow_null": True},
            "current_rate": {"required": False, "allow_null": True},
            "rate_one_year_ago": {"required": False, "allow_null": True},
            "rate_two_years_ago": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class DistrictRateViewSerializer(serializers.Serializer):
    financial_years = FinancialYearSerializer(many=True)
    rates = DistrictRateSerializer(many=True)


class DistrictRateCreateSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    title = serializers.CharField(allow_blank=True)
    title_eng = serializers.CharField(allow_blank=True, required=False)
    description = serializers.CharField(allow_blank=True, required=False)
    amount = serializers.CharField(allow_blank=True, required=False)
    topic = serializers.CharField()
    topic_unicode = serializers.CharField()
    sub_topic = serializers.CharField(allow_blank=True)
    sub_topic_unicode = serializers.CharField(allow_blank=True)
    item = serializers.CharField(allow_blank=True)
    item_unicode = serializers.CharField(allow_blank=True)
    rate_1 = serializers.CharField(allow_blank=True)
    rate_2 = serializers.CharField(allow_blank=True)
    rate_3 = serializers.CharField(allow_blank=True)
    unit = serializers.IntegerField()
    input = serializers.CharField()
    input_unicode = serializers.CharField()
    source = serializers.CharField()
    rate_area = serializers.CharField()


# avoid circular import
from norm.serializers import BasicNormSerializer


class QuantityImportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = (
            "quantity_type",
            "parent",
            "project",
            "type",
            "norm",
            "s_no",
            "description",
            "no",
            "length",
            "breadth",
            "height",
            "quantity",
            "unit",
        )
        extra_kwargs = {
            "quantity_type": {"required": False, "allow_blank": True},
        }


class QuantitySerializer(serializers.ModelSerializer):
    unit_value = UnitSerializer(source="unit", read_only=True)
    norm_value = BasicNormSerializer(source="norm", read_only=True)

    class Meta:
        model = Quantity
        fields = (
            "id",
            "partid",
            "quantity_type",
            "subpartid",
            "topicid",
            "subtopicid",
            "itemid",
            "is_leaf",
            "provisional",
            "project",
            "type",
            "line_number",
            "s_no",
            "description",
            "remarks",
            "no",
            "length",
            "breadth",
            "height",
            "quantity",
            "area",
            "unit",
            "unit_value",
            "norm_value",
            "norm_id",
            "parent",
            "status",
        )
        extra_kwargs = {
            "partid": {"required": False, "allow_null": True},
            "subpartid": {"required": False, "allow_null": True},
            "topicid": {"required": False, "allow_null": True},
            "subtopicid": {"required": False, "allow_null": True},
            "itemid": {"required": False, "allow_null": True},
            "is_leaf": {"required": False, "allow_null": True},
            "provisional": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "type": {"required": False, "allow_null": True},
            "line_number": {"required": False, "allow_null": True},
            "s_no": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "no": {"required": False, "allow_null": True},
            "length": {"required": False, "allow_null": True},
            "breadth": {"required": False, "allow_null": True},
            "height": {"required": False, "allow_null": True},
            "quantity": {"required": False, "allow_null": True},
            "area": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "unit_value": {"required": False, "allow_null": True},
            "norm_value": {"required": False, "allow_null": True},
            "norm_id": {"required": False, "allow_null": True},
            "parent": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class SummaryExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryExtra
        fields = (
            "id",
            "project",
            "s_no",
            "description",
            "amount",
            "remarks",
            "rate",
            "status",
        )
        extra_kwargs = {
            "project": {"required": False, "allow_null": True},
            "s_no": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "rate": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["type"] = "EXTRA"
        return data


class FederalAddressDistrictSerializer(serializers.ModelSerializer):
    municipalities = SimpleMunicipalitySerializer(
        source="municipality_set", many=True, read_only=True
    )

    class Meta:
        model = District
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "code",
            "municipalities",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "municipalities": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class FederalAddressProvinceSerializer(serializers.ModelSerializer):
    districts = FederalAddressDistrictSerializer(
        source="district_set", many=True, read_only=True
    )

    class Meta:
        model = Province
        fields = (
            "id",
            "name",
            "name_eng",
            "name_unicode",
            "code",
            "districts",
            "status",
        )
        extra_kwargs = {
            "name": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "name_unicode": {"required": False, "allow_null": True},
            "code": {"required": False, "allow_null": True},
            "districts": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }
