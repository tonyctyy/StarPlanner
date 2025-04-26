"""
Models for defining the database structure of the application.

These models represent the various entities and relationships within the database,
including data related to users, coaching sessions, academic goals, and more.
"""
from django.db import models

### The following models are used in the current version of the app. ###

# AcademicCoachingRecord includes all the model scores and comments for our Academic Coaching Focus (AC Model/Focus) used in academic coaching. It is a part of the CoachingReportRecord.
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

# CoachingReportRecord is the overall review after each coaching session. It includes the primay info of the session, such as the section, duration and overall comment. It is linked to the AcademicCoachingRecord and SAndCRecord.
class CoachingReportRecord(models.Model):
    created_at = models.DateTimeField()
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='coaching_report_student')
    coach = models.ForeignKey('User', models.DO_NOTHING, blank=True,
                              null=True, related_name="coaching_report_coach")
    comment = models.CharField(max_length=255, blank=True, null=True)
    section = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    phase = models.IntegerField(blank=True, null=True)
    coaching_date = models.DateTimeField()
    class Meta:
        managed = True
        db_table = 'coaching_report_record'

# CoachingReportDashboard is the final report after all coaching sessions. It includes all the essential components of our coaching model (i.e. Social Style, Academic Coaching Focus and Skils & Compentecies Model). It is used to create the final report that is shared with the student and school.
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

    subject_comment = models.TextField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'coaching_report_dashboard'
  
# CoachingReportDashboardSubjectComment is part of the CoachingReportDashboard. It includes the comments for each subject.
class CoachingReportDashboardSubjectComment(models.Model):
    subject_comment = models.TextField()
    report_dashboard = models.ForeignKey(CoachingReportDashboard, models.DO_NOTHING)
    subject = models.ForeignKey('Subject', models.DO_NOTHING)
    student = models.ForeignKey('User', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'coaching_report_dashboard_subject_comments'

# FinalEvaluation is the final questionnaire that is filled in the last coaching session. 
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

# Goal is the primay model for academic coaching. It includes the goal set by the student.
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

# GoalEvaluate is used to store the evaluation of the goal and there can be multiple evaluations for a goal. (We conduct goal evaluation every month.)
class GoalEvaluate(models.Model):
    goal = models.ForeignKey(Goal, models.DO_NOTHING, blank=True, null=True)
    effort = models.IntegerField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    comment = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'goal_evaluate'

# PreAcademicCoachingRecord is used to store the AC Model/Focus scores and comments for the first quarter of the coaching (evaluated after 3-4 sessions). It provides a brief overview of the student's performance in the AC Model/Focus and is used in the final report.
class PreAcademicCoachingRecord(models.Model):
    student = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='pre_academic_coaching_student', db_column='student')
    coach = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True, related_name='pre_academic_coaching_coach', db_column='coach')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phase = models.IntegerField(null=True)
    learning_strategy = models.IntegerField(null=True)
    goal_setting = models.IntegerField(null=True)
    organising = models.IntegerField(null=True)
    motivation_and_accountability = models.IntegerField(null=True)
    time_management = models.IntegerField(null=True)
    life_balance = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'pre_academic_coaching_record'

# SAndCRecord includes all the model scores and comments for our Skills & Competencies Model (S&C Model) used in academic coaching. It is a part of the CoachingReportRecord.
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

# StudentPreAssessment includes the long term goal, area to improve, interested question, preferable time and created at.
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

# Subject includs all the subjects in DSE.
class Subject(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_chin = models.CharField(max_length=255, blank=True, null=True)
    name_abbr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject'

# Task is the primary model for academic coaching. It includes the task set by the student. Evaluation of the task is also included and done every week.
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

# TaskSubjectMapping is used to link the task and subject.
class TaskSubjectMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    subject = models.ForeignKey(Subject, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_subject_mapping'
        unique_together = (('task', 'subject'),)

# TaskGoalMapping is used to link the task and goal.
class TaskGoalMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    goal = models.ForeignKey(Goal, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_goal_mapping'
        unique_together = (('task', 'goal'),)

# TaskTaskMapping is used to link the parent task and child task.
class TaskTaskMapping(models.Model):
    parent_task = models.OneToOneField(
        Task, models.DO_NOTHING, primary_key=True, related_name="parent_task")
    child_task = models.ForeignKey(
        Task, models.DO_NOTHING, related_name="child_task")

    class Meta:
        managed = True
        db_table = 'task_task_mapping'
        unique_together = (('parent_task', 'child_task'),)

# User includes all the users in the system.
class User(models.Model):

    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255)
    name_chinese = models.CharField(
        max_length=255, db_collation='utf8_general_ci', blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    role = models.CharField(max_length=20)
    phase = models.IntegerField(default=1)
    calendar_data = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user'

# UserGradeRecord is used to store the student's grade record. It is linked to the UserSubjectGradeRecord.
class UserGradeRecord(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_grade_record'

# UserSocialStyle is used to store the social style of the user.
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

# UserSubjectGradeRecord is used to store the student's grade record for each subject. It is linked to the UserGradeRecord.
class UserSubjectGradeRecord(models.Model):
    parent = models.ForeignKey(
        UserGradeRecord, models.DO_NOTHING, db_column='parent', blank=True, null=True)
    subject = models.ForeignKey(
        Subject, models.DO_NOTHING, db_column='subject', blank=True, null=True)
    grade = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_subject_grade_record'

# UsreSubjectList is used to link the user and subject.
class UserSubjectList(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(
        Subject, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_subject_list'



### The following models are not implemented in v2 but should be implemented ASAP or are used in the temp system. ###

# CoachInfo includes the university, major, and level of the coach.
class CoachInfo(models.Model):
    id = models.OneToOneField(
        'User', models.DO_NOTHING, db_column='id', primary_key=True)
    university = models.CharField(max_length=255, blank=True, null=True)
    major = models.CharField(max_length=255, blank=True, null=True)
    level = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'coach_info'

# StudentInfo includes the school, nickname, class, and class number of the student.
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


# Eca is the model for the Extra Curricular Activities. 
class Eca(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'eca'

# UserECA is used to link the user and ECA.
class UserEca(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    eca = models.ForeignKey(Eca, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_eca'

# Qualification is the model for the qualification obtained by the user.
class Qualification(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'qualification'

# UserQualification is used to link the user and qualification.
class UserQualification(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    qualification = models.ForeignKey(
        Qualification, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_qualification'

# CoachStudentMapping is used to store the Coach and Coachee mapping. It is used to link the coach and student.
class CoachStudentMapping(models.Model):
    coach = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='coach')
    student = models.ForeignKey(
        'User', models.DO_NOTHING, blank=True, null=True, related_name='student')

    class Meta:
        managed = True
        db_table = 'coach_student_mapping'



### The following models are not used in the current version of the app. ###

"""        
# Interest is the model for the student's interest (e.g. basketball).
class Interest(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'interest'

# UserInterest is used to link the user and interest.
class UserInterest(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    interest = models.ForeignKey(
        Interest, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_interest'

# StatusLabel is status of the student in each coaching/daily (e.g. stressed, passionate).
class StatusLabel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status_label'

# StudentStatusLabelMapping is used to link the student and status label.
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

# Focus is used to label study methods (e.g. reading comphrension).
class Focus(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_chin = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'focus'

# TaskLabel is used to label task. 
class TaskLabel(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_label'

# TaskLabelMapping is used to link the task and label.
class TaskLabelMapping(models.Model):
    task = models.ForeignKey(Task, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        TaskLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_label_mapping'

# TaskTemplate is the suggested task for the student.
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

# TaskTemplateFocusMapping is used to link the task template and student to see if the suggested tasks are applied.
class TaskTemplateLabelMapping(models.Model):
    task = models.ForeignKey(
        TaskTemplate, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        TaskLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'task_template_label_mapping'

# TaskMethodMapping is used to link the task and method.
class TaskMethodMapping(models.Model):
    task = models.OneToOneField(Task, models.DO_NOTHING, primary_key=True)
    student_method_mapping = models.ForeignKey(
        StudentMethodMapping, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'task_method_mapping'
        unique_together = (('task', 'student_method_mapping'),)

# Method is essential for academic coaching and we need to gather more data and information from the coach and students.
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

# MethodFocusMapping is used to link the method and focus.
class MethodFocusMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    focus = models.ForeignKey(Focus, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_focus_mapping'

# MethodLabel is used to store the labels for the method.
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_label'

# MethodLabelMapping is used to link the method and label.
class MethodLabelMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    label = models.ForeignKey(
        MethodLabel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_label_mapping'

# MethodSubjectMapping is used to link the method and subject.
class MethodSubjectMapping(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(
        'Subject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_subject_mapping'

# MethodTaskSuggestion is used to link the method and task template.
class MethodTaskSuggestion(models.Model):
    method = models.ForeignKey(
        Method, models.DO_NOTHING, blank=True, null=True)
    task_template = models.ForeignKey(
        'TaskTemplate', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'method_task_suggestion'

# StudentMethodEvaluate is used to store the evaluation of the method by the student.
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

# StudentMethodMapping is used to link the student and method.
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

# StudentMethodSubjectMapping is used to link the student, method and subject (To see what subjects the method is applied to). 
class StudentMethodSubjectMapping(models.Model):
    student_method_mapping = models.ForeignKey(StudentMethodMapping, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey('Subject', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'student_method_subject_mapping'

"""