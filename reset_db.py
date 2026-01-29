import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medica.settings')
django.setup()

def reset_migrations():
    with connection.cursor() as cursor:
        print("Clearing django_migrations table...")
        cursor.execute("DELETE FROM django_migrations")
        
        # Also drop all tables to start fresh if you want, 
        # but let's just try clearing migrations first.
        # Actually, let's just drop all tables in the public schema
        # to ensure a completely clean state for the new models.
        
        print("Dropping all tables in public schema...")
        cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
    print("Database reset successfully.")

if __name__ == '__main__':
    reset_migrations()
