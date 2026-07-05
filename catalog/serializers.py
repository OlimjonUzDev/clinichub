from rest_framework import serializers

from .models import Speciality, RankType, RankPrice


class SpecialitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'

class RankTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RankType
        fields = '__all__'

class RankPriceSerializers(serializers.ModelSerializer):
    class Meta:
        model = RankPrice
        fields = '__all__'
