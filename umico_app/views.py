from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Scan, Frame, Print, Address
from .serializers import CustomerSerializer, ScanSerializer, PrintSerializer, FrameSerializer, AddressSerializer


# Get requests

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def scans(self, request, pk=None):
        customer = self.get_object()
        scans = Scan.objects.filter(customer=customer)
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def frames(self, request, pk=None):
        customer = self.get_object()
        frames = Frame.objects.filter(customer=customer)
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def prints(self, request, pk=None):
        customer = self.get_object()
        prints = Print.objects.filter(customer=customer)
        serializer = PrintSerializer(prints, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def address(self, request, pk=None):
        customer = self.get_object()
        address = Address.objects.filter(customer=customer)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    @action(detail=True, methods=['get'])
    def frames(self, request, pk=None):
        customer = self.get_object()
        frames = Frame.objects.filter(customer=customer)
        serializer = ScanSerializer(frames, many=True)
        return Response(serializer.data)

class PrintViewSet(viewsets.ModelViewSet):
    queryset = Print.objects.all()
    serializer_class = PrintSerializer

class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

