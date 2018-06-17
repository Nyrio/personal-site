# from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    avatar = StdImageField(upload_to='profilepics', blank=True,
      help_text=_("Please use a square image to avoid cutting"),
      variations={
          'thumbnail': {"width": 64, "height": 64, "crop": True},
          'comment': {"width": 256, "height": 256, "crop": True},
      })

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)
