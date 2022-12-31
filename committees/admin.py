from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from committees.models import CommitteePage


class CommitteeAdmin(ModelAdmin):
    model = CommitteePage
    menu_label = "Formations"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    menu_icon = "group"


modeladmin_register(CommitteeAdmin)
