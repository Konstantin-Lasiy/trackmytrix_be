from rest_framework import serializers
from .models import TrickDefinition, Run, TrickInstance, LastUsedTricks
from datetime import datetime


class LastUsedTricksSerializer(serializers.ModelSerializer):
    class Meta:
        model = LastUsedTricks
        fields = "__all__"


class TrickDefinitionSerializer(serializers.ModelSerializer):
    last_used = serializers.SerializerMethodField()

    class Meta:
        model = TrickDefinition
        fields = "__all__"  # Include all fields from the TrickDefinition model, plus the 'last_used'

    def get_last_used(self, obj):
        # Get the request user from the serializer context
        user = self.context['request'].user
        if not user.is_authenticated:
            return 'Never'  # Return 'Never' if the user is not authenticated

        # Try to fetch the last used date for this trick for the current user
        last_used_trick = LastUsedTricks.objects.filter(trick=obj, user=user).order_by('-last_used').first()
        if last_used_trick:
            return last_used_trick.last_used.strftime('%Y-%m-%d %H:%M:%S')
        return datetime(1900, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
    

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
