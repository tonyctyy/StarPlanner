# yourappname/management/commands/import_methods.py

from django.core.management.base import BaseCommand
from coaching.models import CoachStudentMapping, Focus, Method, MethodFocusMapping, MethodSubjectMapping, Subject, User, UserSocialStyle, UserSubjectList
from django.contrib.auth.models import User as AuthUser
import pandas as pd


class Command(BaseCommand):
    help = 'Import methods from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str,
                            help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file)

        for _, row in df.iterrows():
            user = User()
            user.username = row['username']
            user.email = row['email']
            user.name = row['name']
            user.name_chinese= row['name_chin']
            user.role = "student"
            user.save()
            
            authuser = AuthUser.objects.create_user(
                username=row['username'],
                email=row['email'],
                password="Star@1234",
            )
            
            social_style = UserSocialStyle()
            social_style.user = user
            social_style.driver = int(row['driver'])
            social_style.expressive = int(row['expressive'])
            social_style.amiable = int(row['amiable'])
            social_style.analytical = int(row['analytic'])
            
            social_style.save()
            
            coach_student_mapping = CoachStudentMapping()
            coach_student_mapping.coach = User.objects.get(username=row['coach'])
            coach_student_mapping.student = user
            coach_student_mapping.save()
            
            
            for i in range(1,5):
                user_subject_list = UserSubjectList()
                user_subject_list.user = user
                user_subject_list.subject_id = i
                user_subject_list.save()
            
            subjects = Subject.objects.all()
            for subject in subjects:
                if (subject.name in row['elective1']) or( subject.name_chin in row['elective1']) or (subject.name_abbr in row['elective1']):
                    user_subject_list = UserSubjectList()
                    user_subject_list.user = user
                    user_subject_list.subject = subject
                    user_subject_list.save()
                    break
            for subject in subjects:
                if (subject.name in row['elective2']) or (subject.name_chin in row['elective2'] )or (subject.name_abbr in row['elective2']):
                    user_subject_list = UserSubjectList()
                    user_subject_list.user = user
                    user_subject_list.subject = subject
                    user_subject_list.save()
                    break
            for subject in subjects:
                if( subject.name in row['elective3']) or( subject.name_chin in row['elective3']) or( subject.name_abbr in row['elective3']):
                    user_subject_list = UserSubjectList()
                    user_subject_list.user = user
                    user_subject_list.subject = subject
                    user_subject_list.save()
                    break
                    

                    
                    

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
