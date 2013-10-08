import logging

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tables

LOG = logging.getLogger(__name__)


class CreateRecipe(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Recipe")
    url = "horizon:admin:recipes:create"
    classes = ("ajax-modal", "btn-create")

class MicroserverRecipesTable(tables.DataTable):
    name = tables.Column("name", verbose_name = _("Name"))

    recipe_type = tables.Column("recipe_type", verbose_name = _("Type"))

    created_at = tables.Column("created_at", verbose_name = _("Created at"))

    status = tables.Column("status", verbose_name = _("Status"))

    class Meta:
        name = "recipes"
        verbose_name = _("All Servers")
        table_actions = (CreateRecipe, )
        #row_actions = (DeleteRecipe)



    
