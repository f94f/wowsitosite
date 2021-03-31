from rest_framework import serializers
from mountsHunt.models import Mount

class MountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mount
        fields = ['name', 'expansion', 'notes_1', 'notes_2', 'requirements', 'source', 'url_img']


