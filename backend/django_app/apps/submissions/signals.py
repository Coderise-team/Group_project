from apps.contests.services import calculate_score
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Submission


@receiver(pre_save, sender=Submission)
def _capture_previous_verdict(sender, instance: Submission, **kwargs):
    if not instance.pk:
        instance._previous_verdict = None
        return
    instance._previous_verdict = (
        Submission.objects.filter(pk=instance.pk)
        .values_list("verdict", flat=True)
        .first()
    )


@receiver(post_save, sender=Submission)
def _recalculate_contest_score_on_ac(
    sender, instance: Submission, created: bool, **kwargs
):
    if not instance.contest:
        return
    if instance.verdict != Submission.Verdict.AC:
        return

    if created:
        calculate_score(instance.user, instance.contest)
        return

    previous_verdict = getattr(instance, "_previous_verdict", None)
    if previous_verdict != Submission.Verdict.AC:
        calculate_score(instance.user, instance.contest)
