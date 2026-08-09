from rest_framework import serializers

from .models import Speciality, RankType, RankPrice


class SpecialitySerializers(serializers.ModelSerializer):
    """Speciality modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        model = Speciality
        fields = '__all__'

class RankTypeSerializers(serializers.ModelSerializer):
    """RankType modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        model = RankType
        fields = '__all__'

class RankPriceSerializers(serializers.ModelSerializer):
    """RankPrice modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        model = RankPrice
        fields = '__all__'
