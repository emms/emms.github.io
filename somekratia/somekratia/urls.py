"""somekratia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app.views import index, login_view, issues_bbox, logout_view, subscribe_issue
from app.views import issue
from app.views import issues_search_text, issues_category
from app.views import post_message, edit_message
from app.views import categories
from app.views import vote_message
from app.views import issues_with_messages
from app.views import decisions
from app.views import register
from app.views import user_profile, user_picture, messages
from app.views import get_issue_subscriptions
from app.views import current_user, reply_to_message, recent_decisions
from app.views import update_user_picture
from django.views.generic import RedirectView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^user/$', current_user),
    url(r'^user/picture$', update_user_picture),
    url(r'^user/(?P<userID>[0-9]+)/$', user_profile),
    url(r'^user/(?P<userID>[0-9]+)/picture$', user_picture),
    url(r'^user/(?P<userID>[0-9]+)/subscriptions', get_issue_subscriptions),
    url(r'^user/subscriptions$', get_issue_subscriptions),
    url(r'^admin/', include(admin.site.urls)),
    url(r'index.html', index),
    url(r'^$', index),
    url(r'^login', login_view),
    url(r'^logout', logout_view),
    url(r'^issues/area$', issues_bbox),
    url(r'^issues/text/$', issues_search_text),
    url(r'^issues/category/(?P<category_id>[0-9]+)/$', issues_category),
    url(r'^issues/recent$', recent_decisions),
    url(r'^$', index),
    url(r'^issue/(?P<issueID>[0-9]+)/$', issue),
    url(r'^issue/(?P<issueID>[0-9]+)/messages/$', post_message),
    url(r'^categories/', categories),
    url(r'^message/(?P<messageID>[0-9]+)/$', edit_message),
    url(r'^message/(?P<messageID>[0-9]+)/vote$', vote_message),
    url(r'^issues/recent/comments', issues_with_messages),
    url(r'^issue/(?P<issueID>[0-9]+)/decisions', decisions),
    url(r'^issue/(?P<issueID>[0-9]+)/subscribe', subscribe_issue),
    url(r'^issue/(?P<issueID>[0-9]+)/messages', messages),
    url(r'^message/(?P<messageID>[0-9]+)/reply$', reply_to_message),
    url(r'^accounts/login/$', RedirectView.as_view(url='/')),
    url(r'^reset_password', 'django.contrib.auth.views.password_reset'),
    url('^', include('django.contrib.auth.urls')),
]
