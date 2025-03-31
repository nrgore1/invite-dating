from rest_framework import serializers
from .models import ReferralRequest, ReferralCode

class ReferralRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralRequest
        fields = '__all__'
        read_only_fields = ['referrer', 'approved', 'created_at']

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = '__all__'

