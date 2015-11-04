from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', 'app_admin.views.admin_index', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^pythonix_admin/', include('app_admin.urls', app_name='pythonix_admin', namespace='pythonix_admin')),
    url(r'^pythonix_client/', include('app_client.urls', app_name='pythonix_client', namespace='pythonix_client')),
]
