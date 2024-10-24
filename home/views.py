from home.forms import EmailSubmissionForm
from django.views.generic.edit import FormView
from stldsa.users.models import User


class EmailFormView(FormView):
    template_name = "main_menu.html"
    form_class = EmailSubmissionForm

    def get_success_url(self, **kwargs):
        emails = kwargs.get("emails", None) or User.objects.values_list(
            "email", flat=True
        )
        return (
            "/login/"
            if self.get_form_kwargs()["data"]["email"] in emails
            else "/signup/"
        )
