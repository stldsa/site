from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from committees.models import CommitteePage


class CommitteeViewSet(SnippetViewSet):
    model = CommitteePage
    base_url_path = "formations"
    menu_label = "Formations"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
    icon = "group"
    list_filter = ("live",)


register_snippet(CommitteeViewSet)
