from allauth.account.views import LoginView, SignupView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserSignupView(SignupView):
    def get_initial(self):
        email = self.request.session.get("email")
        return {"email": email} if email else {}


class UserLoginView(LoginView):
    def get_initial(self):
        post = self.request.POST.copy()
        post["login"] = post["email"]
        self.request.POST = post


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self):
        user = self.request.user
        user.update_membership()
        return user


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name"]

    def get_success_url(self):
        return reverse("users:detail")

    def get_object(self):
        return User.objects.get(id=self.request.user.pk)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Info successfully updated")
        )
        return super().form_valid(form)
