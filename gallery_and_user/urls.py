from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from accounts.endpoints import auth_urlpatterns
from accounts.endpoints import urlpatterns as account_urlpatterns
from gallery_and_user import settings

urlpatterns = [
    path('api/', include([
        path('accounts/', include(account_urlpatterns)),
        path('auth/', include(auth_urlpatterns)),

        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

        path('', include('gallery.endpoints')),

    ])),

    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()  # type: ignore
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

