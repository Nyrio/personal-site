from django.db import models
from django.contrib.auth.models import AbstractUser
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from stdimage.models import StdImageField
from django.utils.translation import gettext_lazy as _


class User(SimpleEmailConfirmationUserMixin, AbstractUser):
    """ Extension of Django's user model with email authentication and
    profile picture.
    """
    avatar = StdImageField(upload_to='profilepics', blank=True,
      help_text=_("Please use a square image to avoid cutting"),
      variations={
          'thumbnail': {"width": 64, "height": 64, "crop": True},
          'comment': {"width": 256, "height": 256, "crop": True},
      })

    def __str__(self):
        return "%s (%s)" % (self.username, self.email)


class Category(models.Model):
    """ Category for a blog post.
    """
    name = models.CharField(max_length=64, unique=True)
    glyphicon_name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class BlogPost(models.Model):
    """ Blog post, with support of two languages: French and English.
    """
    title_fr = models.CharField(max_length=128)
    title_en = models.CharField(max_length=128)
    description_fr = models.TextField(max_length=512)
    description_en = models.TextField(max_length=512)
    text_fr = models.TextField()
    text_en = models.TextField()
    cover_picture = StdImageField(upload_to='coverpics', blank=True,
      help_text=_("Cut in 21:9 for both on-site display and sharing"),
      variations={
          'gridview': {"width": 504, "height": 216, "crop": True},
          'ogtag': {"width": 1260, "height": 540, "crop": True},
      })
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name="blogposts")

    def __str__(self):
        return self.title_en


class BlogComment(models.Model):
    """ Comment written by a user on a blog post.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE,
                                 related_name="comments")
    text = models.TextField(help_text=_("You can use markdown formatting"))

    def __str__(self):
        return "%s - %s - %s" % (self.blogpost.title_en, self.user.username,
                                 self.text[:32])
