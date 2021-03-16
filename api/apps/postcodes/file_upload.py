from rest_framework.viewsets import ModelViewSet

from apps.postcodes.serializers import FileUploaderSerializer
from apps.postcodes.models import FileUploader


class FileUploaderAPIView(ModelViewSet):
    model = FileUploader
    serializer_class = FileUploaderSerializer
    queryset = model.objects.none()
    http_method_names = ['post']

    def get_queryset(self):
        return self.queryset

    def perform_create(self, serializer):
        serializer.save()
