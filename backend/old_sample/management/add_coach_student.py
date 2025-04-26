from django.core.management.base import BaseCommand
from coaching.models import User, CoachStudentMapping
import csv

student_num = 7

class Command(BaseCommand):
    help = 'Add multiple user info'

    def handle(self, *args, **options):
        with open('add_coach_student.csv', 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                coach_username = row['username']
                coach = User.objects.filter(username=coach_username)
                for i in range(student_num):
                    student_username = row[f's{i+1}']
                    if student_username != '':
                        student = User.objects.filter(username=student_username)
                        CoachStudentMapping.objects.create(coach_id=coach[0].id, student_id=student[0].id)
                    self.stdout.write(self.style.SUCCESS(f'Successfully created mapping: {coach_username} - {student_username}'))