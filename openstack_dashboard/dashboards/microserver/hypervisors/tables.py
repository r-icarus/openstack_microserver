import logging

from django.utils.translation import ugettext_lazy as _  # noqa

from horizon import tables

LOG = logging.getLogger(__name__)


class CreateRecipe(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Recipe")
    url = "horizon:microserver:recipes:create"
    classes = ("btn-create", )

class DeleteRecipe(tables.DeleteAction):
    data_type_singular = _("Recipe")
    data_type_plural = _("Recipes")

    def delete(self, request, obj_id):
        pass

class UpdateRecipe(tables.LinkAction):
    name = "update"
    verbose_name = _("Edit")
    url = "horizon:microserver:recipes:update"
    classes = ("btn-edit",)

class MicroserverRecipesTable(tables.DataTable):
    identity = tables.Column("id", verbose_name = _("Id"), hidden = True)
    name = tables.Column("name", verbose_name = _("Name"))
    recipe_type = tables.Column("recipe_type", verbose_name = _("Type"))
    created_at = tables.Column("created_at", verbose_name = _("Created at"))
    status = tables.Column("status", verbose_name = _("Status"))

    class Meta:
        name = "recipes"
        verbose_name = _("All Recipes")
        table_actions = (CreateRecipe,DeleteRecipe)
        row_actions = (UpdateRecipe, )



    
