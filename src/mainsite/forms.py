from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import Category, BlogComment


class CustomUserCreationForm(UserCreationForm):
    """ Extension of the default user creation form to add the email
    confirmation and the profile picture.
    """
    error_css_class = "field-error"
    required_css_class = "field-required"

    email = forms.EmailField(label=_("Your email address"))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "avatar")


class UserSettingsForm(forms.ModelForm):
    """ Provides a form to edit some account settings
    """
    error_css_class = "field-error"
    required_css_class = "field-required"

    class Meta:
        model = get_user_model()
        fields = ("username", "avatar")


class BlogSearchForm(forms.Form):
    """ Provides a form to sort blog posts
    """
    error_css_class = "field-error"
    required_css_class = "field-required"

    def category_choices():
        choices = [("", _("any category"))]
        for category in Category.objects.all():
            if get_language() == "fr":
                choices.append((category.pk, category.name_fr))
            else:
                choices.append((category.pk, category.name_en))
        return choices

    keywords = forms.CharField(label=_("Keywords"), max_length=128, required=False, )
    category = forms.ChoiceField(label=_("Category"), choices=category_choices, required=False, )


class CommentForm(forms.ModelForm):
    """ Provides a form to post a comment on a blog post.
    """
    error_css_class = "field-error"
    required_css_class = "field-required"

    class Meta:
        model = BlogComment
        fields = ("text", "user", "blogpost",)
        widgets = {
          'text': forms.Textarea(attrs={'rows': 4, }),
          "user": forms.HiddenInput(),
          "blogpost": forms.HiddenInput(),
        }
