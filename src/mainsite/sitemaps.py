from django.contrib.sitemaps import Sitemap
from .models import BlogPost


class PostsMap(Sitemap):
    """ Blog posts sitemap for the given language.
    """
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def __init__(self, language="en"):
        self.language = language

    def items(self):
        return BlogPost.objects.filter()

    def location(self, item):
        return "/%s/blog/%d" % (self.language, item.pk)

    def lastmod(self, item):
        return item.date


class MiscViewsMap(Sitemap):
    pages = {
        "aboutfr": ["/fr/about/", 1.0, "weekly"],
        "abouten": ["/en/about/", 1.0, "weekly"],
        "blogfr": ["/fr/blog/", 1.0, "daily"],
        "blogen": ["/en/blog/", 1.0, "daily"],
    }
    protocol = "https"

    def items(self):
        return list(self.pages.keys())

    def location(self, item):
        return self.pages[item][0]

    def priority(self, item):
        return self.pages[item][1]

    def changefreq(self, item):
        return self.pages[item][2]
