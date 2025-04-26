from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from coaching.models import User
import csv

Django_User = get_user_model()


class Command(BaseCommand):
    help = 'Create multiple user accounts'

    def handle(self, *args, **options):
        with open('add_users.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                email = row['email']
                username = email
                class_no = row['class_no']
                password = f"holap.{class_no}"
                # password = row['phone_no'] 
                name_chinese = row['name_chinese']
                name = row['name']

                Django_User.objects.create_user(username=username, email=email, password=password)

                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))

                User.objects.create(username=username, name =name, name_chinese=name_chinese, email=email, role="student")


        # print(Django_User.objects.filter(username="user_0").values())
        # print(User.objects.filter(username="user_0").values())