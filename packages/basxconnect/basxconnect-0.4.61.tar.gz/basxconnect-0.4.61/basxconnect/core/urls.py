from basxbread import views as breadviews
from basxbread.utils.urls import (
    autopath,
    default_model_paths,
    model_urlname,
    reverse_model,
)
from basxbread.views import AddView, EditView
from django.views.generic import RedirectView

import basxconnect.core.views.tag_views
from basxconnect.core.views import settings_views
from basxconnect.core.views.person import (
    person_browse_views,
    person_details_views,
    person_modals_views,
    search_person_view,
)

from . import models
from .views.relationship_views import AddRelationshipView, EditRelationshipView
from .views.term import TermsBrowseView
from .views.vocabulary import VocabularyBrowseView
from .wizards.add_person import AddPersonWizard

urlpatterns = [
    autopath(
        RedirectView.as_view(
            url=reverse_model(models.Person, "addwizard", kwargs={"step": "Search"})
        ),
        model_urlname(models.Person, "add"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.NaturalPerson, "browse"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.LegalPerson, "browse"),
    ),
    autopath(
        RedirectView.as_view(url=reverse_model(models.Person, "browse")),
        model_urlname(models.PersonAssociation, "browse"),
    ),
    autopath(
        AddPersonWizard.as_view(url_name=model_urlname(models.Person, "addwizard")),
        model_urlname(models.Person, "addwizard"),
    ),
    *default_model_paths(
        models.Person,
        browseview=person_browse_views.PersonBrowseView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
    ),
    *default_model_paths(
        models.NaturalPerson,
        editview=person_details_views.NaturalPersonEditView,
        readview=person_details_views.NaturalPersonReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.NaturalPerson,
            attrs={
                "personnumber": models.random_personid,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(
        models.LegalPerson,
        editview=person_details_views.LegalPersonEditView,
        readview=person_details_views.LegalPersonReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.LegalPerson,
            attrs={
                "personnumber": None,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(
        models.PersonAssociation,
        editview=person_details_views.PersonAssociationEditView,
        readview=person_details_views.PersonAssociationReadView,
        deleteview=breadviews.DeleteView._with(softdeletefield="deleted"),
        copyview=breadviews.generate_copyview(
            models.PersonAssociation,
            attrs={
                "personnumber": None,
                "primary_postal_address": None,
                "primary_email_address": None,
            },
            labelfield="name",
            copy_related_fields=(
                "core_web_list",
                "core_email_list",
                "core_phone_list",
                "core_fax_list",
                "core_postal_list",
            ),
        ),
    ),
    *default_model_paths(
        models.Relationship,
        editview=EditRelationshipView,
        addview=AddRelationshipView,
    ),
    *default_model_paths(models.RelationshipType),
    *default_model_paths(
        models.Term,
        addview=AddView._with(fields=["term", "vocabulary"]),
        editview=EditView._with(fields=["term", "slug", "disabled"]),
        browseview=TermsBrowseView,
    ),
    *default_model_paths(
        models.Vocabulary,
        browseview=VocabularyBrowseView,
    ),
    *default_model_paths(models.Postal),
    *default_model_paths(models.Phone),
    *default_model_paths(models.Web),
    autopath(
        person_details_views.togglepersonstatus,
        model_urlname(models.Person, "togglestatus"),
    ),
    autopath(settings_views.relationshipssettings),
    autopath(search_person_view.searchperson),
    autopath(
        person_modals_views.NaturalPersonEditMailingsView.as_view(),
        urlname=model_urlname(models.NaturalPerson, "ajax_edit_mailings"),
    ),
    autopath(
        person_modals_views.LegalPersonEditMailingsView.as_view(),
        urlname=model_urlname(models.LegalPerson, "ajax_edit_mailings"),
    ),
    autopath(
        person_modals_views.NaturalPersonEditPersonalDataView.as_view(),
        urlname=model_urlname(models.NaturalPerson, "ajax_edit_personal_data"),
    ),
    autopath(
        person_modals_views.LegalPersonEditPersonalDataView.as_view(),
        urlname=model_urlname(models.LegalPerson, "ajax_edit_personal_data"),
    ),
    autopath(
        person_modals_views.PersonAssociationEditPersonalDataView.as_view(),
        urlname=model_urlname(models.PersonAssociation, "ajax_edit"),
    ),
    autopath(
        person_modals_views.EditPostalAddressView.as_view(),
        urlname=model_urlname(models.Postal, "ajax_edit"),
    ),
    autopath(
        person_modals_views.AddPostalAddressView.as_view(),
        urlname=model_urlname(models.Postal, "ajax_add"),
    ),
    autopath(
        EditView._with(fields=["remarks"]).as_view(model=models.Person),
        urlname=model_urlname(models.Person, "ajax_edit_remarks"),
    ),
    autopath(
        EditView._with(fields=["tags"]).as_view(model=models.Person),
        urlname=model_urlname(models.Person, "ajax_edit_tags"),
    ),
    *[
        autopath(
            EditView._with(model=m, fields=["personnumber", "type"]).as_view(),
            urlname=model_urlname(m, f"{m._meta.model_name}_ajax_edit_metadata"),
        )
        for m in [models.NaturalPerson, models.LegalPerson, models.PersonAssociation]
    ],
    autopath(
        person_details_views.confirm_delete_email,
        urlname=model_urlname(models.Email, "delete"),
    ),
    autopath(
        person_modals_views.AddEmailAddressView.as_view(),
        urlname=model_urlname(models.Email, "add"),
    ),
    autopath(
        person_modals_views.EditEmailAddressView.as_view(),
        urlname=model_urlname(models.Email, "edit"),
    ),
    autopath(
        basxconnect.core.views.tag_views.bulk_tag_operation_view,
        urlname=model_urlname(models.Person, "bulk-tag-operation"),
    ),
    autopath(
        basxconnect.core.views.tag_views.AddTagView.as_view(),
        urlname=model_urlname(models.Term, "ajax_add"),
    ),
]
