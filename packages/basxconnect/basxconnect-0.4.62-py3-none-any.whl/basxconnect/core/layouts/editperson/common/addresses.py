import django.db.models
import htmlgenerator as hg
from basxbread import layout
from basxbread.layout import ObjectFieldValue
from basxbread.layout.components.datatable import DataTableColumn
from basxbread.layout.components.icon import Icon
from basxbread.layout.components.modal import modal_with_trigger
from basxbread.utils import ModelHref, reverse_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from htmlgenerator import mark_safe

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.utils import tile_with_icon, tiling_col

R = layout.grid.Row
C = layout.grid.Col


def numbers():
    return tile_with_datatable(
        models.Phone,
        hg.F(lambda c: c["object"].core_phone_list.all()),
        ["number", "type"],
    )


def tile_with_datatable(model, queryset, columns):
    addmodal = layout.modal.Modal.with_ajax_content(
        _("Add"),
        ModelHref(
            model,
            "add",
            query=hg.F(lambda c: {"person": c["object"].pk, "asajax": True}),
        ),
        submitlabel=_("Save"),
    )

    def editmodal():
        return hg.F(
            lambda c: modal_with_trigger(
                layout.modal.Modal.with_ajax_content(
                    _("Edit"),
                    ModelHref(hg.C("row"), "edit", query={"asajax": True}),
                    submitlabel=_("Save"),
                ),
                layout.button.Button,
                notext=True,
                small=True,
                buttontype="ghost",
                icon="edit",
                label=_("Edit"),
                _class="bx--overflow-menu",
            )
        )

    return tiling_col(
        layout.datatable.DataTable.from_queryset(
            queryset,
            model=model,
            prevent_automatic_sortingnames=True,
            columns=columns,
            rowactions=[
                editmodal(),
                layout.button.Button(
                    _("Delete"),
                    icon="trash-can",
                    notext=True,
                    small=True,
                    buttontype="ghost",
                ).as_submit(
                    href=ModelHref(
                        model,
                        "delete",
                        kwargs={"pk": hg.C("row.pk")},
                    ),
                ),
            ],
            primary_button=layout.button.Button(
                _("Add"), buttontype="primary", **addmodal.openerattributes
            ),
            style="border-top: none;",
        ),
        addmodal,
    )


def email():
    return tile_with_datatable(
        models.Email,
        hg.F(lambda c: c["object"].core_email_list.all()),
        [
            "email",
            DataTableColumn(
                layout.ObjectFieldLabel("type", models.Email),
                hg.SPAN(
                    hg.C("row.type"),
                    hg.If(
                        hg.F(
                            lambda c: c["row"] == c["row"].person.primary_email_address
                        ),
                        hg.BaseElement(" (", _("primary"), ")"),
                        "",
                    ),
                ),
            ),
        ],
    )


def urls():
    return tile_with_datatable(
        models.Web,
        hg.F(lambda c: c["object"].core_web_list.all()),
        ["url", "type"],
    )


def edit_heading(model: type):
    return _("Edit %s") % model._meta.verbose_name


def display_postal():
    postal = hg.C("i")
    modal = layout.modal.Modal.with_ajax_content(
        heading=edit_heading(models.Postal),
        url=ModelHref(
            models.Postal,
            "ajax_edit",
            kwargs={"pk": postal.pk},
            query={"asajax": True},
        ),
        id=hg.format("postal-modal-{}", hg.C("i").id),
        submitlabel=_("Save"),
    )
    is_inactive = hg.F(
        lambda c: c["i"].valid_until and c["i"].valid_until < timezone.now().date()
    )
    return R(
        C(
            hg.DIV(
                postal.type,
                hg.If(
                    hg.F(
                        lambda c: c["i"].person.primary_postal_address
                        and c["i"].person.primary_postal_address.pk == c["i"].pk
                    ),
                    hg.BaseElement(" (", _("primary"), ")"),
                ),
                style="font-weight: bold; margin-bottom: 1rem;",
            ),
            hg.DIV(
                ObjectFieldValue("address", object_contextname="i"),
                style="margin-bottom: 0.25rem;",
            ),
            hg.DIV(postal.postcode, " ", postal.city, style="margin-bottom: 0.25rem;"),
            hg.DIV(postal.get_country_display()),
            hg.If(
                postal.valid_from,
                hg.DIV(
                    hg.SPAN(_("Valid from: "), style="font-weight: bold;"),
                    ObjectFieldValue("valid_from", object_contextname="i"),
                    " ",
                    style="display: inline-block; margin-top: 1rem; margin-right: 1rem;",
                ),
                hg.BaseElement(),
            ),
            hg.If(
                postal.valid_until,
                hg.DIV(
                    hg.SPAN(_("Valid until: "), style="font-weight: bold;"),
                    ObjectFieldValue("valid_until", object_contextname="i"),
                    style="display: inline-block; margin-top: 1rem;",
                ),
                hg.BaseElement(),
            ),
            hg.DIV(
                edit_postal_button(modal),
            ),
        ),
        _class=hg.If(is_inactive, "inactive_postal", ""),
        style=hg.If(
            is_inactive,
            "display: none; margin-top: 1.5rem; color: #a8a8a8;",
            "margin-top: 1.5rem;",
        ),
    )


def edit_postal_button(modal):
    return hg.SPAN(
        layout.button.Button(
            "",
            buttontype="ghost",
            icon="edit",
            **modal.openerattributes,
        ),
        modal,
    )


def delete_postal_button(postal):
    return layout.button.Button(
        _("Delete"),
        buttontype="ghost",
        icon="trash-can",
        notext=True,
        hx_post=reverse_model(
            models.Postal,
            "ajax_delete",
            kwargs={
                "pk": postal.pk,
            },
            query={
                "asajax": True,
            },
        ),
    )


def postals():
    return tile_with_icon(
        Icon("map"),
        hg.H4(_("Address(es)")),
        R(
            C(
                hg.Iterator(
                    hg.F(
                        lambda c: (
                            getattr(c["object"], "core_postal_list")
                            .order_by(
                                django.db.models.F("valid_until").desc(nulls_first=True)
                            )
                            .all()
                            if hasattr(c["object"], "core_postal_list")
                            else []
                        )
                    ),
                    "i",
                    display_postal(),
                )
            )
        ),
        R(
            C(
                layout.button.Button(
                    _("Hide inactive postals"),
                    onclick="hideInactivePostals();",
                    id="hideInactivePostalsButton",
                    style="display: none;",
                    icon="view--off",
                    buttontype="ghost",
                ),
                layout.button.Button(
                    _("Show inactive postals"),
                    onclick="showInactivePostals();",
                    id="showInactivePostalsButton",
                    icon="view",
                    buttontype="ghost",
                ),
            ),
            style="margin-top: 1.5rem;",
        ),
        R(
            C(
                modal_with_trigger(
                    modal_add_postal(),
                    layout.button.Button,
                    _("Add"),
                    buttontype="ghost",
                    icon="add",
                ),
            ),
        ),
        hg.SCRIPT(
            mark_safe(
                """
                function hideInactivePostals() {
                    for(i of $$('.inactive_postal')) {
                        $(i)._.style({display: "none"});
                    }
                    $$('#hideInactivePostalsButton')._.style({display: "none"})
                    $$('#showInactivePostalsButton')._.style({display: "block"})
                }
                function showInactivePostals() {
                    for(i of $$('.inactive_postal')) {
                        $(i)._.style({display: "block"});
                    }
                    $$('#hideInactivePostalsButton')._.style({display: "block"})
                    $$('#showInactivePostalsButton')._.style({display: "none"})
                }
                """
            )
        ),
    )


def modal_add_postal():
    return layout.modal.Modal.with_ajax_content(
        heading=_("Add Address"),
        url=hg.F(
            lambda c: reverse_model(
                models.Postal,
                "ajax_add",
                query={"asajax": True, "person": c["object"].pk},
            ),
        ),
        submitlabel=_("Save"),
    )
