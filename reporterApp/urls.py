from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'guide'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #reporter/login
    url(r'^login/$',views.Login.as_view(), name = 'login'),

    #reporter/superuser
    url(r'^superuser/$',views.IsSuperUser.as_view(), name = 'is-superuser'),

    #reporter/location
    url(r'^location/$',views.LocationView.as_view(), name = 'location-view'),

    #reporter/category
    url(r'^category/$',views.CategoryView.as_view(), name = 'category-view'),

    #reporter/impact
    url(r'^impact/$',views.ImpactView.as_view(), name = 'impact-view'),

    #reporter/report
    url(r'^report/$',views.ReportView.as_view(), name = 'report-view'),

    #reporter/edit_location
    url(r'^edit_location/(?P<id>\w+)/$',views.EditLocation.as_view(), name = 'edit-location'),

    #reporter/delete_location
    url(r'^delete_location/(?P<id>\w+)/$',views.DeleteLocation.as_view(), name = 'delete-location'),

    #reporter/edit_category
    url(r'^edit_category/(?P<id>\w+)/$',views.EditCategory.as_view(), name = 'edit-category'),

    #reporter/delete_category
    url(r'^delete_category/(?P<id>\w+)/$',views.DeleteCategory.as_view(), name = 'delete-category'),

    #reporter/edit_impact
    url(r'^edit_impact/(?P<id>\w+)/$',views.EditImpact.as_view(), name = 'edit-impact'),

    #reporter/delete_category
    url(r'^delete_impact/(?P<id>\w+)/$',views.DeleteImpact.as_view(), name = 'delete-impact'),

    #reporter/type_aggregate
    url(r'^type_aggregate/$',views.ReportTypeAggregate.as_view(), name = 'report-type-aggregate'),

    #reporter/location_aggregate
    url(r'^location_aggregate/$',views.LocationAggregate.as_view(), name = 'location-aggregate'),

    #reporter/impact_aggregate
    url(r'^impact_aggregate/$',views.ImpactAggregate.as_view(), name = 'impact-aggregate'),

    #reporter/category_aggregate
    url(r'^category_aggregate/$',views.CategoryAggregate.as_view(), name = 'category-aggregate'),

    #reporter/user_aggregate
    url(r'^user_aggregate/$',views.UserAggregate.as_view(), name = 'user-aggregate'),

    #reporter/report_aggregate
    url(r'^report_aggregate/$',views.ReportAggregate.as_view(), name = 'report-aggregate'),

    #reporter/superuser_sort
    url(r'^superuser_sort/$',views.SuperUserSort.as_view(), name = 'superuser-sort'),

    #reporter/sort
    url(r'^sort/$',views.SortView.as_view(), name = 'sort-view'),

    #reporter/my_report_aggregate
    url(r'^my_report_aggregate/$',views.MyReportAggregate.as_view(), name = 'my-report-aggregate'),

]