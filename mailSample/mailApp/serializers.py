from rest_framework import serializers
from .models import Mail, Feedback

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
