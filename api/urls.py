from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from api import views
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()
router.register('panel', views.PanelViewSet)

urlpatterns = [

    url(r'^panel/(?P<panelid>\d+)/analytics/$', views.HourAnalyticsView.as_view()),
    url(r'^panel/(?P<panelid>\d+)/analytics/day/$', views.DayAnalyticsView.as_view()),
    path(r'docs/', include_docs_urls(title="Solar Panel Analytics API for One Hour Electricity Generation",
                                     description=""" The project accepts data for registered panels only, 
                                     and to register a panel, a serial number along with latitude and longitude is required. 
                                     The serial number must exact be 16 characters in length (for ex. AAAA1111BBBB2222); 
                                     latitude and longitude should contain 6 decimal places 
                                     and must have valid values within latitude range (-90 to 90) 
                                     and longitude range (-180 to 180) respectively.""", public=True)),
]

urlpatterns += router.urls
