from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path, reverse_lazy
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext_lazy as _

from mainsite import views

urlpatterns = [
    path('', views.index),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

urlpatterns += i18n_patterns(
    path(_(''), views.index, name='index'),
    path(_('about/'), views.about, name='about'),
    path(_('blog/'), views.blog, name='blog'),

    path(_('signup/'), views.RegistrationView.as_view(), name="signup"),
    path(_('activate/<key>/'), views.confirm_email, name="confirm_email"),

    path(_('accounts/login/'), auth_views.LoginView.as_view(), name='login'),
    path(_('accounts/logout/'), auth_views.LogoutView.as_view(next_page=reverse_lazy("index")), name='logout'),
    path(_('accounts/reset-password/'), auth_views.PasswordResetView.as_view(success_url=reverse_lazy("index")), name="password-reset"),
    path(_('accounts/reset-password-done/'), auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path(_('accounts/reset-password-confirm/<uidb64>/<token>/'), auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy("index")),
        name='password_reset_confirm'),
    path(_('accounts/reset-password-complete/'), auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
)