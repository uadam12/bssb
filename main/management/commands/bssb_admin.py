from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Populate data base with some data'
    
    def handle(self, *args, **options):
        try:
            user = User(
                first_name = input('Enter admin firstname: '),
                last_name = input('Enter admin lastname: '),
                email = input('Enter admin email address: '),
                access_code = 4
            )
            user.set_password('bssbAdmin@12')
            user.save()
            print(f"Admin: {user} created successfully.")
        except Exception as e:
            print(e)