from itertools import zip_longest

from django.db import models

from project.models import (
    BaseModel,
    EstimationRate,
    FinancialYear,
    Municipality,
    Project,
    Rate,
    Unit,
)


class ActivityType(BaseModel):
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    name_unicode = models.CharField(blank=True, max_length=255)
    name_eng = models.CharField(blank=True, max_length=255)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name_eng or self.name_unicode


class NormActivity(BaseModel):
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    activity_type = models.ForeignKey(
        ActivityType, null=True, blank=True, on_delete=models.PROTECT
    )
    name_unicode = models.CharField(blank=True, max_length=255)
    name_eng = models.CharField(blank=True, max_length=255)
    status = models.BooleanField(default=True, null=True, blank=True)

    def __str__(self):
        return self.name_eng or self.name_unicode


class Norm(BaseModel):
    created_from = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.PROTECT
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    project = models.ForeignKey(
        Project, on_delete=models.PROTECT, null=True, blank=True
    )
    specification = models.CharField(max_length=255, blank=True)
    activity = models.ForeignKey(
        NormActivity, null=True, blank=True, on_delete=models.PROTECT
    )

    # Item Numbers
    item_id = models.CharField(max_length=255)
    part_id = models.CharField(max_length=255, blank=True)
    sub_part_id = models.CharField(max_length=255, blank=True)

    # Activity Numbers
    activity_no = models.CharField(max_length=255, blank=True)
    part_activity_no = models.CharField(max_length=255, blank=True)
    subpart_activity_no = models.CharField(max_length=255, blank=True)

    # Specification Numbers
    specification_no = models.CharField(max_length=255, blank=True)
    part_specification_no = models.CharField(max_length=255, blank=True)
    subpart_specification_no = models.CharField(max_length=255, blank=True)

    # Title
    title = models.TextField(blank=True)
    title_eng = models.TextField(blank=True)

    # Description
    description = models.TextField(blank=True, default="")
    subpart_description = models.TextField(blank=True, default="")
    item_description = models.TextField(blank=True, default="")

    # Description (Eng)
    description_eng = models.TextField(blank=True, default="")
    subpart_description_eng = models.TextField(blank=True, default="")
    item_description_eng = models.TextField(blank=True, default="")

    remarks = models.TextField(blank=True, null=True, default="")

    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True, blank=True)
    unit_value = models.DecimalField(
        max_digits=20, decimal_places=5, default="0.0", blank=True
    )
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def item_map_id(self):
        return f"{self.activity_no}-{self.specification_no}-{self.item_id}"

    @property
    def part_map_id(self):
        return f"{self.activity_no}-{self.specification_no}-{self.part_id}"

    @property
    def component_by_type(self):
        components = self.normcomponent_set.all()
        labour = components.filter(component_type="LABOUR")
        material = components.filter(component_type="MATERIAL")
        equipment = components.filter(component_type="EQUIPMENT")
        return zip_longest(labour, material, equipment)

    def get_component_total_by_type(self, component_type):
        components = self.normcomponent_set.all()
        component = components.filter(component_type=component_type)
        total = sum([c.amount for c in component])
        return total or 0

    @property
    def labour_total(self):
        return self.get_component_total_by_type("LABOUR")

    @property
    def material_total(self):
        return self.get_component_total_by_type("MATERIAL")

    @property
    def equipment_total(self):
        return self.get_component_total_by_type("EQUIPMENT")

    @property
    def total(self):
        return sum([self.labour_total, self.material_total, self.equipment_total])

    @property
    def analysed_rate(self):
        try:
            return self.total / self.unit_value
        except:
            return 1

    class Meta:
        indexes = (
            models.Index(fields=("activity_no",)),
            models.Index(fields=("specification_no",)),
        )


class NormExtraCost(BaseModel):
    on_choices = (
        ("LABOUR", "Labour"),
        ("MATERIAL", "Material"),
        ("EQUIPMENT", "Equipment"),
        ("TOTAL", "total"),
    )
    on = models.CharField(
        max_length=20, choices=on_choices, blank=True, default="TOTAL"
    )
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    norm = models.ForeignKey(Norm, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=255)
    on_amount = models.DecimalField(max_digits=20, decimal_places=5, default="0.0")
    rate = models.DecimalField(max_digits=20, decimal_places=5)
    amount = models.DecimalField(max_digits=20, decimal_places=5, default="0.0")
    status = models.BooleanField(default=True, null=True, blank=True)


class NormComponent(BaseModel):
    component_type_choices = (
        ("LABOUR", "Labour"),
        ("MATERIAL", "Material"),
        ("EQUIPMENT", "Equipment"),
    )
    norm = models.ForeignKey(Norm, on_delete=models.CASCADE, null=True, blank=True)
    municipality = models.ForeignKey(
        Municipality, on_delete=models.PROTECT, null=True, blank=True
    )
    component_type = models.CharField(max_length=20, choices=component_type_choices)
    category = models.ForeignKey(Rate, on_delete=models.PROTECT, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.DecimalField(max_digits=20, decimal_places=5)
    status = models.BooleanField(default=True, null=True, blank=True)

    @property
    def amount(self):
        return self.quantity * self.rate

    @property
    def rate(self):
        rate = self.category
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
            fys = [str(fy) for fy in financial_years]
            for rate in all_rates:
                val = values.get(rate.topic_id, {})
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
        if rate_amount == 0 and rate and self.norm and self.norm.project:
            rate = EstimationRate.objects.filter(
                project=self.norm.project, rate=rate
            ).first()
            if rate:
                rate_amount = rate.total_rate
        return rate_amount
