from django.db import models
from django.urls import reverse
#ChatGPT 5/14
from django.core.validators import EmailValidator, RegexValidator


# Create your models here.

class Employee(models.Model):
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('employee_detail', kwargs={'pk': self.id})

class Customer(models.Model):
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
        return self.name

    def get_absolute_url(self):
        return reverse('customer_detail', kwargs={'pk': self.id})

class Print(models.Model):
    deadline = models.DateTimeField()
    #Timestamp necessary?
    #one customer to many prints including delete all method
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #PRINT JOB ATTRIBUTES
    image_height = models.DecimalField(4,2)
    image_width = models.DecimalField(4,2)
    paper_height = models.DecimalField(4,2)
    paper_width = models.DecimalField(4,2)
    #border or full bleed
    print_style = models.CharField(max_length=50)
    quantity = models.IntegerField()
    job_notes = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('print_detail', kwargs={'pk': self.id})

class Scan(models.Model):
    deadline = models.DateTimeField()
    #Timestamp necessary?
    #one customer to many scans
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #SCAN JOB ATTRIBUTES
    image_height = models.DecimalField(4, 2)
    image_width = models.DecimalField(4, 2)
    file_type = models.CharField(max_length=50)
    # 300 600 900 1200 or 1600
    dpi = models.DecimalField(4, 2)
    thumbnail = models.CharField(max_length=250)
    is_completed = models.BooleanField()
    client_notified = models.BooleanField()
    notification_date = models.DateTimeField()
    final_location = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    deposit_made = models.BooleanField()
    balance_paid = models.BooleanField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scan_detail', kwargs={'pk': self.id})

class Frame(models.Model):
    deadline = models.DateTimeField()
    #Timestamp necessary?

    #Frame JOB ATTRIBUTES
    image_height = models.DecimalField(4, 2)
    image_width = models.DecimalField(4, 2)

    frame_height = models.DecimalField(4, 2)
    frame_width = models.DecimalField(4, 2)
    moulding = models.CharField(max_length=50)
    moulding = models.IntegerField()
    mat = models.CharField(max_length=50)
    # 4 ply or 8 ply
    mat_ply = models.CharField(max_length=50)
    mat_window = models.BooleanField()
    mat_double = models.BooleanField()
    mat_in_visible = models.DecimalField(4, 2)
    mat_inside_height = models.DecimalField(4, 2)
    mat_inside_width = models.DecimalField(4, 2)
    mat_outside_height = models.DecimalField(4, 2)
    mat_outside_width = models.DecimalField(4, 2)
    # raised or flat
    float_type = models.CharField(max_length=50)
    float_in_visible = models.DecimalField(4, 2)
    float_in_total = models.DecimalField(4, 2)
    glazing = models.CharField(max_length=50)
    # premium clear, conservation clear uv
    glazing_type = models.CharField(max_length=50)
    spacers = models.BooleanField()
    spacers_type = models.CharField(max_length=50)
    canvas_floater = models.DecimalField(4, 2)
    straigt_to_frame = models.BooleanField()
    art_location = models.CharField(max_length=50)
    art_condition = models.TextField()
    is_completed = models.BooleanField()
    client_notified = models.BooleanField()
    notification_date = models.DateTimeField()
    final_location = models.CharField(max_length=50)
    payment_type = models.CharField(max_length=50)
    deposit = models.BooleanField()
    balance_paid = models.BooleanField()


    # one customer to many frames
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #functions

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('frame_detail', kwargs={'pk': self.id})