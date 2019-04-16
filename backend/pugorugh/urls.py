from django.urls import path, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import UserRegisterView

from . import views

# API endpoints
urlpatterns = format_suffix_patterns([
    # API auth
    path(r'api_auth/', include(
        'rest_framework.urls', namespace="rest_framework")),
    path(r'api/user/login/', obtain_auth_token, name='login-user'),
    path(r'api/user/', UserRegisterView.as_view(), name='register-user'),
    # favicon
    path(r'favicon\.ico',
         RedirectView.as_view(
             url='/static/icons/favicon.ico',
             permanent=True
         )),
    # index
    path(r'', TemplateView.as_view(template_name='index.html')),

    # API functions
    # To change or set user preferences
    path(r'api/user/preferences/',
         views.SetUserPref.as_view(), name='userpref'),
    # name='userpref'),

    #   To get the next liked/disliked/undecided dog:
    #    /api/dog/<pk>/liked/next/
    path(r'api/dog/<int:pk>/liked/next/',
         views.LikedNext.as_view(), name='UndecidedNext'),
    #    /api/dog/<pk>/disliked/next/
    path(r'api/dog/<int:pk>/disliked/next/',
         views.DislikedNext.as_view(), name='UndecidedNext'),
    path(r'api/dog/<int:pk>/undecided/next/',
         views.UndecidedNext.as_view(), name='UndecidedNext'),

    #    To change the dog's status

    #    /api/dog/<pk>/liked/
    path(r'api/dog/<int:pk>/liked/',
         views.Liked.as_view(), name='Liked'),
    #    /api/dog/<pk>/disliked/
    path(r'api/dog/<int:pk>/disliked/',
         views.Disliked.as_view(), name='Disliked'),
    #    /api/dog/<pk>/undecided/
    path(r'api/dog/<int:pk>/undecided/',
         views.Undecided.as_view(), name='Undecided'),
])
