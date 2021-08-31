# from home.models import HomePage
# from news.models import NewsPage
# import datetime
#
#
# def test_home_page(db, rf, faker):
#     home_page = HomePage(
#         title="St Louis DSA",
#         banner_title="Welcome to St Louis DSA!",
#         mission_statement=faker.sentence(10),
#         values_statement=faker.sentence(10),
#         highlighted_campaign=f"{' '.join(faker.words(2)).title()} Campaign",
#         highlighted_description=faker.paragraph(5),
#     )
#     news_page = NewsPage.objects.create(
#         title=faker.sentence(),
#         date=datetime.date.today(),
#         body=faker.paragraph(30),
#         show_in_menus=True,
#     )
#     request = rf.post("/", {"email": faker.email()})
#     home_page.serve(request)
