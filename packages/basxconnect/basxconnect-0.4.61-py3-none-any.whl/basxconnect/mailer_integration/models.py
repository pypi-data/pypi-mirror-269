from basxbread.contrib.languages.fields import LanguageField
from django.db import models
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Email


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    external_id = models.CharField(max_length=50)

    def __str__(self):
        return self.name


def languages_choices(field, request, instance):
    from basxconnect.core import settings

    return settings.PREFERRED_LANGUAGES


class SynchronizationResult(models.Model):
    total_synchronized_persons = models.IntegerField(
        null=True, verbose_name=_("Number of persons in the mailer segment")
    )
    sync_completed_datetime = models.DateTimeField(
        null=True, verbose_name=_("Date and time")
    )


class Subscription(models.Model):
    email = models.OneToOneField(Email, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=[
            ("subscribed", "subscribed"),
            ("unsubscribed", "unsubscribed"),
            ("non-subscribed", "non-subscribed"),
            ("cleaned", "cleaned"),
            ("archived", "archived"),
        ],
    )
    status_before_archiving = models.CharField(
        max_length=50,
        choices=[
            ("subscribed", "subscribed"),
            ("unsubscribed", "unsubscribed"),
            ("non-subscribed", "non-subscribed"),
            ("cleaned", "cleaned"),
        ],
        null=True,
    )

    interests = models.ManyToManyField(Interest, blank=True)
    interests.verbose_name = _("Mailing Interests")

    language = LanguageField(_("Language"), blank=True)
    language.lazy_choices = languages_choices

    latest_sync = models.ForeignKey(
        SynchronizationResult,
        related_name="synchronized_subscription",
        on_delete=models.SET_NULL,
        null=True,
    )


class SynchronizationPerson(models.Model):
    sync_result = models.ForeignKey(
        SynchronizationResult, on_delete=models.CASCADE, related_name="persons"
    )
    email = models.CharField(max_length=100)
    first_name = models.CharField(_("First Name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=255, blank=True)
    old_subscription_status = models.CharField(
        _("Old subscription status"), max_length=255, blank=True
    )
    new_subscription_status = models.CharField(
        _("New subscription status"), max_length=255, blank=True
    )

    NEW = "new"
    SKIPPED = "import_error"
    PREVIOUSLY_SYNCED = "synced_previously"
    SUBSCRIPTION_STATUS_CHANGED = "subscription_status_changed"
    SYNC_STATUS_CHOICES = [
        (NEW, _("Newly added to BasxConnect")),
        (SKIPPED, _("Not added to BasxConnect")),
        (PREVIOUSLY_SYNCED, _("Synchronized previously but not this time")),
        (SUBSCRIPTION_STATUS_CHANGED, _("Subscription status changed")),
    ]
    sync_status = models.CharField(
        _("Synchronization Status"),
        choices=SYNC_STATUS_CHOICES,
        max_length=255,
        blank=True,
    )
    maybe_duplicate = models.BooleanField(
        _("Possible duplicate"),
        default=False,
        help_text=_("Other person with same first and last name already exists"),
    )

    def __str__(self):
        return self.email
