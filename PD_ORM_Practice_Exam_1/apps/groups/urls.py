from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^groups/login$', views.login),
    url(r'^groups/age_groups$', views.age_groups),
    url(r'^groups/group_members/(?P<age_range>[0-9_.-]*)$', views.group_members),
    url(r'^groups/add_comment/(?P<age_range>[0-9_.-]*)$', views.add_comment),
    url(r'^groups/save_comment/(?P<age_range>[0-9_.-]*)$', views.save_comment),
    url(r'^groups/logout$', views.logout),
    url(r'^$', views.index)
]
