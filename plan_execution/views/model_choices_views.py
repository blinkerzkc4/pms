from django.db.models import TextChoices
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from plan_execution.choices import BailType, BankGuaranteeType, WorkProposerType


class ModelChoicesView(APIView):
    choice_class: TextChoices = None

    def get(self, request, *args, **kwargs):
        choices_response = {
            "results": [
                {
                    "code": choice_value,
                    "name": choice_label,
                }
                for choice_value, choice_label in self.choice_class.choices
            ]
        }
        return Response(choices_response, status=status.HTTP_200_OK)


class WorkProposerTypeChoicesView(ModelChoicesView):
    choice_class = WorkProposerType


class BankGuaranteeTypeChoicesView(ModelChoicesView):
    choice_class = BankGuaranteeType


class BailTypeChoicesView(ModelChoicesView):
    choice_class = BailType
