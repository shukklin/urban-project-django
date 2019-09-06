from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^auth/', include('api.auth.urls'), name='auth'),
    url(r'^spinner/site-types/$', views.SiteTypesView.as_view(), name='site-types'),
    url(r'^spinner/common-names/$', views.CommonNamesView.as_view(), name='common-names'),
    url(r'^spinner/scientific-names/$', views.ScientificNamesView.as_view(), name='scientific-names'),
    url(r'^tree/(?P<pk>\d+)/users/$', views.UsersTreeView.as_view(), name='tree-users'),
    url(r'^tree/(?P<pk>\d+)/photos/$', views.TreePhotosView.as_view(), name='tree-photos'),
    url(r'^tree/(?P<pk>\d+)/record/$',
        views.TreeRecordView.as_view(), name='tree-record'),
    url(r'^trees/(?P<lat>\d+\.\d+)/(?P<lng>\d+\.\d+)/(?P<z>\d+)/$',
        views.TreesInRadiusView.as_view(),
        name='trees-in-radius'),
    url(r'^tree/$', views.TreeView.as_view(), name='tree'),
    url(r'^record/$', views.RecordsView.as_view(), name='record'),
    url(r'^users/scores/$', views.UsersScoresView.as_view(), name='users-scores'),
    url(r'^user/photos/$', views.UserPhotosView.as_view(), name='user-photos'),
    url(r'^user/trees/$', views.UserTreesView.as_view(), name='user-trees'),
    url(r'^user/score/$', views.UserScoresView.as_view(), name='user-score'),
    url(r'^user/$', views.UserView.as_view(), name='user')
]
