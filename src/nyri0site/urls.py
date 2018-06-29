from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, reverse_lazy
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.utils.translation import ugettext_lazy as url_lazy
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap

from mainsite import views
from mainsite.feeds import PostsFeed
from mainsite.sitemaps import PostsMap, MiscViewsMap


sitemaps = {
    'sitemaps': PostsMap("fr"),
    'postsmapen': PostsMap("en"),
    'miscviews': MiscViewsMap,
}

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', views.robots_view, {}),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

urlpatterns += i18n_patterns(
    path(url_lazy(''), views.index, name='index'),
    path(url_lazy('about/'), views.about, name='about'),

    path(url_lazy('blog/'), views.BlogView.as_view(), name='blog'),
    path(url_lazy('blog/feed/'), PostsFeed(), name='feed'),
    path(url_lazy('blog/<int:pk>'), views.BlogPostView.as_view(), name='blogpost'),

    path(url_lazy('signup/'), views.RegistrationView.as_view(), name="signup"),
    path(url_lazy('activate/<key>/'), views.confirm_email, name="confirm_email"),

    path(url_lazy('accounts/login/'), auth_views.LoginView.as_view(), name='login'),
    path(url_lazy('accounts/logout/'), auth_views.LogoutView.as_view(next_page=reverse_lazy("index")), name='logout'),
    path(url_lazy('accounts/reset-password/'), auth_views.PasswordResetView.as_view(html_email_template_name="registration/password_reset_email.html"), name="password-reset"),
    path(url_lazy('accounts/reset-password-done/'), auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(url_lazy('accounts/reset-password-confirm/<uidb64>/<token>/'), auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path(url_lazy('accounts/reset-password-complete/'), auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path(url_lazy('accounts/user-settings/'), login_required(views.UserSettingsView.as_view()), name='user_settings'),
)

handler404 = 'mainsite.views.handler404'
handler500 = 'mainsite.views.handler500'
handler403 = 'mainsite.views.handler403'
handler400 = 'mainsite.views.handler400'
