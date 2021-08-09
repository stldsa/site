from django.contrib import admin
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from .models import CommitteePage, Person, Committee


class CommitteeAdmin(ModelAdmin):
    model = CommitteePage
    menu_label = "Committees"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    # list_display = ('name','formation_type')


class PersonAdmin(ModelAdmin):
    model = Person
    menu_label = "People"
    menu_order = 400


modeladmin_register(CommitteeAdmin)
modeladmin_register(PersonAdmin)

# Register your models here.
admin.site.register(Person)
admin.site.register(Committee)
admin.site.register(CommitteePage)