import os
import django
from django.db import connection
import shutil
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medica.settings')
django.setup()

def reset_all():
    print("--- Starting Full Project Reset ---")

    with connection.cursor() as cursor:
        # 1. Drop all tables in the public schema
        print("1. Dropping all tables in public schema...")
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        print("   Done: Public tables dropped.")

        # 2. Clear Supabase Auth users
        print("2. Clearing Supabase Auth users...")
        try:
            # We use TRUNCATE CASCADE to clear users and their associated identities, etc.
            cursor.execute("TRUNCATE auth.users CASCADE;")
            print("   Done: Auth users cleared.")
        except Exception as e:
            print(f"   Note: Could not clear auth users via SQL (might lack high-level permissions): {e}")
            print("   You may need to clear users manually via Supabase Dashboard if this fails.")

    # 3. Delete migration files
    print("3. Deleting local migration files...")
    # List of apps to clear migrations for
    apps = ['medica911']
    
    for app in apps:
        migrations_dir = Path(app) / 'migrations'
        if migrations_dir.exists():
            for file in migrations_dir.glob('*.py'):
                if file.name != '__init__.py':
                    print(f"   Deleting {file}...")
                    file.unlink()
            
            # Also clean up __pycache__
            pycache = migrations_dir / '__pycache__'
            if pycache.exists():
                shutil.rmtree(pycache)
    print("   Done: Local migrations cleared.")

    print("\n--- Reset Complete! ---")
    print("Next steps:")
    print("1. python manage.py makemigrations medica911")
    print("2. python manage.py migrate")
    print("3. python seed_data.py (if you want to re-seed)")

if __name__ == '__main__':
    reset_all()

