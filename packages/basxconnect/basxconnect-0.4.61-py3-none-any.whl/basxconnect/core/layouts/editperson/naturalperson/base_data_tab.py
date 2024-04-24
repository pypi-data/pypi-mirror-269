import htmlgenerator as hg
from basxbread import layout
from basxbread.layout import ObjectFieldLabel
from basxbread.layout.components.icon import Icon
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common import addresses, base_data, utils
from basxconnect.core.layouts.editperson.common.utils import (
    display_label_and_value,
    person_metadata,
)

R = layout.grid.Row
C = layout.grid.Col


def base_data_tab():
    return layout.tabs.Tab(
        _("Personal data"),
        utils.grid_inside_tab(
            R(
                personal_data(),
                person_metadata(models.NaturalPerson),
            ),
            base_data.common_tiles(),
        ),
    )


def personal_data():
    displayed_fields = (
        [
            utils.display_field_label_and_value(field)
            for field in [
                "salutation",
                "title",
                "name",
                "first_name",
                "last_name",
            ]
        ]
        + [
            hg.If(
                hg.C("object.middle_name"),
                utils.display_field_label_and_value("middle_name"),
            )
        ]
        + [
            hg.If(
                hg.C("object.maiden_name"),
                utils.display_field_label_and_value("maiden_name"),
            )
        ]
        + [
            utils.display_field_label_and_value(field)
            for field in [
                "gender",
                "date_of_birth",
                "place_of_birth",
                "profession",
            ]
        ]
        + [
            hg.If(
                hg.C("object.deceased"),
                display_label_and_value(
                    ObjectFieldLabel("deceased"),
                    hg.If(hg.C("object.deceased"), _("Yes"), _("No")),
                ),
            ),
            hg.If(
                hg.C("object.deceased"),
                utils.display_field_label_and_value("decease_date"),
            ),
        ]
    )
    return utils.tile_col_edit_modal_displayed_fields(
        _("Personal Data"),
        models.NaturalPerson,
        "ajax_edit_personal_data",
        Icon("user--profile"),
        displayed_fields,
    )


def contact_details_naturalperson(request):
    return hg.BaseElement(
        R(
            addresses.postals(),
            addresses.numbers(request),
        ),
        R(
            addresses.email(request),
            addresses.urls(request),
        ),
        R(
            base_data.tags(),
            base_data.other(),
        ),
    )
