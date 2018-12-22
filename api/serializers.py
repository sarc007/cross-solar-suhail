import decimal
import pytz
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datetime import *


from .models import Panel, OneHourElectricity


class PanelSerializer(serializers.ModelSerializer):

    def validate_longitude(self, value):
        """validate longitude"""
        if value > 180 or value < -180:
            raise serializers.ValidationError("Ensure the value of longitude is between +180 and -180")
        d = decimal.Decimal(value)
        if d.as_tuple().exponent < -6:
            raise serializers.ValidationError("Ensure the value has not more than 6 decimal places")

        return value

    def validate_latitude(self, value):
        """validate latitude"""
        if value > 90 or value < -90:
            raise serializers.ValidationError("Ensure the value of latitude is between +90 and -90")
        d = decimal.Decimal(value)
        if d.as_tuple().exponent < -6:
            raise serializers.ValidationError("Ensure the value has not more than 6 decimal places")

        return value

    def validate_serial(self, value):
        """
            validate serial
        """
        if len(value) != 16:
            raise serializers.ValidationError("Ensure the value of serial is exactly 16 digits")
        return value

    class Meta:
        model = Panel
        fields = ('id', 'brand', 'serial', 'latitude', 'longitude')

        validators = [
            UniqueTogetherValidator(
                queryset=Panel.objects.all(),
                fields=('brand', 'serial')
            )]


class OneHourElectricitySerializer(serializers.ModelSerializer):
    kilo_watt = OneHourElectricity.kilo_watt
    date_time = OneHourElectricity.date_time

    def validate_kilo_watt(self, value):
        if value < 0:
            raise serializers.ValidationError('Ensure value of kilo watt(s) is more than or equal to zero')
        return value

    def validate_date_time(self, value):
        try:
            now_datetime = pytz.utc.localize(datetime.utcnow())
            if value > now_datetime:
                raise serializers.ValidationError("Date Time Cannot Be Greater Current Date And Time")
        except Exception as e:
            raise serializers.ValidationError("Valid date time \n exception details "+str(e))
        value_timetuple = value.timetuple()
        if value_timetuple.tm_min > 0 or value_timetuple.tm_sec > 0:
            raise serializers.ValidationError('Ensure value of date time is hourly '
                                              'i.e. 0 in minutes and 0 seconds value '
                                              'e.g '+value.strftime("%Y-%m-%dT%H:00:00Z")+' is valid value and'
                                              ' '+value.strftime("%Y-%m-%dT%H:%M:%SZ")+' is an invalid value')
        return value

    class Meta:
        panel = serializers.PrimaryKeyRelatedField(queryset=Panel.objects.all)
        model = OneHourElectricity
        fields = ('id', 'panel', 'kilo_watt', 'date_time')
        validators = [
            UniqueTogetherValidator(
                queryset=OneHourElectricity.objects.all(),
                fields=('panel', 'date_time')
            )]
