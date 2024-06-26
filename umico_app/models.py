from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
#ChatGPT 5/14
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.

class Address(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='shipping_addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zip_code}"
    
    def get_absolute_url(self):
        return reverse('shipping_address_detail', kwargs={'pk': self.id})

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?[0-9\- ]+$',
                message="Enter a valid phone number. It may contain digits, spaces, and optionally start with a '+'."
            )
        ],
        blank=False
    )
    timestamp = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
       return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse('customer_detail', kwargs={'pk': self.id})

class Print(models.Model):
    deadline = models.DateTimeField()
    #Timestamp necessary?
    #one customer to many prints including delete all method
    customer = models.ForeignKey(Customer, related_name='prints', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #PRINT JOB ATTRIBUTES
    image_height = models.DecimalField(max_digits=8, decimal_places=3)
    image_width = models.DecimalField(max_digits=8, decimal_places=3)
    paper_height = models.DecimalField(max_digits=8, decimal_places=3)
    paper_width = models.DecimalField(max_digits=8, decimal_places=3)
    #border or full bleed
    print_style = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    job_notes = models.TextField(default="N/A")

    is_completed = models.BooleanField(default=False)
    client_notified = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    final_location = models.CharField(max_length=50, default="N/A")
    payment_type = models.CharField(max_length=50, default="Visa")
    deposit = models.BooleanField(default=False)
    balance_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name}"

    def get_absolute_url(self):
        return reverse('print_detail', kwargs={'pk': self.id})

class Scan(models.Model):
    deadline = models.DateTimeField()
    #Timestamp necessary?
    #one customer to many scans
    customer = models.ForeignKey(Customer, related_name='scans', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #SCAN JOB ATTRIBUTES
    image_height = models.DecimalField(max_digits=8, decimal_places=3)
    image_width = models.DecimalField(max_digits=8, decimal_places=3)
    file_type = models.CharField(max_length=50)
    # 300 600 900 1200 or 1600
    dpi = models.DecimalField(max_digits=8, decimal_places=3)
   
    is_completed = models.BooleanField(default=False)
    client_notified = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    final_location = models.CharField(max_length=50, default="N/A")
    payment_type = models.CharField(max_length=50, default="Visa")
    deposit = models.BooleanField(default=False)
    balance_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name}"

    def get_absolute_url(self):
        return reverse('scan_detail', kwargs={'pk': self.id})
    
class Misc(models.Model):
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    job_notes = models.TextField(default="No notes at this time")
    is_completed = models.BooleanField(default=False)
    client_notified = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    final_location = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50, default="Visa")
    deposit = models.BooleanField(default=False)
    balance_paid = models.BooleanField(default=False)

    # one customer to many frames
    customer = models.ForeignKey(Customer, related_name='misc', on_delete=models.CASCADE)

    #functions
    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name}"

    def get_absolute_url(self):
        return reverse('misc_detail', kwargs={'pk': self.id})


class Frame(models.Model):
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    #Timestamp necessary?

    #Frame JOB ATTRIBUTES
    image_height = models.DecimalField(max_digits=8, decimal_places=3)
    image_width = models.DecimalField(max_digits=8, decimal_places=3)
    frame_height = models.DecimalField(max_digits=8, decimal_places=3)
    frame_width = models.DecimalField(max_digits=8, decimal_places=3)
    moulding = models.CharField(max_length=50)
    moulding_number = models.BigIntegerField(default=23423)
    # mat float or window
    mat = models.CharField(max_length=50)
    mat_number = models.BigIntegerField(default=23432)
    # mat 2, 4 or 8 ply
    mat_ply = models.CharField(max_length=50)
    mat_window = models.BooleanField()
    mat_double = models.BooleanField()
    mat_in_visible = models.DecimalField(max_digits=8, decimal_places=3)
    mat_in_total = models.DecimalField(max_digits=8, decimal_places=3, default=0.0)
    mat_inside_height = models.DecimalField(max_digits=8, decimal_places=3)
    mat_inside_width = models.DecimalField(max_digits=8, decimal_places=3)
    mat_outside_height = models.DecimalField(max_digits=8, decimal_places=3)
    mat_outside_width = models.DecimalField(max_digits=8, decimal_places=3)
    #float raised or flat
    float = models.BooleanField(default=False)
    float_type = models.CharField(max_length=50)
    float_in_visible = models.DecimalField(max_digits=8, decimal_places=3)
    float_in_total = models.DecimalField(max_digits=8, decimal_places=3)
    glazing = models.CharField(max_length=50)
    #upload image to storage & save url
    thumbnail = models.CharField(max_length=250, default='/static/images/placeholder.svg')
    # glazing premium clear, conservation clear uv
    glazing_type = models.CharField(max_length=50)
    spacers = models.BooleanField(default=False)
    spacers_type = models.CharField(max_length=50)
    canvas_floater = models.DecimalField(8, 2)
    canvas_floater = models.DecimalField(max_digits=8, decimal_places=3)
    straight_to_frame = models.BooleanField(default=False)
    art_location = models.CharField(max_length=50)
    art_condition = models.TextField(default="N/A")
    job_notes = models.TextField(default="No notes at this time")

    is_completed = models.BooleanField(default=False)
    client_notified = models.BooleanField(default=False)
    notification_date = models.DateTimeField(null=True, blank=True)
    final_location = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50, default="Visa")
    deposit = models.BooleanField(default=False)
    balance_paid = models.BooleanField(default=False)

    # one customer to many frames
    customer = models.ForeignKey(Customer, related_name='frames', on_delete=models.CASCADE)
   
    #functions
    def __str__(self):
        return f"{self.customer.first_name} {self.customer.last_name}"

    def get_absolute_url(self):
        return reverse('frame_detail', kwargs={'pk': self.id})