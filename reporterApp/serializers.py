from rest_framework import serializers
from .models import Account, Category, Impact, Location


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'


class NewAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['email','name','password']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'email', 'name','isSuperUser']


class ErrorCheckSerializer(serializers.Serializer):

    error_message = serializers.CharField()


class SuccessCodeSerializer(serializers.Serializer):

    code = serializers.CharField()


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ImpactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Impact
        fields = '__all__'



class ReportSerializer(serializers.Serializer):

    reporter_name = serializers.CharField()
    report_type = serializers.CharField()
    report_location = serializers.CharField()
    report_impact = serializers.CharField()
    incident_category = serializers.CharField()
    incident_description = serializers.CharField()
    report_deed = serializers.CharField()
    report_date = serializers.CharField()
    date = serializers.CharField()




class ReportTypeAggregateSerializer(serializers.Serializer):

    positive = serializers.CharField()
    negative = serializers.CharField()


class AggregateSerializer(serializers.Serializer):

    name = serializers.CharField()
    value = serializers.CharField()


class MyReportAggregateSerializer(serializers.Serializer):

    myReport = serializers.CharField()
    totalReport = serializers.CharField()