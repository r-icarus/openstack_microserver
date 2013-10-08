import logging

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tables

LOG = logging.getLogger(__name__)


class AdminHypervisorsTable(tables.DataTable):
    name = tables.Column("name",
                            verbose_name=_("Name"))

    recipe_type = tables.Column("recipe_type",
                                    verbose_name=_("Type"))

    created_at = tables.Column("created_at",
                          verbose_name=_("Created at"))


    class Meta:
        name = "recipes"
        verbose_name = _("All Servers")
