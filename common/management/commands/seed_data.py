from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from about.models import AboutContent
from admin_profiles.models import AdminProfile
from blog_categories.models import BlogCategory
from blog.models import BlogPost
from bookings.models import ConsultationBooking
from business.models import BusinessContact
from contact.models import ContactSubmission
from home.models import HomeContent
from roles.models import Role, UserRole
from services.models import ServicesContent
from datetime import date


class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Roles - 2 default roles only
        super_admin, _ = Role.objects.get_or_create(
            name='super_admin',
            defaults={
                'description': 'Full system access and control',
                'permissions': ['create', 'read', 'update', 'delete', 'manage_users', 'manage_roles']
            }
        )
        admin, _ = Role.objects.get_or_create(
            name='admin',
            defaults={
                'description': 'Administrative access with content management',
                'permissions': ['create', 'read', 'update', 'delete']
            }
        )
        # Remove any other roles (editor, etc.) to keep only 2 default roles
        Role.objects.exclude(name__in=['super_admin', 'admin']).delete()
        self.stdout.write(self.style.SUCCESS('✓ Roles: 2 records'))

        # About Content - 2 records
        AboutContent.objects.get_or_create(
            content_type='hero',
            item_index=0,
            defaults={
                'heading': 'About K&T Financial',
                'subtitle': 'Your trusted financial partner',
                'text': 'We provide expert financial services tailored to your needs.',
            }
        )
        AboutContent.objects.get_or_create(
            content_type='team_member',
            item_index=1,
            defaults={
                'name': 'John Smith',
                'role': 'CEO',
                'bio': 'Experienced financial advisor with 20+ years in the industry.',
                'image': 'https://example.com/john.jpg',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ AboutContent: 2 records'))

        # Admin Profiles - 2 records
        user1, _ = User.objects.get_or_create(
            username='admin1',
            defaults={'email': 'admin1@kt.com', 'is_staff': True}
        )
        user2, _ = User.objects.get_or_create(
            username='admin2',
            defaults={'email': 'admin2@kt.com', 'is_staff': True}
        )
        AdminProfile.objects.get_or_create(
            user=user1,
            defaults={
                'email': 'admin1@kt.com',
                'name': 'Admin One',
                'role': 'Super Admin',
                'bio': 'System administrator',
            }
        )
        AdminProfile.objects.get_or_create(
            user=user2,
            defaults={
                'email': 'admin2@kt.com',
                'name': 'Admin Two',
                'role': 'Content Manager',
                'bio': 'Manages content and blog posts',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ AdminProfile: 2 records'))

        # User Roles - assign roles to users
        UserRole.objects.get_or_create(
            user=user1,
            defaults={'role': super_admin}
        )
        UserRole.objects.get_or_create(
            user=user2,
            defaults={'role': admin}
        )
        self.stdout.write(self.style.SUCCESS('✓ UserRoles: 2 records'))

        # Blog Categories - 2 records
        cat1, _ = BlogCategory.objects.get_or_create(
            name='Finance',
            defaults={'description': 'Financial tips and advice'}
        )
        cat2, _ = BlogCategory.objects.get_or_create(
            name='Investment',
            defaults={'description': 'Investment strategies'}
        )
        self.stdout.write(self.style.SUCCESS('✓ BlogCategory: 2 records'))

        # Blog Posts - 2 records
        BlogPost.objects.get_or_create(
            title='Getting Started with Investing',
            defaults={
                'excerpt': 'Learn the basics of investing for beginners.',
                'body': 'Investing can seem daunting, but with the right approach...',
                'category': cat1,
                'published': True,
                'image': 'https://example.com/investing.jpg',
            }
        )
        BlogPost.objects.get_or_create(
            title='Retirement Planning Essentials',
            defaults={
                'excerpt': 'Plan your retirement with these key strategies.',
                'body': 'Retirement planning is crucial for financial security...',
                'category': cat2,
                'published': True,
                'featured': True,
                'image': 'https://example.com/retirement.jpg',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ BlogPost: 2 records'))

        # Bookings - 2 records
        ConsultationBooking.objects.get_or_create(
            email='client1@example.com',
            preferred_date=date(2025, 6, 15),
            defaults={
                'name': 'Jane Doe',
                'phone': '555-0101',
                'service': 'Financial Planning',
                'message': 'Need help with retirement planning',
            }
        )
        ConsultationBooking.objects.get_or_create(
            email='client2@example.com',
            preferred_date=date(2025, 6, 20),
            defaults={
                'name': 'Bob Wilson',
                'phone': '555-0102',
                'service': 'Tax Consultation',
                'message': 'Tax optimization for small business',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ ConsultationBooking: 2 records'))

        # Business Contact - 2 records
        BusinessContact.objects.get_or_create(
            item_index=0,
            defaults={
                'title': 'Main Office',
                'address': '123 Financial District, New York, NY 10001',
                'phone': '555-1000',
                'email': 'contact@ktfinancial.com',
                'office_hours': {'mon-fri': '9AM-6PM', 'sat': '10AM-2PM'},
            }
        )
        BusinessContact.objects.get_or_create(
            item_index=1,
            defaults={
                'title': 'Branch Office',
                'address': '456 Commerce Ave, Brooklyn, NY 11201',
                'phone': '555-2000',
                'email': 'brooklyn@ktfinancial.com',
                'office_hours': {'mon-fri': '8AM-5PM'},
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ BusinessContact: 2 records'))

        # Contact Submissions - 2 records
        ContactSubmission.objects.get_or_create(
            email='inquiry1@example.com',
            subject='General Inquiry',
            defaults={
                'name': 'Alice Johnson',
                'phone': '555-3001',
                'message': 'Interested in your financial services',
            }
        )
        ContactSubmission.objects.get_or_create(
            email='inquiry2@example.com',
            subject='Partnership',
            defaults={
                'name': 'Charlie Brown',
                'phone': '555-3002',
                'message': 'Would like to discuss partnership opportunities',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ ContactSubmission: 2 records'))

        # Home Content - 2 records
        HomeContent.objects.get_or_create(
            content_type='hero',
            item_index=0,
            defaults={
                'title': 'Welcome to K&T Financial',
                'heading': 'Secure Your Financial Future',
                'subtitle': 'Expert guidance for all your financial needs',
                'description': 'We help individuals and businesses achieve their financial goals.',
            }
        )
        HomeContent.objects.get_or_create(
            content_type='stat',
            item_index=1,
            defaults={
                'label': 'Happy Clients',
                'value': '10,000+',
                'text': 'Satisfied customers served',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ HomeContent: 2 records'))

        # Services Content - 2 records
        ServicesContent.objects.get_or_create(
            service_id='financial-planning',
            defaults={
                'title': 'Financial Planning',
                'description': 'Comprehensive financial planning services for individuals and families.',
                'tagline': 'Plan for tomorrow, today',
                'features': ['Retirement Planning', 'Investment Strategy', 'Risk Assessment'],
                'image': 'https://example.com/financial.jpg',
            }
        )
        ServicesContent.objects.get_or_create(
            service_id='tax-services',
            defaults={
                'title': 'Tax Services',
                'description': 'Expert tax preparation and optimization services.',
                'tagline': 'Maximize your returns',
                'features': ['Tax Preparation', 'Audit Support', 'Tax Strategy'],
                'image': 'https://example.com/tax.jpg',
            }
        )
        self.stdout.write(self.style.SUCCESS('✓ ServicesContent: 2 records'))

        self.stdout.write(self.style.SUCCESS('\n✅ Seed completed successfully!'))
