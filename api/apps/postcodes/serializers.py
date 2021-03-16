from rest_framework import serializers

from apps.postcodes.models import FileUploader, Code


class FileUploaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUploader
        fields = '__all__'

    def create(self, validated_data):
        files = FileUploader.objects.create(**validated_data)
        return files


class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = '__all__'
