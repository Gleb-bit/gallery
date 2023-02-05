from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from gallery.models import Picture
from gallery.serializers import PictureSerializer


class PictureModelViewSet(ModelViewSet):
    queryset = Picture.objects.select_related('user')
    serializer_class = PictureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Picture.objects.filter(user=self.request.user).select_related('user')


class DeleteAllPicturesAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        Picture.objects.all().delete()
        return Response(status=204)
