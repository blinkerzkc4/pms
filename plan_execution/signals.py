from django.db.models.signals import post_save
from django.dispatch import receiver

from notification.models import Notification
from plan_execution.models import (
    OfficialProcess,
    OpeningContractAccount,
    QuotationSpecification,
)
from plan_execution.serializers import (
    OfficialProcessRequestSerializer,
    ProjectCommentSerializer,
)


@receiver(post_save, sender="plan_execution.ProjectComment")
def send_notificaiton(sender, instance, created, **kwargs):
    if created:
        notification_title = f"Comment Received for {instance.get_send_for_display()}"
        notification_description = f"Hi, {instance.send_to.full_name or instance.send_to.username}. You have received a comment of {instance.project.name} for {instance.get_send_for_display()}. Please review and update its status accordingly."
        notification_creation_data = {
            "title": notification_title,
            "description": notification_description,
            "user": instance.send_to,
            "notified_for": "comment",
            "notified_object": ProjectCommentSerializer(instance).data,
        }
        try:
            notification_creation_data["project"] = instance.project.execution
        except:
            pass
        Notification.objects.create(**notification_creation_data)


@receiver(post_save, sender="plan_execution.ConsumerFormulation")
def opening_contract_account_update(sender, instance, created, **kwargs):
    if created:
        consumer_committee = (
            instance.selected_consumer_committee or instance.consumer_committee
        )
        if consumer_committee:
            oca = OpeningContractAccount.objects.filter(project=instance.project)
            if oca:
                oca.update(
                    bank_name=consumer_committee.bank,
                    bank_branch=consumer_committee.bank_branch,
                    account_no=consumer_committee.bank_acc_no,
                )
            else:
                oca = OpeningContractAccount.objects.create(
                    project=instance.project,
                    bank_name=consumer_committee.bank,
                    bank_branch=consumer_committee.bank_branch,
                    account_no=consumer_committee.bank_acc_no,
                )


@receiver(post_save, sender=QuotationSpecification)
def quotation_create_invitation(sender, instance, created, **kwargs):
    if instance:
        qsa = instance.create_submission_approval()
        print(qsa)
        print(instance.specification_firm_details.all())
        for firm in instance.specification_firm_details.all():
            firm.create_invitation()
            firm.create_firm_quoted_cost_estimate()
            firm.submission_approval = qsa
            print(firm)
            print(firm.submission_approval)
            firm.save()


@receiver(post_save, sender=OfficialProcess)
def official_process_notification(sender, instance, created, **kwargs):
    if created:
        notification_title = f"Official Process Created for {instance.project.name}"
        notification_description = f"Hi, {instance.send_to.full_name or instance.send_to.username}. Official Process has been created for {instance.project.project.name}. Please review and update its status accordingly."
        notification_creation_data = {
            "title": notification_title,
            "description": notification_description,
            "user": instance.send_to,
            "notified_for": "official_process",
            "notified_object": OfficialProcessRequestSerializer(instance).data,
        }
        Notification.objects.create(**notification_creation_data)
