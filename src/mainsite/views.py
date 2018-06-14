from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib import messages
from simple_email_confirmation.models import EmailAddress

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
        link = self.request.META['HTTP_HOST'] + rlnk
        email_en = """
            <p>Hi {},</p>
            <p>Welcome to nyri0.fr!<p>
            <p>Use the following link to confirm your email:
            <a href="http://{}">http://{}</a></p>
            <p>After confirmation, you will be able to comment on
            posts. Please make the comments space a place where it is pleasant
            for everyone to talk and share their opinion.</p>
            <p>---<br>
            This is an auto-generated email. Please don't reply.</p>
            """
        send_mail("Email Confirmation for nyri0.fr",
                  "Welcome to our website!",
                  from_email="nyri0bot",
                  recipient_list=[user.email],
                  html_message=email_en.format(user.username, link, link))
        return super().form_valid(form)


def confirm_email(request, key):
    """ Confirmation of an email via the link provided to this address.
    """
    email = EmailAddress.objects.get(key=key)
    email.user.confirm_email(key)
    messages.add_message(request, messages.INFO, "Email verified!")
    return HttpResponseRedirect("/")
