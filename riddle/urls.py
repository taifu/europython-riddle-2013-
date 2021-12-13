from django.conf.urls import patterns, url

from .views import RiddleCaptchaView, RiddleDatesView, RiddleBriesView, WinnerView, HomeView

dict_views = dict((view.LEVEL, view) for view in
        (RiddleCaptchaView, RiddleDatesView, RiddleBriesView, WinnerView))

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^go$', dict_views[1].as_view(), name='riddle1'),
    url(r'^go2$', dict_views[2].as_view(), name='riddle2'),
    url(r'^go3$', dict_views[3].as_view(), name='riddle3'),
    url(r'^end$', dict_views[4].as_view(), name='riddle4'),
)
