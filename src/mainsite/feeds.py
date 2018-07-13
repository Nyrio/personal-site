from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import BlogPost
from .templatetags.misc_tags import parse_comment_markdown


class CustomRssFeed(Rss201rev2Feed):
    """ Custom class to support cover pictures.
    """
    def __init__(self, title, link, description, **kwargs):
        kwargs["language"] = get_language()
        super().__init__(title, link, description, **kwargs)

    def rss_attributes(self):
        attributes = super().rss_attributes()
        attributes.update({"xmlns:media": "http://search.yahoo.com/mrss/"})
        return attributes

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        cover_url = item["cover"]
        handler.addQuickElement("media:content",
          contents=None,
          attrs={"url": cover_url})
        # handler.addQuickElement("atom:content",
        #   contents=None,
        #   attrs={"url": cover_url})
        item["cover"] = None


class PostsFeed(Feed):
    """ One unique feed class for two different feeds in the end/ EN and FR.
    """
    title = _("Nyri0's Devblog")
    link = reverse_lazy("blog")
    feed_url = reverse_lazy("feed")
    description = _("Updates on blog entries - English version.")
    author_name = "Louis Sugy"
    author_link = reverse_lazy("about")
    feed_type = CustomRssFeed

    def get_object(self, request):
        self.request = request

    def items(self):
        return BlogPost.objects.all().order_by("-date")[:10]

    def item_title(self, item):
        if get_language() == 'fr':
            return item.title_fr
        else:
            return item.title_en

    def item_description(self, item):
        if get_language() == 'fr':
            return parse_comment_markdown(item.description_fr)
        else:
            return parse_comment_markdown(item.description_en)

    def item_link(self, item):
        return reverse_lazy('blogpost', kwargs={'pk': item.pk})

    def item_pubdate(self, item):
        return item.date

    def item_extra_kwargs(self, item):
        return {
            "cover": self.request.build_absolute_uri(
                item.cover_picture.ogtag.url),
        }
