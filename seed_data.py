import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medica.settings')
django.setup()

from medica911.models import Speciality, User, Doctor

def seed():
    # 1. Create Specialities
    specialities = [
        {'name': 'Cardiology', 'icon': 'fa-heart-pulse'},
        {'name': 'Dermatology', 'icon': 'fa-allergies'},
        {'name': 'Neurology', 'icon': 'fa-brain'},
        {'name': 'Pediatrics', 'icon': 'fa-baby'},
        {'name': 'Psychiatry', 'icon': 'fa-user-nurse'},
        {'name': 'Orthopedics', 'icon': 'fa-bone'},
        {'name': 'Ophthalmology', 'icon': 'fa-eye'},
        {'name': 'Dentistry', 'icon': 'fa-tooth'},
    ]

    for spec in specialities:
        s, created = Speciality.objects.get_or_create(name=spec['name'], defaults={'icon': spec['icon']})
        if created:
            print(f"Created speciality: {s.name}")

    # 2. Create Admin if not exists
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@medica.com', 'admin123')
        admin.role = 'admin'
        admin.first_name = 'Medica'
        admin.last_name = 'Admin'
        admin.save()
        print("Created superuser: admin")

    print("Seeding completed!")

if __name__ == '__main__':
    seed()
