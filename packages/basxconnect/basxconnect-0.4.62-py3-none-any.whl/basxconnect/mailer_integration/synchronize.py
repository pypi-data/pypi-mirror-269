import django_countries
from django.db.models.functions import Lower
from django.utils import timezone
from dynamic_preferences.registries import global_preferences_registry
from mailchimp_marketing.api_client import ApiClientError

from basxconnect.core import models
from basxconnect.mailer_integration.abstract.mailer import AbstractMailer, MailerPerson
from basxconnect.mailer_integration.models import (
    Interest,
    Subscription,
    SynchronizationPerson,
    SynchronizationResult,
)


def synchronize(mailer: AbstractMailer) -> SynchronizationResult:
    synchronize_interests(mailer)

    person_count = mailer.get_person_count()
    sync_result = SynchronizationResult.objects.create()
    sync_result.total_synchronized_persons = person_count
    batch_size = 1000
    for batch_number in range(((person_count - 1) // batch_size) + 1):
        synchronize_batch(batch_size, batch_number * batch_size, mailer, sync_result)
    sync_result.sync_completed_datetime = timezone.now()
    sync_result.save()

    # delete all subscriptions which were not synchronized
    # and were not deactivated already using the UI
    # (those we want to be able to reactivate, so we have to keep them)
    Subscription.objects.exclude(latest_sync=sync_result).exclude(
        status="archived"
    ).delete()

    return sync_result


def synchronize_batch(count, offset, mailer, sync_result):
    mailer_persons = mailer.get_persons(count, offset)
    datasource_tag = _get_or_create_tag(mailer.tag())
    for mailer_person in mailer_persons:
        try:
            matching_email_addresses = list(
                models.Email.objects.filter(
                    email=mailer_person.email,
                ).all()
            )
            if len(matching_email_addresses) == 0:
                if not is_valid_new_person(mailer_person):
                    _save_sync_person(
                        mailer_person, sync_result, SynchronizationPerson.SKIPPED
                    )
                else:
                    created_person = _save_person(datasource_tag, mailer_person)
                    # simplified duplication detection, only yield warning
                    _save_subscription(
                        created_person.primary_email_address,
                        mailer_person,
                        sync_result,
                        new_person=True,
                    )
                    _save_sync_person(
                        mailer_person, sync_result, SynchronizationPerson.NEW
                    )
            else:
                # if the downloaded email address already exists in our system,
                # update the mailing preference for this email address, without
                # creating a new person in the database
                for email in matching_email_addresses:
                    _save_subscription(
                        email, mailer_person, sync_result, new_person=False
                    )
        except ApiClientError:
            # todo: "skipped" is not really the right term, since the person might already
            #  have been added to BasxConnect before the exception happens
            _save_sync_person(mailer_person, sync_result, SynchronizationPerson.SKIPPED)


def synchronize_interests(datasource):
    old_interests = Interest.objects.all()
    downloaded_interests = datasource.get_interests()
    new_interests_ids = []
    for interest in downloaded_interests:
        interest_from_db, _ = Interest.objects.get_or_create(
            external_id=interest.id, name=interest.name
        )
        new_interests_ids.append(interest_from_db.id)
    for interest in old_interests:
        if interest.id not in new_interests_ids:
            interest.delete()


def _get_or_create_tag(tag: str) -> models.Term:
    tags_vocabulary = models.Vocabulary.objects.get(slug="tag")
    tag, _ = models.Term.objects.get_or_create(term=tag, vocabulary=tags_vocabulary)
    return tag


def is_valid_new_person(person: MailerPerson):
    return django_countries.Countries().countries.get(
        person.country
    ) and person.status in ["subscribed"]


def _save_sync_person(
    mailer_person, sync_result, syn_status, old_subscription_status=""
):
    # slighly complicated ignore-case comparison due to Sqlite's
    # behaviour with ignore-case-comparison of non-ascii strings
    # See https://docs.djangoproject.com/en/dev/ref/databases/#sqlite-string-matching
    maybe_duplicate = (
        syn_status == SynchronizationPerson.NEW
        and models.NaturalPerson.objects.annotate(
            first_name_lower=Lower("first_name"), last_name_lower=Lower("last_name")
        )
        .filter(
            first_name_lower=mailer_person.first_name.lower(),
            last_name_lower=mailer_person.last_name.lower(),
        )
        .count()
        > 1
    )
    SynchronizationPerson.objects.create(
        sync_result=sync_result,
        email=mailer_person.email,
        first_name=mailer_person.first_name,
        last_name=mailer_person.last_name,
        sync_status=syn_status,
        maybe_duplicate=maybe_duplicate,
        new_subscription_status=mailer_person.status,
        old_subscription_status=old_subscription_status,
    )


def _save_person(datasource_tag: models.Term, mailer_person: MailerPerson):
    person = models.NaturalPerson.objects.create(
        first_name=mailer_person.first_name,
        name=mailer_person.display_name,
        last_name=mailer_person.last_name,
    )
    if mailer_person.persontype:
        persontype = models.Term.objects.filter(slug=mailer_person.persontype).first()
        if persontype:
            person.type = persontype
    person.tags.add(datasource_tag)
    person.save()
    email = models.Email.objects.create(email=mailer_person.email, person=person)
    person.primary_email_address = email
    person.save()
    _save_postal_address(person, mailer_person)
    return person


def _save_postal_address(person: models.Person, mailer_person: MailerPerson):
    address = models.Postal(
        person=person,
        country=mailer_person.country,
        address=mailer_person.address,
        postcode=mailer_person.postcode,
        city=mailer_person.city,
    )
    address.save()
    person.primary_postal_address = address
    person.save()


def _save_subscription(
    email: models.Email,
    mailer_person: MailerPerson,
    sync_result: SynchronizationResult,
    new_person: bool,
):
    subscription, _ = Subscription.objects.get_or_create(email=email)
    old_subscription_status = subscription.status or ""
    subscription.status = mailer_person.status
    subscription.language = mailer_person.language
    subscription.interests.clear()
    for interest_id in mailer_person.interests_ids:
        interest = Interest.objects.get(external_id=interest_id)
        subscription.interests.add(interest)
    subscription.latest_sync = sync_result
    subscription.save()
    if old_subscription_status != subscription.status:
        _save_sync_person(
            mailer_person,
            sync_result,
            SynchronizationPerson.SUBSCRIPTION_STATUS_CHANGED,
            old_subscription_status=old_subscription_status,
        )
    if (
        new_person
        and global_preferences_registry.manager()["mailchimp__synchronize_language"]
    ):
        person = email.person
        person.preferred_language = mailer_person.language
        person.save()
