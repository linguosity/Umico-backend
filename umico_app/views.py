from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import Customer, Scan, Frame, Print, Address
from .serializers import CustomerSerializer, ScanSerializer, PrintSerializer, FrameSerializer, AddressSerializer
from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger('umico_app')

# umico_app/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

# GET Viewsets
class GetCSRFToken(APIView):
    permission_classes = (IsAuthenticated,)

    @ensure_csrf_cookie
    def get(self, request, *args, **kwargs):
        return Response({"message": "CSRF cookie set"})
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        customer=self.get_object()
        scans = Scan.objects.filter(customer=customer)
        frames = Frame.objects.filter(customer=customer)
        prints = Print.objects.filter(customer=customer)

        customer_data = CustomerSerializer(customer).data
        customer_data['scans'] = ScanSerializer(scans, many=True).data
        customer_data['frames'] = FrameSerializer(frames, many=True).data
        customer_data['prints'] = PrintSerializer(prints, many=True).data

        return Response(customer_data)
    
     # CREATE CUSTOMER
    @action(detail=False, methods=['post'])
    def add_customer(self, request):
        logger.debug("63 Received request data: %s", request.data) 
        print("Received request data:", request.data)  # Log the received request data
        
        # Extract and remove the addresses data from the request data
        addresses_data = request.data.pop('shipping_addresses', [])
        logger.debug("68 Extracted addresses data: %s", addresses_data)
        
        # Check if the shipping_addresses field exists in the request data
        if 'shipping_addresses' in request.data:
            print("shipping_addresses found in request data")
        else:
            print("shipping_addresses NOT found in request data")

        serializer = CustomerSerializer(data=request.data)
        logger.debug("serializer 70: ", serializer)
        if serializer.is_valid(): 
            logger.debug("Serializer valid, saving data...") 
            print("Serializer valid, saving data...")

            customer = serializer.save()

            for address_data in addresses_data:
                logger.debug("addressdata before setting customer 1st", address_data)
                address_data.pop('customer', None)
                address_data['customer'] = customer
                logger.debug("addressdata before setting customer 2nd time", address_data)
                Address.objects.create(**address_data)
                logger.debug("Created address: %s", address_data)  # Log each created address
            
            logger.debug("Customer created successfully: %s", serializer.data) 
            print("Customer created successfully:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("Serializer errors: %s", serializer.errors)
            print("Validation errors:", serializer.errors)
            logger.error("Validation errors: %s", serializer.errors)
            logger.debug("Request data for debugging: %s", request.data)
            logger.debug("Extracted addresses data for debugging: %s", addresses_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    @action(detail=True, methods=['delete'])
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
    @action(detail=True, methods=['put'])
    def update_frame(self, request, pk=None):
        customer = self.get_object()
        frame = get_object_or_404(Frame, customer=customer, pk=request.data.get('frame_id'))
        serializer = FrameSerializer(frame, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE FRAME 
    @action(detail=True, methods=['delete'])
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
    @action(detail=True, methods=['delete'])
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
    permission_classes = [IsAuthenticated]


class PrintViewSet(viewsets.ModelViewSet):
    queryset = Print.objects.order_by('deadline')
    serializer_class = PrintSerializer
    permission_classes = [IsAuthenticated]


class FrameViewSet(viewsets.ModelViewSet):
    queryset = Frame.objects.order_by('deadline')
    serializer_class = FrameSerializer
    permission_classes = [IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

