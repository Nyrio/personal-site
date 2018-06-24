from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from simple_email_confirmation.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

from .forms import CustomUserCreationForm, UserSettingsForm, BlogSearchForm
from .models import User, BlogPost  # , BlogComment


def index(request):
    """ Currently the index view is just a redirection to the CV view.
    In the future there might be a custom homepage.
    """
    return HttpResponseRedirect(reverse("about"))


def about(request):
    """ The about view shows the CV.
    """
    mdname = "CV_%s.md" % get_language()
    cvmd = render_to_string(mdname)
    return render(request, "about.html", context={"cvmd": cvmd})


class BlogView(generic.ListView):
    """ Displays the list of blog posts as a responsive grid.
    Supports pagination and sorting by category and keywords.
    """

    model = BlogPost
    template_name = "blog.html"
    paginate_by = 12

    def get_queryset(self):
        """Get all the blogposts and filter them according to GET parameters
        """

        qs = BlogPost.objects.all()

        keywords = self.request.GET.get("keywords", "").split(" ")
        for word in keywords:
            if get_language() == "fr":
                qs = qs.filter(title_fr__icontains=word)
            else:
                qs = qs.filter(title_en__icontains=word)

        category = self.request.GET.get("category", "")
        if category:
            qs = qs.filter(category=category)

        qs = qs.distinct()

        return qs

    def get_context_data(self, object_list=None, **kwargs):
        """ Used to get the search form and pagination info
        """

        context = super().get_context_data(**kwargs)

        form = BlogSearchForm(self.request.GET)
        context["form"] = form

        if context["is_paginated"]:
            page_range = list(context["paginator"].page_range)
            page_number = context["page_obj"].number
            if len(page_range) <= 3:
                context["custom_range"] = page_range
            elif page_number == 1:
                context["custom_range"] = page_range[:3]
            elif context["page_obj"].number == context["paginator"].num_pages:
                context["custom_range"] = page_range[-3:]
            else:
                context["custom_range"] = page_range[page_number - 2:
                                                     page_number + 1]
        return context


class BlogPostView(generic.DetailView):
    """View where the user can play a game that they have purchased and see scores.
    """

    model = BlogPost
    template_name = "blogpost.html"

    def get_context_data(self, **kwargs):
        """ Add some info in context (e.g comments)
        """

        context = super().get_context_data(**kwargs)
        blogpost = context["object"]
        context["comments"] = blogpost.comments.all()
        return context


# User account and registration

class RegistrationView(generic.FormView):
    """ Registration of a new user.
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


class UserSettingsView(generic.UpdateView):
    """ Update of an existing user
    """
    model = User
    form_class = UserSettingsForm
    template_name = "registration/user_settings.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        """ Gets the current user.
        """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.get_object()
        return context

    def form_valid(self, form):
        form.save()
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
