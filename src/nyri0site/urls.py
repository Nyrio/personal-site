from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
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
    url(_(r'^$'), views.index, name='index'),
    url(_(r'^about/$'), views.about, name='about'),
    url(_(r'^blog/$'), views.blog, name='blog'),

    url(_(r'^signup/$'), views.RegistrationView.as_view(), name="signup"),
    url(_(r'^activate/(?P<key>[\w\-]+)/$'), views.confirm_email, name="confirm_email"),

    url(_(r'^accounts/login/$'), auth_views.LoginView.as_view(), name='login'),
    url(_(r'^accounts/logout/$'), auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    url(_(r'^accounts/reset-password/$'), auth_views.PasswordResetView.as_view(), name="password-reset"),
    url(_(r'^accounts/reset-password-done/$'), auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    url(_(r'^accounts/reset-password-confirm/<uidb64>/<token>/$'), auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(_(r'^accounts/reset-password-complete/$'), auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
)