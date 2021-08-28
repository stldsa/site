# from pytest_drf import ViewSetTest, UsesGetMethod, Returns200, UsesListEndpoint
# from pytest_drf.util import pluralized, url_for
# from pytest_lambda import lambda_fixture

# from events.models import Event


# class TestEventViewSet(ViewSetTest):

#     list_url = lambda_fixture(lambda: url_for("events-list"))

#     def express_event(event: Event) -> dict[str, Any]:
#         return {
#             "id": event.id,
#             "title": event.title,
#             "start": event.start,
#             "url": event.url,
#         }

#     express_key_values = pluralized(express_key_values)

#     class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
#         events = lambda_fixture()

#         def test_it_returns_key_values(self, key_values, results):
#             expected = express_key_values(sorted(key_values, key=lambda kv: kv.id))
#             actual = results
#             assert expected == actual
