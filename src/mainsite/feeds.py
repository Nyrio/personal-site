from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from .models import BlogPost
from .templatetags.misc_tags import parse_comment_markdown


class PostsFeed(Feed):
    title = _("Nyri0's Devblog")
    link = reverse_lazy("blog")
    feed_url = reverse_lazy("feed")
    description = _("Updates on blog entries - English version.")
    author_name = "Louis Sugy"
    author_link = reverse_lazy("about")

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

    def item_enclosure_url(self, item):
        return self.request.build_absolute_uri(item.cover_picture.url)
