from rest_framework import serializers
from .models import Customer, Scan, Print, Employee, Frame, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ScanSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        return CustomerSerializer(obj.customer).data
    
    class Meta:
        model = Scan
        fields = '__all__'

class PrintSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        return CustomerSerializer(obj.customer).data
    
    class Meta:
        model = Print
        fields = '__all__'

class FrameSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Frame
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = AddressSerializer(many=True, read_only=True)
    scans = ScanSerializer(many=True, read_only=True)
    prints = PrintSerializer(many=True, read_only=True)
    frames = FrameSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id','first_name', 'last_name', 'email', 'phone_number', 'shipping_addresses', 'scans', 'prints', 'frames']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
