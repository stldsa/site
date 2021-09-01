from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import CommitteePage


class CommitteeAdmin(ModelAdmin):
    model = CommitteePage
    menu_label = "Committees"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    # list_display = ('name','formation_type')


modeladmin_register(CommitteeAdmin)
