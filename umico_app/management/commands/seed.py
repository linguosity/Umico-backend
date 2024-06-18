from django.core.management.base import BaseCommand
from umico_app.models import Customer, Scan, Print, Frame, Address, Misc
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Clear all existing data
        self.stdout.write("Deleting old data...")
        Address.objects.all().delete()
        Print.objects.all().delete()
        Scan.objects.all().delete()
        Misc.objects.all().delete()
        Frame.objects.all().delete()
        Customer.objects.all().delete()

        # Verify deletion
        self.stdout.write("Verifying deletion...")
        assert Customer.objects.count() == 0
        assert Address.objects.count() == 0
        assert Print.objects.count() == 0
        assert Scan.objects.count() == 0
        assert Misc.objects.count() == 0
        assert Frame.objects.count() == 0

        # Create some customers
        self.stdout.write("Creating new customers...")
        cust1 = Customer.objects.create(first_name='Alice', last_name='Smith', email='alice.smith@example.com', phone_number='+1122334455')
        cust2 = Customer.objects.create(first_name='Bob', last_name='Brown', email='bob.brown@example.com', phone_number='+9988776655')
        cust3 = Customer.objects.create(first_name='Charlie', last_name='Davis', email='charlie.davis@example.com', phone_number='+5566778899')
        cust4 = Customer.objects.create(first_name='Diana', last_name='Evans', email='diana.evans@example.com', phone_number='+4433221100')
        cust5 = Customer.objects.create(first_name='Eve', last_name='White', email='eve.white@example.com', phone_number='+6677889900')

        # Create shipping addresses for each customer
        self.stdout.write("Creating addresses...")
        Address.objects.create(customer=cust1, street='123 Elm St', city='Springfield', state='IL', zip_code='62701', country='USA')
        Address.objects.create(customer=cust2, street='789 Oak St', city='Springfield', state='IL', zip_code='62703', country='USA')
        Address.objects.create(customer=cust3, street='456 Pine St', city='Springfield', state='IL', zip_code='62704', country='USA')
        Address.objects.create(customer=cust4, street='321 Maple St', city='Springfield', state='IL', zip_code='62705', country='USA')
        Address.objects.create(customer=cust5, street='654 Cedar St', city='Springfield', state='IL', zip_code='62706', country='USA')

        # Create initial print jobs
        self.stdout.write("Creating print jobs...")
        Print.objects.create(
            customer=cust1,
            deadline=timezone.now() + timedelta(days=10),
            image_height=8.5,
            image_width=11.0,
            paper_height=8.5,
            paper_width=11.0,
            print_style='Full Bleed',
            quantity=100,
            job_notes='Print job for Alice'
        )

        Print.objects.create(
            customer=cust2,
            deadline=timezone.now() + timedelta(days=5),
            image_height=8.5,
            image_width=11.0,
            paper_height=8.5,
            paper_width=11.0,
            print_style='Border',
            quantity=50,
            job_notes='Print job for Bob'
        )

        Print.objects.create(
            customer=cust3,
            deadline=timezone.now() + timedelta(days=15),
            image_height=10.0,
            image_width=12.0,
            paper_height=10.0,
            paper_width=12.0,
            print_style='Full Bleed',
            quantity=150,
            job_notes='Print job for Charlie'
        )

        # Create initial scan jobs
        self.stdout.write("Creating scan jobs...")
        Scan.objects.create(
            customer=cust1,
            deadline=timezone.now() + timedelta(days=7),
            image_height=8.5,
            image_width=11.0,
            file_type='JPEG',
            dpi=300,
            is_completed=False,
            client_notified=False,
            notification_date=None,
            final_location='server/folder1',
            payment_type='Credit Card',
            deposit=True,
            balance_paid=False
        )

        Scan.objects.create(
            customer=cust4,
            deadline=timezone.now() + timedelta(days=12),
            image_height=9.0,
            image_width=12.0,
            file_type='PNG',
            dpi=600,
            is_completed=True,
            client_notified=True,
            notification_date=timezone.now(),
            final_location='server/folder2',
            payment_type='Cash',
            deposit=False,
            balance_paid=True
        )

        # Create initial misc jobs
        self.stdout.write("Creating misc jobs...")
        Misc.objects.create(
            customer=cust1,
            deadline=timezone.now() + timedelta(days=20),
            is_completed=False,
            client_notified=False,
            notification_date=None,
            final_location='Storage Room',
            payment_type='Credit Card',
            deposit=True,
            balance_paid=False,
            job_notes='Misc job for Alice'
        )

        Misc.objects.create(
            customer=cust5,
            deadline=timezone.now() + timedelta(days=8),
            is_completed=True,
            client_notified=True,
            notification_date=timezone.now(),
            final_location='Exhibition Hall',
            payment_type='Check',
            deposit=False,
            balance_paid=True,
            job_notes='Misc job for Eve'
        )

        # Create initial frame jobs
        self.stdout.write("Creating frame jobs...")
        Frame.objects.create(
            customer=cust2,
            deadline=timezone.now() + timedelta(days=15),
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
            notification_date=None,
            final_location='Storage Room',
            payment_type='Credit Card',
            deposit=True,
            balance_paid=False
        )

        Frame.objects.create(
            customer=cust3,
            deadline=timezone.now() + timedelta(days=30),
            image_height=9.0,
            image_width=12.0,
            frame_height=11.0,
            frame_width=13.0,
            moulding='Metal',
            moulding_number=4321,
            mat='Double',
            mat_number=8765,
            mat_ply='8-ply',
            mat_window=False,
            mat_double=True,
            mat_in_visible=0.4,
            mat_inside_height=8.5,
            mat_inside_width=11.5,
            mat_outside_height=9.5,
            mat_outside_width=12.5,
            float_type='Flat',
            float_in_visible=0.2,
            float_in_total=0.4,
            glazing='Acrylic',
            thumbnail='https://cdn.midjourney.com/f642f4ea-53bf-4ede-a775-1086bb7bef13/0_0.jpeg',
            glazing_type='Non-Glare',
            spacers=False,
            spacers_type='None',
            canvas_floater=0.3,
            straight_to_frame=True,
            art_location='Exhibition Hall',
            art_condition='Excellent',
            is_completed=True,
            client_notified=True,
            notification_date=timezone.now(),
            final_location='Exhibition Hall',
            payment_type='Check',
            deposit=False,
            balance_paid=True
        )

        self.stdout.write("Data seeding completed.")
