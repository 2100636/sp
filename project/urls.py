from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from tastypie.api import Api
from project.notifications.api import NotificationResource
v1_api = Api(api_name='v1')
v1_api.register(NotificationResource())


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^pristroy', include('project.pristroy.urls')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^notice/', include('project.notifications.urls')),
    url(r'^', include('project.core.urls')),
    url(r'^', include('project.cart.urls')),
    url(r'^', include('project.calendar_js.urls')),
    url(r'^', include('project.documentation.urls')),
    url(r'^profile/', include('project.accounts.urls')),
)


if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}
        ),

        url(
            r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
