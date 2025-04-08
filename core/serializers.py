from rest_framework import serializers
from .models import ReferralRequest, ReferrerCode

class ReferralRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralRequest
        fields = '__all__'
        read_only_fields = ['referrer', 'approved', 'created_at']

class ReferrerCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferrerCode
        fields = '__all__'

