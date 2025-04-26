# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone


class AcademicCoachingRecord(models.Model):
    coaching_report_record = models.ForeignKey(
        'CoachingReportRecord', models.DO_NOTHING, blank=True, null=True)
    learning_strategy_1 = models.IntegerField(blank=True, null=True)
    learning_strategy_2 = models.IntegerField(blank=True, null=True)
    learning_strategy_3 = models.IntegerField(blank=True, null=True)
    learning_strategy_comment = models.CharField(
        max_length=255, blank=True, null=True)
    goal_setting_1 = models.IntegerField(blank=True, null=True)
    goal_setting_2 = models.IntegerField(blank=True, null=True)
    goal_setting_3 = models.IntegerField(blank=True, null=True)
    goal_setting_comment = models.CharField(
        max_length=255, blank=True, null=True)
    organising_1 = models.IntegerField(blank=True, null=True)
    organising_2 = models.IntegerField(blank=True, null=True)
    organising_3 = models.IntegerField(blank=True, null=True)
    organising_comment = models.CharField(
        max_length=255, blank=True, null=True)
    motivation_and_accountability_1 = models.IntegerField(
        blank=True, null=True)
    motivation_and_accountability_2 = models.IntegerField(
        blank=True, null=True)
    motivation_and_accountability_3 = models.IntegerField(
        blank=True, null=True)
    motivation_and_accountability_comment = models.CharField(
        max_length=255, blank=True, null=True)
    time_management_1 = models.IntegerField(blank=True, null=True)
    time_management_2 = models.IntegerField(blank=True, null=True)
    time_management_3 = models.IntegerField(blank=True, null=True)
    time_management_comment = models.CharField(
        max_length=255, blank=True, null=True)
    life_balance_1 = models.IntegerField(blank=True, null=True)
    life_balance_2 = models.IntegerField(blank=True, null=True)
    life_balance_3 = models.IntegerField(blank=True, null=True)
    life_balance_comment = models.CharField(
        max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'academic_coaching_record'


class CoachInfo(models.Model):
    id = models.OneToOneField(
        'User', models.DO_NOTHING, db_column='id', primary_key=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'coach_info'


class CoachingReportRecord(models.Model):
    created_at = models.DateTimeField()
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='coaching_report_student')
    coach = models.ForeignKey('User', models.DO_NOTHING, blank=True,
                              null=True, related_name="coaching_report_coach")
    phase = models.IntegerField(blank=True, null=True)
    section = models.IntegerField()
    coaching_date = models.DateField()
    duration = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        managed = True
        db_table = 'coaching_report_record'


class CoachingReportDashboard(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phase = models.IntegerField(null=True)
    student = models.ForeignKey('User', models.DO_NOTHING)
    coach = models.ForeignKey('User', models.DO_NOTHING, related_name='coaching_reports_as_coach')
    before_social_style = models.ForeignKey('UserSocialStyle', models.DO_NOTHING, related_name='coaching_reports_before')
    after_social_style = models.ForeignKey('UserSocialStyle', models.DO_NOTHING, related_name='coaching_reports_after')
    social_style_type = models.CharField(max_length=63)
    social_style_comment = models.TextField(blank=True, null=True)
    critical_thinking_score = models.FloatField(blank=True, null=True)
    critical_thinking_comment = models.TextField(blank=True, null=True)
    problem_solving_score = models.FloatField(blank=True, null=True)
    problem_solving_comment = models.TextField(blank=True, null=True)
    managing_information_score = models.FloatField(blank=True, null=True)
    managing_information_comment = models.TextField(blank=True, null=True)
    creativity_and_innovation_score = models.FloatField(blank=True, null=True)
    creativity_and_innovation_comment = models.TextField(blank=True, null=True)
    communication_score = models.FloatField(blank=True, null=True)
    communication_comment = models.TextField(blank=True, null=True)
    collaboration_score = models.FloatField(blank=True, null=True)
    collaboration_comment = models.TextField(blank=True, null=True)
    cultural_and_global_citizenship_score = models.FloatField(blank=True, null=True)
    cultural_and_global_citizenship_comment = models.TextField(blank=True, null=True)
    personal_growth_and_wellbeing_score = models.FloatField(blank=True, null=True)
    personal_growth_and_wellbeing_comment = models.TextField(blank=True, null=True)

    critical_thinking_1 = models.FloatField(blank=True, null=True)
    critical_thinking_2 = models.FloatField(blank=True, null=True)
    critical_thinking_3 = models.FloatField(blank=True, null=True)
    critical_thinking_4 = models.FloatField(blank=True, null=True)
    critical_thinking_5 = models.FloatField(blank=True, null=True)
    
    problem_solving_1 = models.FloatField(blank=True, null=True)
    problem_solving_2 = models.FloatField(blank=True, null=True)
    problem_solving_3 = models.FloatField(blank=True, null=True)
    problem_solving_4 = models.FloatField(blank=True, null=True)
    problem_solving_5 = models.FloatField(blank=True, null=True)
    
    managing_information_1 = models.FloatField(blank=True, null=True)
    managing_information_2 = models.FloatField(blank=True, null=True)
    managing_information_3 = models.FloatField(blank=True, null=True)
    managing_information_4 = models.FloatField(blank=True, null=True)
    
    creativity_and_innovation_1 = models.FloatField(blank=True, null=True)
    creativity_and_innovation_2 = models.FloatField(blank=True, null=True)
    creativity_and_innovation_3 = models.FloatField(blank=True, null=True)
    creativity_and_innovation_4 = models.FloatField(blank=True, null=True)
    
    communication_1 = models.FloatField(blank=True, null=True)
    communication_2 = models.FloatField(blank=True, null=True)
    communication_3 = models.FloatField(blank=True, null=True)
    communication_4 = models.FloatField(blank=True, null=True)
    communication_5 = models.FloatField(blank=True, null=True)
    
    collaboration_1 = models.FloatField(blank=True, null=True)
    collaboration_2 = models.FloatField(blank=True, null=True)
    collaboration_3 = models.FloatField(blank=True, null=True)
    collaboration_4 = models.FloatField(blank=True, null=True)
    
    cultural_and_global_citizenship_1 = models.FloatField(blank=True, null=True)
    cultural_and_global_citizenship_2 = models.FloatField(blank=True, null=True)
    cultural_and_global_citizenship_3 = models.FloatField(blank=True, null=True)
    cultural_and_global_citizenship_4 = models.FloatField(blank=True, null=True)
    cultural_and_global_citizenship_5 = models.FloatField(blank=True, null=True)
    
    personal_growth_and_wellbeing_1 = models.FloatField(blank=True, null=True)
    personal_growth_and_wellbeing_2 = models.FloatField(blank=True, null=True)
    personal_growth_and_wellbeing_3 = models.FloatField(blank=True, null=True)
    personal_growth_and_wellbeing_4 = models.FloatField(blank=True, null=True)
    personal_growth_and_wellbeing_5 = models.FloatField(blank=True, null=True)
    
    learning_strategy_score = models.FloatField(blank=True, null=True)
    learning_strategy_comment = models.TextField(blank=True, null=True)
    goal_setting_score = models.FloatField(blank=True, null=True)
    goal_setting_comment = models.TextField(blank=True, null=True)
    organising_score = models.FloatField(blank=True, null=True)
    organising_comment = models.TextField(blank=True, null=True)
    motivation_and_accountability_score = models.FloatField(blank=True, null=True)
    motivation_and_accountability_comment = models.TextField(blank=True, null=True)
    time_management_score = models.FloatField(blank=True, null=True)
    time_management_comment = models.TextField(blank=True, null=True)
    life_balance_score = models.FloatField(blank=True, null=True)
    life_balance_comment = models.TextField(blank=True, null=True)

    learning_strategy_1 = models.FloatField(blank=True, null=True)
    learning_strategy_2 = models.FloatField(blank=True, null=True)
    learning_strategy_3 = models.FloatField(blank=True, null=True)

    goal_setting_1 = models.FloatField(blank=True, null=True)
    goal_setting_2 = models.FloatField(blank=True, null=True)
    goal_setting_3 = models.FloatField(blank=True, null=True)

    organising_1 = models.FloatField(blank=True, null=True)
    organising_2 = models.FloatField(blank=True, null=True)
    organising_3 = models.FloatField(blank=True, null=True)
   
    motivation_and_accountability_1 = models.FloatField(blank=True, null=True)
    motivation_and_accountability_2 = models.FloatField(blank=True, null=True)
    motivation_and_accountability_3 = models.FloatField(blank=True, null=True)

    time_management_1 = models.FloatField(blank=True, null=True)
    time_management_2 = models.FloatField(blank=True, null=True)
    time_management_3 = models.FloatField(blank=True, null=True)
    
    life_balance_1 = models.FloatField(blank=True, null=True)
    life_balance_2 = models.FloatField(blank=True, null=True)
    life_balance_3 = models.FloatField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'coaching_report_dashboard'
    

class CoachingReportDashboardSubjectComment(models.Model):
    subject_comment = models.TextField()
    subject_display_name = models.CharField(max_length=255, blank=True, null=True)
    report_dashboard = models.ForeignKey(CoachingReportDashboard, models.DO_NOTHING)
    subject = models.ForeignKey('Subject', models.DO_NOTHING)
    student = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'coaching_report_dashboard_subject_comments'


class CoachStudentMapping(models.Model):
    coach = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='coach')
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='student')

    class Meta:
        managed = True
        db_table = 'coach_student_mapping'


class Eca(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eca'


class FinalEvaluation(models.Model):
    student = models.ForeignKey('User', models.DO_NOTHING, blank=True,
                                null=True, related_name='final_evaluation_student')
    coach = models.ForeignKey('User', models.DO_NOTHING, blank=True,
                              null=True, related_name="final_evaluation_coach")
    created_at = models.DateTimeField()
    q1 = models.IntegerField(blank=True, null=True)
    q2 = models.IntegerField(blank=True, null=True)
    q3 = models.IntegerField(blank=True, null=True)
    q4 = models.IntegerField(blank=True, null=True)
    q5 = models.IntegerField(blank=True, null=True)
    q6 = models.IntegerField(blank=True, null=True)
    q7 = models.IntegerField(blank=True, null=True)
    q8 = models.IntegerField(blank=True, null=True)
    q9 = models.IntegerField(blank=True, null=True)
    q10 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'final_evaluation'


class Focus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_chin = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'focus'


class Goal(models.Model):
    goal_type = models.CharField(max_length=9, blank=True, null=True)
    difficulty = models.CharField(max_length=9, blank=True, null=True)
    goal_status = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    predicted_end_time = models.DateTimeField()
    end_at = models.DateTimeField()
    is_subgoal = models.IntegerField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', models.DO_NOTHING, db_column='parent', blank=True, null=True)
    final_result = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'goal'


class GoalEvaluate(models.Model):
    goal = models.ForeignKey(Goal, models.DO_NOTHING, blank=True, null=True)
    effort = models.IntegerField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    comment = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'goal_evaluate'


class Interest(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'interest'


class Method(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_chin = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    description_chin = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    social_style_amiable = models.IntegerField(blank=True, null=True)
    social_style_analytic = models.IntegerField(blank=True, null=True)
    social_style_expressive = models.IntegerField(blank=True, null=True)
    social_style_driver = models.IntegerField(blank=True, null=True)
    time_consumption = models.CharField(max_length=6, blank=True, null=True)
    beginner_suggestions = models.CharField(
        max_length=255, blank=True, null=True)
    beginner_suggestions_chin = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    intermediate_suggestions = models.CharField(
        max_length=255, blank=True, null=True)
    intermediate_suggestions_chin = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    advanced_suggestions = models.CharField(
        max_length=255, blank=True, null=True)
    advanced_suggestions_chin = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    detail_description = models.CharField(
        max_length=1023, db_collation='utf8_general_ci', blank=True, null=True)
    detail_description_chin = models.CharField(
        max_length=1023, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method'


class MethodFocusMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    focus = models.ForeignKey(Focus, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_focus_mapping'


class MethodLabel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_label'


class MethodLabelMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        MethodLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_label_mapping'


class MethodSubjectMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(
        'Subject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_subject_mapping'


class MethodTaskSuggestion(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    task_template = models.ForeignKey(
        'TaskTemplate', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_task_suggestion'


class Qualification(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qualification'


class SAndCRecord(models.Model):
    coaching_report_record = models.ForeignKey(
        CoachingReportRecord, models.DO_NOTHING, blank=True, null=True)
    critical_thinking_1 = models.IntegerField(blank=True, null=True)
    critical_thinking_2 = models.IntegerField(blank=True, null=True)
    critical_thinking_3 = models.IntegerField(blank=True, null=True)
    critical_thinking_4 = models.IntegerField(blank=True, null=True)
    critical_thinking_5 = models.IntegerField(blank=True, null=True)
    critical_thinking_comment = models.CharField(
        max_length=255, blank=True, null=True)
    problem_solving_1 = models.IntegerField(blank=True, null=True)
    problem_solving_2 = models.IntegerField(blank=True, null=True)
    problem_solving_3 = models.IntegerField(blank=True, null=True)
    problem_solving_4 = models.IntegerField(blank=True, null=True)
    problem_solving_5 = models.IntegerField(blank=True, null=True)
    problem_solving_comment = models.CharField(
        max_length=255, blank=True, null=True)
    managing_information_1 = models.IntegerField(blank=True, null=True)
    managing_information_2 = models.IntegerField(blank=True, null=True)
    managing_information_3 = models.IntegerField(blank=True, null=True)
    managing_information_4 = models.IntegerField(blank=True, null=True)
    managing_information_comment = models.CharField(
        max_length=255, blank=True, null=True)
    creativity_and_innovation_1 = models.IntegerField(blank=True, null=True)
    creativity_and_innovation_2 = models.IntegerField(blank=True, null=True)
    creativity_and_innovation_3 = models.IntegerField(blank=True, null=True)
    creativity_and_innovation_4 = models.IntegerField(blank=True, null=True)
    creativity_and_innovation_comment = models.CharField(
        max_length=255, blank=True, null=True)
    communication_1 = models.IntegerField(blank=True, null=True)
    communication_2 = models.IntegerField(blank=True, null=True)
    communication_3 = models.IntegerField(blank=True, null=True)
    communication_4 = models.IntegerField(blank=True, null=True)
    communication_5 = models.IntegerField(blank=True, null=True)
    communication_comment = models.CharField(
        max_length=255, blank=True, null=True)
    collaboration_1 = models.IntegerField(blank=True, null=True)
    collaboration_2 = models.IntegerField(blank=True, null=True)
    collaboration_3 = models.IntegerField(blank=True, null=True)
    collaboration_4 = models.IntegerField(blank=True, null=True)
    collaboration_comment = models.CharField(
        max_length=255, blank=True, null=True)
    cultural_and_global_citizenship_1 = models.IntegerField(
        blank=True, null=True)
    cultural_and_global_citizenship_2 = models.IntegerField(
        blank=True, null=True)
    cultural_and_global_citizenship_3 = models.IntegerField(
        blank=True, null=True)
    cultural_and_global_citizenship_4 = models.IntegerField(
        blank=True, null=True)
    cultural_and_global_citizenship_5 = models.IntegerField(
        blank=True, null=True)
    cultural_and_global_citizenship_comment = models.CharField(
        max_length=255, blank=True, null=True)
    personal_growth_and_wellbeing_1 = models.IntegerField(
        blank=True, null=True)
    personal_growth_and_wellbeing_2 = models.IntegerField(
        blank=True, null=True)
    personal_growth_and_wellbeing_3 = models.IntegerField(
        blank=True, null=True)
    personal_growth_and_wellbeing_4 = models.IntegerField(
        blank=True, null=True)
    personal_growth_and_wellbeing_5 = models.IntegerField(
        blank=True, null=True)
    personal_growth_and_wellbeing_comment = models.CharField(
        max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 's_and_c_record'


class StatusLabel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status_label'


class StudentInfo(models.Model):
    id = models.OneToOneField(
        'User', models.DO_NOTHING, db_column='id', primary_key=True)
    school = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    # Field renamed because it was a Python reserved word.
    class_field = models.CharField(
        db_column='class', max_length=255, blank=True, null=True)
    class_no = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student_info'


class StudentMethodEvaluate(models.Model):
    id = models.IntegerField(primary_key=True)
    student_method_mapping = models.ForeignKey(
        'StudentMethodMapping', models.DO_NOTHING, blank=True, null=True)
    suitable = models.IntegerField(blank=True, null=True)
    willingness = models.IntegerField(blank=True, null=True)
    comment = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'student_method_evaluate'


class StudentMethodMapping(models.Model):
    created_at = models.DateTimeField()
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True)
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    personalization = models.CharField(max_length=255, blank=True, null=True)
    related_goal = models.ForeignKey(
        Goal, models.DO_NOTHING, db_column='related_goal', blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    name = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student_method_mapping'


class StudentMethodSubjectMapping(models.Model):
    student_method_mapping = models.ForeignKey(StudentMethodMapping, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student_method_subject_mapping'


class StudentPreAssessment(models.Model):
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True)
    long_term_goal = models.CharField(max_length=255, blank=True, null=True)
    area_to_improve = models.CharField(max_length=255, blank=True, null=True)
    interested_question = models.CharField(
        max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    preferable_time_1 = models.DateTimeField()
    preferable_time_2 = models.DateTimeField()
    preferable_time_3 = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'student_pre_assessment'


class StudentStatusRecord(models.Model):
    created_at = models.DateTimeField()
    status = models.ForeignKey(
        StatusLabel, models.DO_NOTHING, blank=True, null=True)
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True)
    phy_health = models.IntegerField(blank=True, null=True)
    men_health = models.IntegerField(blank=True, null=True)
    stress = models.IntegerField(blank=True, null=True)
    motivation = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student_status_record'


class Subject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_chin = models.CharField(max_length=255, blank=True, null=True)
    name_abbr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'


class Task(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    predicted_end_time = models.DateTimeField()
    end_at = models.DateTimeField()
    description = models.CharField(max_length=255, blank=True, null=True)
    is_recurring = models.IntegerField(blank=True, null=True)
    recurring_cycle = models.IntegerField(blank=True, null=True)
    willingness = models.IntegerField(blank=True, null=True)
    effort = models.IntegerField(blank=True, null=True)
    effectiveness = models.IntegerField(blank=True, null=True)
    completeness = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)
    time_spent = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task'


class TaskSubjectMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_subject_mapping'
        unique_together = (('task', 'subject'),)


class TaskGoalMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    goal = models.ForeignKey(Goal, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_goal_mapping'
        unique_together = (('task', 'goal'),)


class TaskMethodMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    student_method_mapping = models.ForeignKey(
        StudentMethodMapping, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_method_mapping'
        unique_together = (('task', 'student_method_mapping'),)


class TaskTaskMapping(models.Model):
    parent_task = models.OneToOneField(
        Task, models.DO_NOTHING, primary_key=True, related_name="parent_task")
    child_task = models.ForeignKey(
        Task, models.DO_NOTHING, related_name="child_task")

    class Meta:
        managed = True
        db_table = 'task_task_mapping'
        unique_together = (('parent_task', 'child_task'),)


class TaskLabel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_label'


class TaskLabelMapping(models.Model):
    task = models.ForeignKey(Task, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        TaskLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_label_mapping'


class TaskTemplate(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    parent = models.CharField(max_length=6, blank=True, null=True)
    is_recurring = models.IntegerField(blank=True, null=True)
    recurring_cycle = models.IntegerField(blank=True, null=True)
    willingness = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_template'


class TaskTemplateLabelMapping(models.Model):
    task = models.ForeignKey(
        TaskTemplate, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        TaskLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_template_label_mapping'


class User(models.Model):

    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    name_chinese = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    role = models.CharField(max_length=20)
    phase = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        managed = True
        db_table = 'user'


class UserEca(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    eca = models.ForeignKey(Eca, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_eca'


class UserGradeRecord(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_grade_record'


class UserInterest(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    interest = models.ForeignKey(
        Interest, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_interest'


class UserQualification(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    qualification = models.ForeignKey(
        Qualification, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_qualification'


class UserSocialStyle(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField()
    driver = models.IntegerField(blank=True, null=True)
    amiable = models.IntegerField(blank=True, null=True)
    analytical = models.IntegerField(blank=True, null=True)
    expressive = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_social_style'


class UserSubjectGradeRecord(models.Model):
    parent = models.ForeignKey(
        UserGradeRecord, models.DO_NOTHING, db_column='parent', blank=True, null=True)
    subject = models.ForeignKey(
        Subject, models.DO_NOTHING, db_column='subject', blank=True, null=True)
    grade = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_subject_grade_record'


class UserSubjectList(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(
        Subject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_subject_list'
