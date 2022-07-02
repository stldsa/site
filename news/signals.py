from django.conf import settings
from wagtail.signals import page_published
from actionnetwork.email import create
from django.dispatch import receiver
from news.models import NewsPage


@receiver(page_published, sender=NewsPage)
def create_email(sender, **kwargs):
    newspage = kwargs["instance"]
    response = create(
        newspage.title,
        newspage.body,
        "STL DSA",
        "info@stldsa.org",
        settings.ACTIONNETWORK_API_KEYS["main"],
    )
    print(response.content)
    # status = "calculating"
    # while status != "draft":re
    #     time.sleep(1)
    #     response = requests.get(
    #         response["_links"]["self"]["href"],
    #         headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    #     )
    #     data = json.loads(response.content)
    #     status = data["status"]
    # schedule_helper = data["_links"]["osdi:schedule_helper"]["href"]
    # response = requests.post(
    #     schedule_helper,
    #     headers={"OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS["main"]},
    #     json={"scheduled_start_date": datetime.datetime(2024, 1, 1)},
    # )
    # print(response.contents)
