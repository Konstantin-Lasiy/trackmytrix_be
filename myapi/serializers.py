from rest_framework import serializers
from .models import TrickDefinition, Run


class TrickDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrickDefinition
        fields = "__all__"


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"
