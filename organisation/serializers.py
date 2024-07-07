from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Organisation


User = get_user_model()


# organisaiton serializer
class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'
        