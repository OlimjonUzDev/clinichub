from rest_framework import serializers

from .models import Speciality, RankType


class SpecilatySerializers(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'

class RankTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RankType
        fields = '__all__'
