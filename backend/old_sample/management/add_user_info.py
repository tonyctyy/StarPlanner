from django.core.management.base import BaseCommand
from coaching.models import User, UserSubjectList, UserSocialStyle
import csv

subject_columns = ['X1', 'X2', 'X3', 'M1', 'M2']
social_style_columns = ['amiable', 'analytical', 'expressive', 'driver']

class Command(BaseCommand):
    help = 'Add multiple user info'

    def handle(self, *args, **options):
        with open('add_user_info.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['email']
                user = User.objects.filter(username=username)


                subjects = [1, 2, 3, 4]
                for col in subject_columns:
                    if row[col] != '':
                        subjects.append(int(row[col]))
                for subject in subjects:
                    UserSubjectList.objects.create(user_id=user[0].id, subject_id=subject)
                

                UserSocialStyle.objects.create(user_id=user[0].id,  amiable=int(row['amiable']), analytical=int(row['analytical']), expressive=int(row['expressive']), driver=int(row['driver']))

                
                self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))


