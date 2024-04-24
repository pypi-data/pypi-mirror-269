from django.utils.translation import gettext_lazy as _
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import (
    BooleanPreference,
    LongStringPreference,
    StringPreference,
)

mailchimp_integration = Section("mailchimp", _("Mailchimp"))


@global_preferences_registry.register
class MailchimpServer(StringPreference):
    section = mailchimp_integration
    name = "server"
    default = ""
    verbose_name = _("Mailchimp server")


@global_preferences_registry.register
class MailchimpListId(StringPreference):
    section = mailchimp_integration
    name = "list_id"
    default = ""
    verbose_name = _("Mailchimp list ID")


@global_preferences_registry.register
class MailchimpSegmentId(StringPreference):
    section = mailchimp_integration
    name = "segment_id"
    default = ""
    verbose_name = _("Mailchimp segment ID")


@global_preferences_registry.register
class MailchimpInterestsCategoryId(StringPreference):
    section = mailchimp_integration
    name = "interests_category_id"
    default = ""
    verbose_name = _("Mailchimp interests category ID")


@global_preferences_registry.register
class MailchimpTag(StringPreference):
    section = mailchimp_integration
    name = "tag"
    default = "Synchronized with Basxconnect"
    verbose_name = _("Mailchimp tag")


@global_preferences_registry.register
class MailchimpBasxconnectTag(StringPreference):
    section = mailchimp_integration
    name = "basxconnect_tag"
    default = "Imported from Mailchimp"
    verbose_name = _("BasxConnect Mailchimp tag")


@global_preferences_registry.register
class MailchimpApiKey(LongStringPreference):
    section = mailchimp_integration
    name = "api_key"
    default = ""
    verbose_name = _("Mailchimp API key")


@global_preferences_registry.register
class MailchimpDisableInterestsKey(BooleanPreference):
    section = mailchimp_integration
    name = "disable_interests"
    default = False
    verbose_name = _("Disable mailing interests")


@global_preferences_registry.register
class MailchimpSynchronizeLanguage(BooleanPreference):
    section = mailchimp_integration
    name = "synchronize_language"
    default = False
    verbose_name = _("Synchronize language with Mailchimp")


@global_preferences_registry.register
class MailchimpAutomaticallySubscribeNewPersons(BooleanPreference):
    section = mailchimp_integration
    name = "automatically_subscribe_new_persons"
    default = False
    verbose_name = _("Automatically subscribe new persons")
