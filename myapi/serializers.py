
from rest_framework import serializers
from .models import DailyWeight

class WeightEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWeight
        fields = ['id', 'date', 'weight']
        read_only_fields = ['id']