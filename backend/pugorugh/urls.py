from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView

from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    # API auth
    url(r'^api_auth/', include(
        'rest_framework.urls', namespace="rest_framework")),
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    # favicon
    url(r'^favicon\.ico',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    # index
    url(r'^', TemplateView.as_view(template_name='index.html')),

    # API functions
    # To change or set user preferences
    url(r'^api/user/preferences/$',
        views.SetUserPref.as_view(), name='userpref'),

    #   To get the next liked/disliked/undecided dog:
    #    /api/dog/<pk>/liked/next/
    url(r'^api/dog/(?P<pk>-?\d+)/liked/next/$',
        views.LikedNext.as_view(), name='UndecidedNext'),
    #    /api/dog/<pk>/disliked/next/
    url(r'^api/dog/(?P<pk>-?\d+)/disliked/next/$',
        views.DislikedNext.as_view(), name='UndecidedNext'),
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/next/$',
        views.UndecidedNext.as_view(), name='UndecidedNext'),

    #    To change the dog's status

    #    /api/dog/<pk>/liked/
    url(r'^api/dog/(?P<pk>-?\d+)/liked/$',
        views.Liked.as_view(), name='Liked'),
    #    /api/dog/<pk>/disliked/
    url(r'^api/dog/(?P<pk>-?\d+)/disliked/$',
        views.Disliked.as_view(), name='Disliked'),
    #    /api/dog/<pk>/undecided/
    url(r'^api/dog/(?P<pk>-?\d+)/undecided/$',
        views.Undecided.as_view(), name='Undecided'),
])
