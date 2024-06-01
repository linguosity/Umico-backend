from rest_framework import serializers
from .models import Customer, Scan, Print, Frame, Address


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
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        return CustomerSerializer(obj.customer).data

    class Meta:
        model = Frame
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    shipping_addresses = AddressSerializer(many=True)
    scans = ScanSerializer(many=True, read_only=True)
    prints = PrintSerializer(many=True, read_only=True)
    frames = FrameSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'shipping_addresses', 'scans', 'prints', 'frames']

    def create(self, validated_data):
        addresses_data = validated_data.pop('shipping_addresses')
        print("Creating customer with addresses:", validated_data, addresses_data)  # Add this line
        customer = Customer.objects.create(**validated_data)

        # Save the Address instances to the database before calling the set() method
        address_instances = []
        for address_data in addresses_data:
            address = Address.objects.create(customer=customer, **address_data)
            address_instances.append(address)

        customer.shipping_addresses.set(address_instances)

        return customer


    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('shipping_addresses')
        
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()

        # Delete any addresses not included in the new data
        current_addresses = instance.shipping_addresses.all()
        current_address_ids = set(address.id for address in current_addresses)
        new_address_ids = set(address_data.get('id', 0) for address_data in addresses_data)
        addresses_to_delete = current_address_ids - new_address_ids
        Address.objects.filter(id__in=addresses_to_delete).delete()

        # Save the Address instances to the database before calling the set() method
        address_instances = []
        for address_data in addresses_data:
            address_id = address_data.get('id')
            if address_id:
                address = Address.objects.get(id=address_id, customer=instance)
                address.street = address_data.get('street', address.street)
                address.city = address_data.get('city', address.city)
                address.state = address_data.get('state', address.state)
                address.zip_code = address_data.get('zip_code', address.zip_code)
                address.country = address_data.get('country', address.country)
                address.save()
                address_instances.append(address)
            else:
                address = Address.objects.create(customer=instance, **address_data)
                address_instances.append(address)

        # Set the shipping_addresses field of the instance instance
        instance.shipping_addresses.set(address_instances)

        return instance