from django.http import HttpRequest

from norm.models import Norm
from norm.serializers import NormSerializer
from project.models import FinancialYear, Rate
from user.choices import UserTypeChoices


def get_norms_data(request: HttpRequest):
    if request.user.user_type == UserTypeChoices.SUPER_ADMIN:
        norms_queryset = Norm.objects.all()
    else:
        norms_queryset = Norm.objects.filter(
            municipality=request.user.assigned_municipality
        )
    norms_serializer = NormSerializer(norms_queryset, many=True)
    return norms_serializer.data


def get_district_rate_data(request: HttpRequest):
    financial_years = FinancialYear.last_3_fys()
    current_fy = FinancialYear.current_fy()

    def single_input(**data):
        input_type = data.get("input_type")
        disable = input_type != "ITEM"
        level = data.get("level")
        input_type = "TOPIC" if level == 1 else input_type

        return {
            "oid": data.get("oid"),
            "id": data.get("id"),
            "parent_id": data.get("parent", 0),
            "s_no": data.get("s_no", 0),
            "sort_id": data.get("sort_id"),
            "input_type": input_type,
            # "content_eng": "topic1",
            # "content_unicode": "",
            "rate_1": data.get("rate_1", 0),
            "rate_2": data.get("rate_2", 0),
            "rate_3": data.get("rate_3", 0),
            "unit": data.get("unit", ""),
            "unit_id": data.get("unit_id"),
            "area": data.get("area", ""),
            "area_id": data.get("area_id"),
            "source": data.get("source", ""),
            "source_id": data.get("source_id"),
            "topic": data.get("topic", ""),
            "topic_unicode": data.get("topic_unicode", ""),
            "sub_topic": data.get("subtopic", ""),
            "sub_topic_unicode": data.get("subtopic_unicode", ""),
            "item": data.get("item", ""),
            "item_unicode": data.get("item_unicode", ""),
            "isDisable": disable,
        }

    def add_data(data, level, j, parent=0, sort_id=0):
        output = []
        if isinstance(data, list):
            for d in data:
                output.append(
                    single_input(
                        input_type="ITEM",
                        oid=j,
                        parent=parent,
                        sort_id=sort_id,
                        **d,
                    )
                )
                j += 1
        else:
            for k in data:
                eng, nep = k.split("-" * 5)
                input_type = "TOPIC" if level == 1 else "SUBTOPIC"
                dta = (
                    {"topic": eng, "topic_unicode": nep}
                    if level == 1
                    else {
                        "subtopic": eng,
                        "subtopicunicode": nep,
                    }
                )
                output.append(
                    single_input(
                        input_type=input_type,
                        oid=j,
                        parent=parent,
                        sort_id=sort_id,
                        **dta,
                    )
                )
                j += 1
                j, out = add_data(data[k], level + 1, j, parent=j - 1, sort_id=sort_id)
                output.extend(out)
                j += 1
        return j, output

    def create_frontend_format(data, level):
        output = []
        j = 1
        i = 0
        for i, l in enumerate(level):
            try:
                j, out = add_data({l: level[l]}, 1, j, sort_id=i)
                output.extend(out)
            except Exception as e:
                print(e)
        try:
            j, out = add_data(data, 1, j, sort_id=i + 1)
        except Exception as e:
            print(e)
        output.extend(out)
        return output

    if request.user.user_type == UserTypeChoices.SUPER_ADMIN:
        rates = Rate.objects.all().prefetch_related(
            "unit",
            "financial_year",
            "topic",
            "topic__parent",
            "topic__parent__parent",
            "category",
        )
    else:
        rates = Rate.objects.filter(
            municipality=request.user.assigned_municipality
        ).prefetch_related(
            "unit",
            "financial_year",
            "topic",
            "topic__parent",
            "topic__parent__parent",
            "category",
        )

    fys = [str(fy) for fy in financial_years]

    if not rates:
        return []

    values = {}
    for rate in rates:
        val = values.get(rate.topic_id, {})
        val["rate"] = rate
        i = fys.index(rate.financial_year.name) + 1
        if rate.financial_year.name == current_fy.name:
            val["id"] = rate.id
        val[f"rate_{i}"] = {"fy": str(rate.financial_year), "amount": rate.amount}
        values[rate.topic.id] = val

    output = []
    level = {}

    for val in values.values():
        # TODO: maybe can get this from serializer to optimize it
        if not val.get("id"):
            continue
        rate = val.pop("rate")
        val["level"] = rate.level
        val["category"] = rate.category.name_eng if rate.category else ""
        val["category_unicode"] = rate.category.name_unicode if rate.category else ""
        val["area_id"] = rate.area_id
        val["area"] = rate.area.name_eng if rate.area else ""
        val["source_id"] = rate.source_id
        val["source"] = rate.source.name_eng if rate.source else ""
        val["unit_id"] = rate.unit_id
        val["unit"] = rate.unit.name_eng if rate.unit else ""
        val["unit_unicode"] = rate.unit.name_unicode if rate.unit else ""
        rate_topic = rate.topic
        topic, subtopic, item, *_ = rate_topic._name_unicode.split("-" * 5) + [
            "",
            "",
            "",
        ]
        val["topic_unicode"] = topic
        val["subtopic_unicode"] = subtopic
        val["item_unicode"] = item

        t, st, itm, *_ = rate_topic._name_eng.split("-" * 5) + ["", "", ""]
        val["topic"] = t
        val["subtopic"] = st
        val["item"] = itm
        tps = f"{topic}-----{t}"
        stps = f"{subtopic}-----{st}"
        try:
            if rate.level == 1:
                output.append(val)
            elif rate.level == 2:
                val["subtopic"] = ""
                val["subtopic_unicode"] = ""
                val["item"] = subtopic
                val["item_unicode"] = st
                tpic = level.get(tps, [])
                tpic.append(val)
                level[tps] = tpic
            elif rate.level == 3:
                level[tps] = level.get(tps, {})
                st = level[tps].get(stps, [])
                st.append(val)
                level[tps][stps] = st
        except Exception as e:
            print(e)
    return create_frontend_format(output, level)
