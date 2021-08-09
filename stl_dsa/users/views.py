from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    pk_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "email"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"id": self.request.user.pk})

    def get_object(self):
        return User.objects.get(id=self.request.user.pk)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Info successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"id": self.request.user.id})


user_redirect_view = UserRedirectView.as_view()
