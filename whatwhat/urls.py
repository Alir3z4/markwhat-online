from django.conf.urls import patterns, url
from whatwhat.views import IndexView

urlpatterns = patterns('',
    url(
        r"^$",
        IndexView.as_view(),
        name='index'
    ),
)
