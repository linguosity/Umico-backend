from rest_framework import serializers
from .models import Customer, Scan, Print, Employee, Frame, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id','first_name', 'last_name', 'email', 'phone_number', 'shipping_addresses']

class ScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scan
        fields = '__all__'

class PrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Print
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = '__all__'
