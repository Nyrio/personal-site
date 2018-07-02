from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from simple_email_confirmation.models import EmailAddress
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from django.db.models import F

from .forms import CustomUserCreationForm, UserSettingsForm, BlogSearchForm, CommentForm
from .models import User, BlogPost


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


def robots_view(request):
    """ Serving the robots.txt from corresponding template.
    """
    robots_txt = render_to_string("robots.txt")
    return HttpResponse(robots_txt, content_type='text/plain')


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


class BlogPostView(generic.DetailView, generic.edit.FormMixin):
    """ View of a blog post and its comments.
    """

    model = BlogPost
    template_name = "blogpost.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        """ Add some info in context:
            comments, form to post comment, other articles.
        """

        context = super().get_context_data(**kwargs)
        blogpost = context["object"]

        # Get comments related to this blog post
        context["comments"] = blogpost.comments.all()

        # Get the form to comment
        context["form"] = CommentForm(initial={"user": self.request.user,
                                               "blogpost": self.get_object()})

        # Get all blog post for the side bar on large screens
        if get_language() == "fr":
            months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                      "Juillet", "Août", "Septembre", "Octobre", "Novembre",
                      "Décembre"]
        else:
            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November",
                      "December"]
        months_posts = {}
        for otherpost in BlogPost.objects.values('pk', 'date',
                                                 'title_%s' % get_language()):
            post_date = otherpost["date"]
            date_code = "%d%02d" % (post_date.year, post_date.month)
            date_str = "%s %d" % (months[post_date.month - 1], post_date.year)
            if date_code not in months_posts:
                months_posts[date_code] = (date_str, [])
            months_posts[date_code][1].append({
                "title": otherpost["title_%s" % get_language()],
                "url": reverse_lazy("blogpost", kwargs={"pk": otherpost["pk"]})})

        otherposts = []
        for date_code in reversed(sorted(months_posts)):
            otherposts.append((months_posts[date_code][0],
                               months_posts[date_code][1]))

        context["otherposts"] = otherposts

        return context

    def post(self, request, *args, **kwargs):
        """ Handle comments on POST requests.
        """
        if not request.user.is_authenticated or not request.user.is_confirmed:
            return HttpResponseForbidden()

        form = self.get_form()
        self.object = self.get_object()

        # pdb.set_trace()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """ Post the comment if the form is valid.
        """
        if form.cleaned_data["user"] != self.request.user:
            return self.form_invalid(form)
        if form.cleaned_data["blogpost"] != self.get_object():
            return self.form_invalid(form)

        form.save()
        return super(BlogPostView, self).form_valid(form)

    def form_invalid(self, form):
        return super(BlogPostView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("blogpost", kwargs={'pk': self.get_object().pk})


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


# Error pages

def handler404(request, *args, **kwargs):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request, *args, **kwargs):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response


def handler403(request, *args, **kwargs):
    response = render(request, '403.html', {})
    response.status_code = 403
    return response


def handler400(request, *args, **kwargs):
    response = render(request, '400.html', {})
    response.status_code = 400
    return response
