from decimal import Decimal

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from project.models import EstimationRate, FinancialYear, Rate
from project.serializers import RateSerializer, UnitSerializer

from .models import ActivityType, Norm, NormActivity, NormComponent, NormExtraCost


class ActivityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityType
        fields = ("id", "name_unicode", "name_eng", "status")


class NormActivitySerializer(serializers.ModelSerializer):
    activity_type_data = ActivityTypeSerializer(read_only=True, source="activity_type")

    class Meta:
        model = NormActivity
        fields = (
            "id",
            "name_unicode",
            "name_eng",
            "activity_type",
            "activity_type_data",
            "status",
        )
        extra_kwargs = {
            "name_unicode": {"required": False, "allow_null": True},
            "name_eng": {"required": False, "allow_null": True},
            "activity_type": {"required": False, "allow_null": True},
            "activity_type_data": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class NormExtraCostSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormExtraCost
        fields = ("id", "norm", "title", "rate", "on_amount", "on", "amount", "status")
        extra_kwargs = {
            "norm": {"required": False, "allow_null": True},
            "title": {"required": False, "allow_null": True},
            "rate": {"required": False, "allow_null": True},
            "on_amount": {"required": False, "allow_null": True},
            "on": {"required": False, "allow_null": True},
            "amount": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class NormComponentSerializer(serializers.ModelSerializer):
    """
    category -> Rate

    """

    id = serializers.IntegerField(required=False)
    category = RateSerializer(read_only=True)
    category_id = serializers.IntegerField(required=False)
    component_type = serializers.ChoiceField(
        choices=NormComponent.component_type_choices
    )
    rate = serializers.SerializerMethodField(read_only=True)
    unit_representation = UnitSerializer(source="unit", read_only=True)
    unit_id = serializers.IntegerField(required=False)

    class Meta:
        model = NormComponent
        fields = (
            "id",
            "norm",
            "category_id",
            "component_type",
            "category",
            "unit",
            "unit_id",
            "unit_representation",
            "quantity",
            "rate",
            "status",
        )
        extra_kwargs = {
            "norm": {"required": False, "allow_null": True},
            "component_type": {"required": False, "allow_null": True},
            "category": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "unit_representation": {"required": False, "allow_null": True},
            "quantity": {"required": False, "allow_null": True},
            "rate": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }

    def get_rate(self, instance):
        rate = instance.category
        rate_amount = 0
        if rate:
            all_rates = Rate.objects.prefetch_related(
                "unit",
                "financial_year",
                "topic",
                "topic__parent",
                "topic__parent__parent",
                "category",
            ).filter(topic=rate.topic, category=rate.category)
            current_fy = FinancialYear.current_fy()
            values = {}
            financial_years = FinancialYear.last_3_fys()
            fys = [fy.id for fy in financial_years]
            for rate in all_rates:
                val: dict = values.get(rate.topic_id, {})
                val.setdefault("rate_1", 0)
                val.setdefault("rate_2", 0)
                val.setdefault("rate_3", 0)
                val["rate"] = rate
                try:
                    i = fys.index(rate.financial_year.id) + 1
                    if rate.financial_year.name == current_fy.name:
                        val["id"] = rate.id
                    val[f"rate_{i}"] = rate.amount
                except:
                    pass
                values[rate.topic.id] = val
            rate_amount = val.get("rate_3", rate.amount)
        if rate_amount == 0 and rate and instance.norm and instance.norm.project:
            try:
                rate = EstimationRate.objects.get(
                    project=instance.norm.project, rate=rate
                )
                rate_amount = rate.total_rate
            except Exception as e:
                print(e)
                pass
        return rate_amount

    def get_amount(self, data):
        rate = data.get("rate", 0)
        quantity = data.get("quantity", 0)
        return Decimal(rate) * Decimal(quantity)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["amount"] = self.get_amount(data)
        return data


class ComponentListSerializer(serializers.Serializer):
    category_id = serializers.IntegerField(required=False)
    component_type = serializers.ChoiceField(
        choices=NormComponent.component_type_choices
    )
    unit_id = serializers.IntegerField(required=False)
    quantity = serializers.DecimalField(max_digits=20, decimal_places=5)


class BasicNormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Norm
        fields = (
            "id",
            "part_id",
            "sub_part_id",
            "item_id",
            "specification_no",
            "activity_no",
            "status",
        )
        extra_kwargs = {
            "part_id": {"required": False, "allow_null": True},
            "sub_part_id": {"required": False, "allow_null": True},
            "item_id": {"required": False, "allow_null": True},
            "specification_no": {"required": False, "allow_null": True},
            "activity_no": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class NormSerializer(WritableNestedModelSerializer):
    cost_component = NormExtraCostSerializer(
        many=True, source="normextracost_set", default=[]
    )

    equipment_component = NormComponentSerializer(many=True, required=False)
    material_component = NormComponentSerializer(many=True, required=False)
    labour_component = NormComponentSerializer(many=True, required=False)
    components_list = NormComponentSerializer(
        write_only=True, many=True, required=False
    )
    active = serializers.BooleanField(source="status", default=True)
    unit_representation = UnitSerializer(source="unit", read_only=True)

    @staticmethod
    def get_norm_component_by_type(norm, component_type):
        qs = norm.normcomponent_set.all().filter(component_type=component_type)
        serializer = NormComponentSerializer(instance=qs, many=True)
        return serializer.data

    def validate(self, data):
        print(data)
        material = data.pop("material_component", [])
        labour = data.pop("labour_component", [])
        equipment = data.pop("equipment_component", [])
        data["components_list"] = material + labour + equipment
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["material_component"] = self.get_norm_component_by_type(
            instance, "MATERIAL"
        )
        data["labour_component"] = self.get_norm_component_by_type(instance, "LABOUR")
        data["equipment_component"] = self.get_norm_component_by_type(
            instance, "EQUIPMENT"
        )
        amount = Decimal(0)
        for k in [
            "material_component",
            "labour_component",
            "equipment_component",
            "cost_component",
        ]:
            for d in data[k]:
                amount += Decimal(d["amount"])

        data["total_amount"] = amount
        data["unit_display"] = (
            f"{instance.unit_value} {instance.unit.name_eng if instance.unit else 'N/A'}"
        )
        return data

    def create(self, data):
        try:
            municipality = self.context.get("request").user.assigned_municipality
        except:
            municipality = None

        norms = Norm.objects.filter(
            municipality=municipality,
            activity_no=data["activity_no"],
            part_id=data["part_id"],
            sub_part_id=data["sub_part_id"],
            item_id=data["item_id"],
        )
        if norms.exists():
            raise serializers.ValidationError("This item_id already exists")

        components = data.pop("components_list")
        cost_components = data.pop("normextracost_set")
        norm = Norm.objects.create(**data)
        for component in components:
            component.pop("id", None)
            try:
                NormComponent.objects.create(norm_id=norm.id, **component)
            except Exception as e:
                print(e)
        for component in cost_components:
            component.pop("id", None)
            try:
                NormExtraCost.objects.create(norm_id=norm.id, **component)
            except Exception as e:
                print(e)
        return norm

    def update(self, instance, validated_data):
        instance.item_id = validated_data.get("item_id", instance.item_id)
        instance.part_id = validated_data.get("part_id", instance.part_id)
        instance.sub_part_id = validated_data.get("sub_part_id", instance.sub_part_id)
        instance.title = validated_data.get("title", instance.title)
        instance.title_eng = validated_data.get("title_eng", instance.title_eng)
        instance.description = validated_data.get("description", instance.description)
        instance.description_eng = validated_data.get(
            "description_eng", instance.description_eng
        )
        instance.remarks = validated_data.get("remarks", instance.remarks)
        instance.subpart_description = validated_data.get(
            "subpart_description", instance.subpart_description
        )
        instance.item_description = validated_data.get(
            "item_description", instance.item_description
        )
        instance.unit_value = validated_data.get("unit_value", instance.unit_value)
        instance.unit = validated_data.get("unit", instance.unit)
        instance.activity_no = validated_data.get("activity_no", instance.activity_no)
        instance.status = validated_data.get("status", instance.status)
        instance.specification_no = validated_data.get(
            "specification_no", instance.specification_no
        )

        components = validated_data.pop("components_list")
        cost_components = validated_data.pop("normextracost_set")

        for component in components:
            try:
                norm_component = NormComponent.objects.get(id=component.get("id"))
                norm_component.quantity = component.get("quantity")
                norm_component.save()
            except Exception as e:
                print(e)

        for component in cost_components:
            try:
                norm_component = NormExtraCost.objects.get(id=component.get("id"))
                norm_component.title = component.get("title")
                norm_component.rate = component.get("rate")
                norm_component.on_amount = component.get("on_amount")
                norm_component.on = component.get("on")
                norm_component.amount = component.get("amount")
                norm_component.save()
            except Exception as e:
                print(e)

        instance.save()

        return instance

    class Meta:
        model = Norm
        fields = (
            "id",
            "part_id",
            "sub_part_id",
            "item_id",
            "activity_no",
            "part_activity_no",
            "subpart_activity_no",
            "specification_no",
            "part_specification_no",
            "subpart_specification_no",
            "title",
            "title_eng",
            "description",
            "description_eng",
            "subpart_description",
            "subpart_description_eng",
            "item_description",
            "item_description_eng",
            "remarks",
            "title",
            "unit",
            "unit_representation",
            "unit_value",
            "cost_component",
            "components_list",
            "material_component",
            "labour_component",
            "equipment_component",
            "active",
            "activity",
            "project",
            "status",
        )
        extra_kwargs = {
            "part_id": {"required": False, "allow_null": True},
            "sub_part_id": {"required": False, "allow_null": True},
            "item_id": {"required": False, "allow_null": True},
            "activity_no": {"required": False, "allow_null": True},
            "part_activity_no": {"required": False, "allow_null": True},
            "subpart_activity_no": {"required": False, "allow_null": True},
            "specification_no": {"required": False, "allow_null": True},
            "part_specification_no": {"required": False, "allow_null": True},
            "subpart_specification_no": {"required": False, "allow_null": True},
            "title": {"required": False, "allow_null": True},
            "title_eng": {"required": False, "allow_null": True},
            "description": {"required": False, "allow_null": True},
            "description_eng": {"required": False, "allow_null": True},
            "subpart_description": {"required": False, "allow_null": True},
            "subpart_description_eng": {"required": False, "allow_null": True},
            "item_description": {"required": False, "allow_null": True},
            "item_description_eng": {"required": False, "allow_null": True},
            "remarks": {"required": False, "allow_null": True},
            "unit": {"required": False, "allow_null": True},
            "unit_representation": {"required": False, "allow_null": True},
            "unit_value": {"required": False, "allow_null": True},
            "cost_component": {"required": False, "allow_null": True},
            "components_list": {"required": False, "allow_null": True},
            "material_component": {"required": False, "allow_null": True},
            "labour_component": {"required": False, "allow_null": True},
            "equipment_component": {"required": False, "allow_null": True},
            "active": {"required": False, "allow_null": True},
            "activity": {"required": False, "allow_null": True},
            "project": {"required": False, "allow_null": True},
            "status": {"required": False, "allow_null": True},
        }


class NormExportSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    unit_name_eng = serializers.CharField(source="unit.name_eng", read_only=True)

    class Meta:
        model = Norm
        fields = (
            "activity_no",
            "specification_no",
            "description",
            "description_eng",
            "unit_name",
            "unit_name_eng",
            "analysed_rate",
            "remarks",
        )
