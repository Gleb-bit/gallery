from django.urls import path, include
from rest_framework.routers import DefaultRouter

from gallery.views import DeleteAllPicturesAPIView, PictureModelViewSet

router = DefaultRouter()

router.register('pictures', PictureModelViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('destroy_all_rictures/', DeleteAllPicturesAPIView.as_view(), name='destroy_all_rictures')
]
