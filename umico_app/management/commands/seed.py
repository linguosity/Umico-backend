from django.core.management.base import BaseCommand
from umico_app.models import Customer, Scan, Print, Employee, Frame, Address
from datetime import datetime, timedelta
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Clear all existing data
        Customer.objects.all().delete()
        Scan.objects.all().delete()
        Print.objects.all().delete()
        Employee.objects.all().delete()
        Frame.objects.all().delete()
        Address.objects.all().delete()

        # Create some employees
        emp1 = Employee.objects.create(first_name='John', last_name='Doe', email='john.doe@example.com', phone_number='+123456789')
        emp2 = Employee.objects.create(first_name='Jane', last_name='Doe', email='jane.doe@example.com', phone_number='+987654321')

        # Create some customers
        cust1 = Customer.objects.create(first_name='Alice', last_name='Smith', email='alice.smith@example.com', phone_number='+1122334455')
        cust2 = Customer.objects.create(first_name='Bob', last_name='Brown', email='bob.brown@example.com', phone_number='+9988776655')

        # Create one shipping address for each customer
        Address.objects.create(customer=cust1, street='123 Elm St', city='Springfield', state='IL', zip_code='62701', country='USA')
        Address.objects.create(customer=cust2, street='789 Oak St', city='Springfield', state='IL', zip_code='62703', country='USA')

        # Art URLs for low-resolution images
        art_urls = [
            'https://cdn.midjourney.com/593ccd89-0308-40d2-8dca-4e7f703224d6/0_0.jpeg',
            'https://cdn.midjourney.com/8ffd06b0-78d8-4e47-8c07-6342c34c3d86/0_3.jpeg',
            'https://cdn.midjourney.com/f642f4ea-53bf-4ede-a775-1086bb7bef13/0_0.jpeg',
            # Add more URLs as needed
        ]

        def random_date():
            return timezone.make_aware(datetime(2023, 7, 1, 12, 0) + timedelta(days=random.randint(-365, 365)))

        def create_prints(customer):
            for i in range(3):
                Print.objects.create(
                    customer=customer,
                    deadline=timezone.now(),
                    image_height=random.uniform(8.0, 12.0),
                    image_width=random.uniform(8.0, 12.0),
                    paper_height=random.uniform(8.0, 12.0),
                    paper_width=random.uniform(8.0, 12.0),
                    print_style=random.choice(['Full Bleed', 'Border']),
                    quantity=random.randint(10, 200),
                    job_notes=f'Print job notes {i + 3}'
                )

        def create_scans(customer):
            for i in range(3):
                Scan.objects.create(
                    customer=customer,
                    deadline=timezone.now(),
                    image_height=random.uniform(8.0, 12.0),
                    image_width=random.uniform(8.0, 12.0),
                    file_type=random.choice(['JPEG', 'PNG']),
                    dpi=random.choice([300, 600, 1200]),
                    thumbnail=random.choice(art_urls),
                    is_completed=random.choice([True, False]),
                    client_notified=random.choice([True, False]),
                    notification_date=random_date(),
                    final_location=f'server/folder{i + 3}',
                    payment_type=random.choice(['Credit Card', 'Cash', 'Check']),
                    deposit_made=random.choice([True, False]),
                    balance_paid=random.choice([True, False])
                )

        def create_frames(customer):
            for i in range(3):
                Frame.objects.create(
                    customer=customer,
                    deadline=timezone.now(),
                    image_height=random.uniform(8.0, 12.0),
                    image_width=random.uniform(8.0, 12.0),
                    frame_height=random.uniform(10.0, 15.0),
                    frame_width=random.uniform(10.0, 15.0),
                    moulding=random.choice(['Wood', 'Metal']),
                    moulding_number=random.randint(1000, 9999),  # Add this line
                    mat_number=random.randint(1000, 9999), 
                    mat=random.choice(['Single', 'Double']),
                    mat_ply=random.choice(['4-ply', '8-ply']),
                    mat_window=random.choice([True, False]),
                    mat_double=random.choice([True, False]),
                    mat_in_visible=random.uniform(0.1, 0.5),
                    mat_inside_height=random.uniform(8.0, 10.0),
                    mat_inside_width=random.uniform(8.0, 10.0),
                    mat_outside_height=random.uniform(9.0, 11.0),
                    mat_outside_width=random.uniform(9.0, 11.0),
                    float_type=random.choice(['Raised', 'Flat']),
                    float_in_visible=random.uniform(0.1, 0.5),
                    float_in_total=random.uniform(0.3, 0.7),
                    glazing=random.choice(['Glass', 'Acrylic']),
                    thumbnail=random.choice(art_urls),
                    glazing_type=random.choice(['UV Clear', 'Non-Glare']),
                    spacers=random.choice([True, False]),
                    spacers_type=random.choice(['Plastic', 'None']),
                    canvas_floater=random.uniform(0.1, 0.3),
                    straight_to_frame=random.choice([True, False]),
                    art_location=random.choice(['Storage Room', 'Exhibition Hall']),
                    art_condition=random.choice(['Good', 'Excellent']),
                    is_completed=random.choice([True, False]),
                    client_notified=random.choice([True, False]),
                    notification_date=random_date(),
                    final_location=random.choice(['Storage Room', 'Exhibition Hall']),
                    payment_type=random.choice(['Credit Card', 'Cash', 'Check']),
                    deposit=random.choice([True, False]),
                    balance_paid=random.choice([True, False])
                )

        # Create initial print jobs
        Print.objects.create(
            customer=cust1,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            paper_height=8.5,
            paper_width=11.0,
            print_style='Full Bleed',
            quantity=100,
            job_notes='Print job 1 notes'
        )

        Print.objects.create(
            customer=cust2,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            paper_height=8.5,
            paper_width=11.0,
            print_style='Border',
            quantity=50,
            job_notes='Print job 2 notes'
        )

        # Create initial scan jobs
        Scan.objects.create(
            customer=cust1,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            file_type='JPEG',
            dpi=300,
            thumbnail='https://cdn.midjourney.com/593ccd89-0308-40d2-8dca-4e7f703224d6/0_0.jpeg',
            is_completed=False,
            client_notified=False,
            notification_date=timezone.make_aware(datetime(2023, 7, 1, 12, 0)),
            final_location='server/folder1',
            payment_type='Credit Card',
            deposit_made=True,
            balance_paid=False
        )

        Scan.objects.create(
            customer=cust2,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            file_type='PNG',
            dpi=600,
            thumbnail='http://example.com/thumb2.jpg',
            is_completed=True,
            client_notified=True,
            notification_date=timezone.make_aware(datetime(2023, 7, 1, 12, 0)),
            final_location='server/folder2',
            payment_type='Cash',
            deposit_made=True,
            balance_paid=True
        )

        # Create initial frame jobs
        Frame.objects.create(
            customer=cust1,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            frame_height=10.0,
            frame_width=12.0,
            moulding='Wood',
            moulding_number=1234, 
            mat='Single',
            mat_number=5678,
            mat_ply='4-ply',
            mat_window=True,
            mat_double=False,
            mat_in_visible=0.5,
            mat_inside_height=8.0,
            mat_inside_width=10.0,
            mat_outside_height=9.0,
            mat_outside_width=11.0,
            float_type='Raised',
            float_in_visible=0.3,
            float_in_total=0.5,
            glazing='Glass',
            thumbnail='https://cdn.midjourney.com/8ffd06b0-78d8-4e47-8c07-6342c34c3d86/0_3.jpeg',
            glazing_type='UV Clear',
            spacers=True,
            spacers_type='Plastic',
            canvas_floater=0.2,
            straight_to_frame=False,
            art_location='Storage Room',
            art_condition='Good',
            is_completed=False,
            client_notified=False,
            notification_date=timezone.make_aware(datetime(2023, 7, 1, 12, 0)),
            final_location='Storage Room',
            payment_type='Credit Card',
            deposit=True,
            balance_paid=False
        )

        Frame.objects.create(
            customer=cust2,
            deadline=timezone.now(),
            image_height=8.5,
            image_width=11.0,
            frame_height=10.0,
            frame_width=12.0,
            moulding='Metal',
            mat='Double',
            mat_ply='8-ply',
            mat_window=False,
            mat_double=True,
            mat_in_visible=0.5,
            mat_inside_height=8.0,
            mat_inside_width=10.0,
            mat_outside_height=9.0,
            mat_outside_width=11.0,
            float_type='Flat',
            float_in_visible=0.3,
            float_in_total=0.5,
            glazing='Acrylic',
            thumbnail='https://cdn.midjourney.com/f642f4ea-53bf-4ede-a775-1086bb7bef13/0_0.jpeg',
            glazing_type='Non-Glare',
            spacers=False,
            spacers_type='None',
            canvas_floater=0.2,
            straight_to_frame=True,
            art_location='Exhibition Hall',
            art_condition='Excellent',
            is_completed=True,
            client_notified=True,
            notification_date=timezone.make_aware(datetime(2023, 7, 1, 12, 0)),
            final_location='Exhibition Hall',
            payment_type='Check',
            deposit=False,
            balance_paid=True
        )

        # Create additional jobs
        for customer in [cust1, cust2]:
            create_prints(customer)
            create_scans(customer)
            create_frames(customer)

        self.stdout.write("Data seeding completed.")
