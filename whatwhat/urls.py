from django.conf.urls import patterns, url
from whatwhat.views import IndexView, MarkItWhatView

urlpatterns = patterns('',
    url(
        r"^$",
        IndexView.as_view(),
        name='index'
    ),
    url(
        r'mark_it_what/$',
        MarkItWhatView.as_view(),
        name='mark_it_what'
    )
)
