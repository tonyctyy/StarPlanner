# yourappname/management/commands/import_methods.py

from django.core.management.base import BaseCommand
from coaching.models import Focus, Method, MethodFocusMapping, MethodSubjectMapping, Subject
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
            method = Method()
            
            method.name = row['name_eng']
            method.name_chin = row['name_chin']
            method.description = row['description_eng']
            method.description_chin = row['description_chin']
            
            method.social_style_amiable = int(row['amiable'])
            method.social_style_analytic = int(row['analytic'])
            method.social_style_expressive = int(
                row['expressive'])
            method.social_style_driver = int(row['driver'])
            method.time_consumption = row['time_consumption']
            method.beginner_suggestions = row['beginner_suggestions_eng']
            method.beginner_suggestions_chin = row['beginner_suggestions_chin']
            method.intermediate_suggestions = row['intermediate_suggestions_eng']
            method.intermediate_suggestions_chin = row['intermediate_suggestions_chin']
            method.advanced_suggestions = row['advanced_suggestions_eng']
            method.advanced_suggestions_chin = row['advanced_suggestions_chin']
            method.save()
            
            subjects = Subject.objects.all()
            for subject in subjects:
                if subject.name in row['suitable_subjects']:
                    new_method_subject_mapping = MethodSubjectMapping()
                    new_method_subject_mapping.method = method
                    new_method_subject_mapping.subject = subject
                    new_method_subject_mapping.save()
                    
            focus_list = Focus.objects.all()
            for focus in focus_list:
                if focus.name in row['study_focus']:
                    new_study_focus_mapping = MethodFocusMapping()
                    new_study_focus_mapping.method = method
                    new_study_focus_mapping.focus = focus
                    new_study_focus_mapping.save()
                    
                    

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
