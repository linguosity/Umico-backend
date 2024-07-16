from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import Customer, Scan, Frame, Print, Address, Misc
from .serializers import CustomerSerializer, ScanSerializer, PrintSerializer, FrameSerializer, AddressSerializer, MiscSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
import logging
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

logger = logging.getLogger('umico_app')

# umico_app/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the index.")

# GET Viewsets

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token to logout
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)

class SearchResultsView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'shipping_addresses__city', 'shipping_addresses__state']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("Authorization header:", request.headers.get('Authorization'))
        return super().get(request, *args, **kwargs)


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
        customer_data = CustomerSerializer(customer).data
        return Response(customer_data)
    
     # CREATE CUSTOMER
    @action(detail=False, methods=['post'])
    def add_customer(self, request):
        
        # Extract and remove the addresses data from the request data
        addresses_data = request.data.pop('shipping_addresses', [])
        
        # Check if the shipping_addresses field exists in the request data
        if 'shipping_addresses' in request.data:
            print("shipping_addresses found in request data")
        else:
            print("shipping_addresses NOT found in request data")

        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(): 

            customer = serializer.save()

            for address_data in addresses_data:
                address_data.pop('id', None)
                address_data.pop('customer', None)
                address_data['customer'] = customer
                Address.objects.create(**address_data)

            print("Customer created successfully:", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.debug("Serializer errors: %s", serializer.errors)
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
    
    #VIEW MISC | customers/{id}/miscs/ #####################
    @action(detail=True, methods=['get'])
    def misc(self, request, pk=None):
        customer = self.get_object()
        misc = Misc.objects.filter(customer=customer)
        serializer = MiscSerializer(misc, many=True)
        return Response(serializer.data)

    # CREATE MISC
    @action(detail=True, methods=['post'])
    def add_misc(self, request, pk=None):
        customer = self.get_object()
        serializer = MiscSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # UPDATE MISC
    @action(detail=True, methods=['put'], url_path='update_misc/(?P<misc_id>[^/.]+)')
    def update_misc(self, request, pk=None):
        customer = self.get_object()
        misc = get_object_or_404(Misc, customer=customer, pk=request.data.get('misc_id'))
        serializer = MiscSerializer(misc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE MISC (ARCHIVE)
    @action(detail=True, methods=['delete'])
    def delete_misc(self, request, pk=None):
        customer = self.get_object()
        misc = get_object_or_404(Misc, customer=customer, pk=request.data.get('misc_id'))
        misc.delete()
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

class MiscViewSet(viewsets.ModelViewSet):
    queryset = Misc.objects.order_by('deadline')
    serializer_class = MiscSerializer
    permission_classes = [IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

