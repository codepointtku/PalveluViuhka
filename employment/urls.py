from django.conf.urls import url
from django.contrib import admin
from services import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from djproxy.views import HttpProxy
from djproxy.urls import generate_routes
from django.conf import settings

router = DefaultRouter()
router.register(r'services', views.ServiceViewSet, 'services')

elasticsearch_settings = getattr(settings, "ELASTICSEARCH", "")
elasticsearch_url = elasticsearch_settings['base_url']

configuration = {
    'search': {
        'base_url': elasticsearch_url,
        'prefix': 'services/_search'
    }
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.get_search, name='search'),
    url(r'^employmentservices-test/v1/', include(router.urls)),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^feedback_form/', views.feedback_form, name='feedback_form'),
    url(r'^info/', views.info, name='info'),
    url(r'^provider_info/', views.provider_info, name='provider_info'),
    url(r'^form/', views.ServiceForm.as_view(), name='form_new'),
    url(r'^edit/(?P<pk>\d+)$', views.ServiceEditForm.as_view(), name='form_edit'),
    url(r'^post_edit_thank_you/', views.post_edit_thank_you, name='form_post_edit_thank_you'),
    url(r'^list/', views.ServiceList.as_view(), name="service_list"),
    url(r'^details/(?P<pk>\d+)$', views.ServiceDetail.as_view(), name="service_detail"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]

#if not getattr(settings, "FORCE_SCRIPT_NAME", ""):
#    urlpatterns.insert(0, url(r'^admin/', admin.site.urls))

urlpatterns += generate_routes(configuration)

handler404 = views.page_not_found

admin.site.site_header = 'Työllisyyspalvelurekisterin ylläpito'
