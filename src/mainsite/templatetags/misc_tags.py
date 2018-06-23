from django.template import Library
import markdown as markdown

register = Library()


def common_markdown_parse(extensions, text):
    md = markdown.Markdown(safe_mode=True,
                           extensions=extensions)
    htmltxt = md.convert(text)

    replacements = {
        "<table": "<table class='table table-responsive table-bordered'",
        "<img": "<img class='img-responsive'",
        "[HTML_REMOVED]": "",
        "%newline%": "<br>",
    }
    for key in replacements:
        htmltxt = htmltxt.replace(key, replacements[key])

    return htmltxt


@register.filter
def parse_post_markdown(text):
    extensions = [
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.meta",
        "markdown.extensions.toc",
        "markdown.extensions.smarty",
        "markdown.extensions.nl2br",
        "urlize",
    ]
    return common_markdown_parse(extensions, text)
parse_post_markdown.is_safe = True


@register.filter
def parse_comment_markdown(text):
    extensions = [
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.smarty",
        "markdown.extensions.nl2br",
        "urlize",
    ]
    return common_markdown_parse(extensions, text)
parse_comment_markdown.is_safe = True


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def absolute_uri(request, relative_uri):
    return request.build_absolute_uri(relative_uri)
