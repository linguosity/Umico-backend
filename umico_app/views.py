from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import Customer, Scan, Frame, Print, Address
from .serializers import CustomerSerializer, ScanSerializer, PrintSerializer, FrameSerializer, AddressSerializer

# GET Viewsets

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    #VIEW SCANS | customers/{id}/scans/ #####################
    @action(detail=True, methods=['get'])
    def scans(self, request, pk=None):
        customer = self.get_object()
        scans = Scan.objects.filter(customer=customer)
        serializer = ScanSerializer(scans, many=True)
        return Response(serializer.data)
    
    #CREATE SCAN
    @action(detail=True, methods=['post'])
    def add_scan(self, request, pk=None):
        customer = self.get_object()
        serializer = ScanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #UPDATE SCAN
    @action(detail=True, methods=['put'], url_path='update_scan/(?P<scan_id>[^/.]+)')
    def update_scan(self, request, pk=None):
        customer = self.get_object()
        scan = get_object_or_404(Scan, customer=customer, pk=request.data.get('scan_id'))
        serializer = ScanSerializer(scan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #DELETE SCAN (ARCHIVE)
    @action(detail=True, methods=['delete'], url_path='delete_scan/(?P<scan_id>[^/.]+)')
    def delete_scan(self, request, pk=None):
        customer = self.get_object()
        scan = get_object_or_404(Scan, customer=customer, pk=request.data.get('scan_id'))
        scan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    #VIEW FRAMES | customers/{id}/frames/ #####################
    @action(detail=True, methods=['get'])
    def frames(self, request, pk=None):
        customer = self.get_object()
        frames = Frame.objects.filter(customer=customer)
        serializer = FrameSerializer(frames, many=True)
        return Response(serializer.data)
    
     # CREATE FRAME
    @action(detail=True, methods=['post'])
    def add_frame(self, request, pk=None):
        customer = self.get_object()
        serializer = FrameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE FRAME
    def update_frame(self, request, pk=None):
        customer = self.get_object()
        frame = get_object_or_404(Frame, customer=customer, pk=request.data.get('frame_id'))
        serializer = FrameSerializer(frame, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE FRAME (ARCHIVE)
    @action(detail=True, methods=['delete'], url_path='delete_frame/(?P<frame_id>[^/.]+)')
    def delete_frame(self, request, pk=None):
        customer = self.get_object()
        frame = get_object_or_404(Frame, customer=customer, pk=request.data.get('frame_id'))
        frame.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    #VIEW PRINTS | customers/{id}/prints/ #####################
    @action(detail=True, methods=['get'])
    def prints(self, request, pk=None):
        customer = self.get_object()
        prints = Print.objects.filter(customer=customer)
        serializer = PrintSerializer(prints, many=True)
        return Response(serializer.data)
        
     # CREATE PRINT
    @action(detail=True, methods=['post'])
    def add_print(self, request, pk=None):
        customer = self.get_object()
        serializer = PrintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE PRINT
    @action(detail=True, methods=['put'], url_path='update_print/(?P<print_id>[^/.]+)')
    def update_print(self, request, pk=None):
        customer = self.get_object()
        print_obj = get_object_or_404(Print, customer=customer, pk=request.data.get('print_id'))
        serializer = PrintSerializer(print_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE PRINT (ARCHIVE)
    @action(detail=True, methods=['delete'], url_path='delete_print/(?P<print_id>[^/.]+)')
    def delete_print(self, request, pk=None):
        customer = self.get_object()
        print_obj = get_object_or_404(Print, customer=customer, pk=request.data.get('print_id'))
        print_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #VIEW ADDRESS | customers/{id}/address/ endpoint
    @action(detail=True, methods=['get'])
    def address(self, request, pk=None):
        customer = self.get_object()
        address = Address.objects.filter(customer=customer)
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data)

class ScanViewSet(viewsets.ModelViewSet):
    queryset = Scan.objects.order_by('deadline')
    serializer_class = ScanSerializer

class PrintViewSet(viewsets.ModelViewSet):
    queryset = Print.objects.order_by('deadline')
    serializer_class = PrintSerializer

class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.order_by('deadline')
    serializer_class = FrameSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

