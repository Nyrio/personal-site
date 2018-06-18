from django import template
import markdown as markdown

register = template.Library()


@register.filter
def parse_markdown(text):
    extensions = [
        "markdown.extensions.extra",
        "markdown.extensions.codehilite",
        "markdown.extensions.meta",
        "markdown.extensions.toc",
        "markdown.extensions.smarty",
        "urlize",
    ]
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
parse_markdown.is_safe = True


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
