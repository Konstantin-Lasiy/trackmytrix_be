from rest_framework import serializers
from .models import TrickDefinition, Run, TrickInstance


class TrickDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrickDefinition
        fields = "__all__"


class TrickDefinitionShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrickDefinition
        fields = ["id", "name"]


class TrickInstanceSerializer(serializers.ModelSerializer):
    trick_definition = TrickDefinitionShortSerializer(read_only=True)

    class Meta:
        model = TrickInstance
        fields = ["id", "successful", "right", "reverse", "twisted", "trick_definition"]


class RunSerializer(serializers.ModelSerializer):
    tricks = TrickInstanceSerializer(many=True)

    class Meta:
        model = Run
        fields = ["id", "user", "date", "time", "wing", "site", "tricks"]
