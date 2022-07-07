from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from news.models import NewsIndexPage


class NewsIndexPageAdmin(ModelAdmin):
    model = NewsIndexPage
    ordering = "-last_published_at"


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(NewsIndexPageAdmin)
