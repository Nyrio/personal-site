from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from simple_email_confirmation.models import EmailAddress
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm


def index(request):
    return HttpResponseRedirect(reverse("about"))


def about(request):
    return render(request, "about.html")


def blog(request):
    return render(request, "blog.html")


# User account and registration

class RegistrationView(generic.FormView):
    """Registration of a new user.
    """
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password1"])
        login(self.request, user)
        rlnk = reverse("confirm_email", kwargs={"key": user.confirmation_key})
        link = "http://" + self.request.META['HTTP_HOST'] + rlnk
        email_text = render_to_string("registration/activation_email.html",
                                      request=self.request,
                                      context={"link": link})
        send_mail(_("Email confirmation for nyri0.fr"),
                  _("Activate html to see this email."),
                  from_email="nyri0bot",
                  recipient_list=[user.email],
                  html_message=email_text.format(user.username, link, link))
        return super().form_valid(form)


def confirm_email(request, key):
    """ Confirmation of an email via the link provided to this address.
    """
    try:
        email = EmailAddress.objects.get(key=key)
        email.user.confirm_email(key)
        return render(request, "registration/activate.html",
                      context={"activate_success": True})
    except Exception:
        return render(request, "registration/activate.html",
                      context={"activate_success": False})
