from home.forms import EmailSubmissionForm
from django.views.generic.edit import FormView
from stl_dsa.users.models import User


class EmailFormView(FormView):
    template_name = "home_page.html"
    form_class = EmailSubmissionForm

    def get_success_url(self, **kwargs):
        emails = kwargs.get("emails", [])
        return "/login/" if self.email in emails else "/signup/"
