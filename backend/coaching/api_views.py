from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User as AuthUser
from .forms import *
from .models import *
from operator import attrgetter
from .serializers import *
from .gpt_prompts import gpt_prompt

# Dictionary to map model names to their respective fields
MODEL_DICT = {
    's_and_c': ['critical_thinking', 'problem_solving', 'managing_information', 'creativity_and_innovation', 'communication', 'collaboration', 'cultural_and_global_citizenship', 'personal_growth_and_wellbeing'],
    'ac': ['learning_strategy', 'goal_setting', 'organising', 'motivation_and_accountability', 'time_management', 'life_balance']
}

# Dictionary to map model names to their respective fields in Chinese
MODEL_DICT_CHIN = {
    's_and_c': ['批判性思維', '解決問題', '管理資訊', '創意與創新', '表達與溝通', '團隊合作', '文化和全球公民意識', '個人成長'],
    'ac': ['學習策略', '目標設定', '組織管理', '動機與責任', '時間管理', '生活平衡']
}

# Dictionary to map model names to their respective fields and the scores in each field
MODEL_SCORE_DICT = {
    's_and_c': {
        'critical_thinking': ['critical_thinking_1', 'critical_thinking_2', 'critical_thinking_3', 'critical_thinking_4', 'critical_thinking_5'],
        'problem_solving': ['problem_solving_1', 'problem_solving_2', 'problem_solving_3', 'problem_solving_4', 'problem_solving_5'],
        'managing_information': ['managing_information_1', 'managing_information_2', 'managing_information_3', 'managing_information_4'],
        'creativity_and_innovation': ['creativity_and_innovation_1', 'creativity_and_innovation_2', 'creativity_and_innovation_3', 'creativity_and_innovation_4'],
        'communication': ['communication_1', 'communication_2', 'communication_3', 'communication_4', 'communication_5'],
        'collaboration': ['collaboration_1', 'collaboration_2', 'collaboration_3', 'collaboration_4'],
        'cultural_and_global_citizenship': ['cultural_and_global_citizenship_1', 'cultural_and_global_citizenship_2', 'cultural_and_global_citizenship_3', 'cultural_and_global_citizenship_4', 'cultural_and_global_citizenship_5'],
        'personal_growth_and_wellbeing': ['personal_growth_and_wellbeing_1', 'personal_growth_and_wellbeing_2', 'personal_growth_and_wellbeing_3', 'personal_growth_and_wellbeing_4', 'personal_growth_and_wellbeing_5']
        },
    'ac': {
        'learning_strategy': ['learning_strategy_1', 'learning_strategy_2', 'learning_strategy_3'],
        'goal_setting': ['goal_setting_1', 'goal_setting_2', 'goal_setting_3'],
        'organising': ['organising_1', 'organising_2', 'organising_3'],
        'motivation_and_accountability': ['motivation_and_accountability_1', 'motivation_and_accountability_2', 'motivation_and_accountability_3'],
        'time_management': ['time_management_1', 'time_management_2', 'time_management_3'],
        'life_balance': ['life_balance_1', 'life_balance_2', 'life_balance_3']
        }
        }

# Dictionary to map model names to their respective comments in each field
COMMENT_LIST_DICT = {
    's_and_c': ['critical_thinking_comment', 'problem_solving_comment', 'managing_information_comment',                'creativity_and_innovation_comment', 'communication_comment', 'collaboration_comment',                 'cultural_and_global_citizenship_comment', 'personal_growth_and_wellbeing_comment'],
    'ac': ['learning_strategy_comment', 'goal_setting_comment', 'organising_comment', 'motivation_and_accountability_comment', 'time_management_comment', 'life_balance_comment'], 'report': ['comment']
}



### The following API endpoints are used to handle the student dashboard ###

# API endpoint for the student dashboard (homepage), displaying goals, tasks, and subjects
# If it is the final report, it is used to get all the goals and tasks
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def student_dashboard_api(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if it is called for the final report
    isFinal = request.data.get('isFinal')

    # Retrieve student's goals, tasks, and subjects
    goals = get_goals(student, isFinal)    
    # methods = get_methods(student)
    tasks = get_tasks(student, isFinal)   
    subjects = get_subjects(student)

    # Return dashboard data
    return Response({
        'goals': goals,
        # 'methods': methods,
        'tasks': tasks,
        'subjects': subjects
    })


# API endpoint for adding a goal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def add_goal(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Extract goal data from request
    goal = request.data.get('goal')

    # Create a new goal instance and populate it with data
    new_goal = Goal()
    new_goal.student_id = student.id
    new_goal.goal_type = goal['goal_type']
    new_goal.difficulty = goal['difficulty']
    new_goal.description = goal['description']
    new_goal.predicted_end_time = goal['predicted_end_time']
    new_goal.name = goal['name']
    new_goal.goal_status = 'on going'

    # Check if the goal is a subgoal
    goal_parent_id = int(goal['goal_id'])
    if goal_parent_id!=0:
        new_goal.parent_id = goal_parent_id
        new_goal.is_subgoal = 1
    else:
        new_goal.is_subgoal = 0

    # Save the new goal instance
    new_goal.save()

    return Response(status=status.HTTP_201_CREATED)


# API endpoint for evaluating a goal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def evaluate_goal(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Extract evaluation data from request
    evaluation = request.data['evaluation']

    # Retrieve the goal instance to be evaluated
    goal = Goal.objects.get(id=evaluation['goal_id'])

    # Create a new goal evaluation instance and populate it with data
    goal_evaluation = GoalEvaluate()
    goal_evaluation.effort = evaluation['effort']
    goal_evaluation.progress = evaluation['progress']
    goal_evaluation.comment = evaluation['comment']
    goal_evaluation.goal_id = evaluation['goal_id']

    # Save the new goal evaluation instance
    goal_evaluation.save()

    # Update goal status if evaluation indicates completion
    if evaluation['status'] != "on going":
        goal.goal_status = evaluation['status']
        goal.final_result = evaluation['final_result']
        goal.end_at = datetime.now()
    
    # Evaluate subgoals of the goal
        evaluate_sub_goal(evaluation['goal_id'], student.id, evaluation)
        goal.save()
    
    return Response(status=status.HTTP_200_OK)


# API endpoint for adding a task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def add_task(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Extract task data from request
    task = request.data.get('task')

    # Create a new task instance and populate it with data
    new_task = Task()
    new_task.name = task['name']
    new_task.student_id = student.id
    new_task.predicted_end_time = task['predicted_end_time']
    new_task.description = task['description']
    new_task.status = 'on going'
    new_task.priority = task['priority']

    # Save the new task instance
    new_task.save()

    # Link the task to related subjects, goals, methods, and parent tasks
    subject_id = int(task['subject_id'])
    goal_id = int(task['goal_id'])
    method_id = int(task['method_id'])
    task_id = int(task['task_id'])

    # Link task to subject if specified
    if subject_id != 0:
        new_task_subject_mapping = TaskSubjectMapping()
        new_task_subject_mapping.task_id = new_task.id
        new_task_subject_mapping.subject_id = subject_id
        new_task_subject_mapping.save()

    # Link task to goal if specified
    if goal_id != 0:
        new_task_goal_mapping = TaskGoalMapping()
        new_task_goal_mapping.task_id = new_task.id
        new_task_goal_mapping.goal_id = goal_id
        new_task_goal_mapping.save()

    # Link task to method if specified
    # if method_id != 0:
    #     new_task_method_mapping = TaskMethodMapping()
    #     new_task_method_mapping.task_id = new_task.id
    #     new_task_method_mapping.student_method_mapping_id = method_id
    #     new_task_method_mapping.save()
    
    # Link task to parent task if specified
    if task_id != 0:
        new_task_task_mapping = TaskTaskMapping()
        new_task_task_mapping.child_task_id = new_task.id
        new_task_task_mapping.parent_task_id = task_id
        new_task_task_mapping.save()  

    return Response(status=status.HTTP_201_CREATED)


# API endpoint for evaluating a task
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def evaluate_task(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Extract evaluation data from request
    evaluation = request.data['evaluation']

    # Retrieve the task instance to be evaluated
    task = Task.objects.get(id=evaluation['task_id'])

    # Update task attributes with evaluation data
    task.effort = evaluation['effort']
    task.effectiveness = evaluation['effectiveness']
    task.comment = evaluation['comment']
    task.willingness = evaluation['willingness']
    task.status = evaluation['status']
    task.completeness = evaluation['completeness']
    task.time_spent = evaluation['time_spent']
    task.end_at = datetime.now()

    # Evaluate subtasks of the task
    evaluate_sub_task(evaluation['task_id'], student.id, evaluation)

    # Save the updated task instance
    task.save()
    return Response(status=status.HTTP_200_OK)


# API endpoint for retrieving calendar data in the student dashboard
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_calendar_data(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
  
    # Retrieve calendar data for the student
    calendar_data = student.calendar_data

    # Return calendar data
    return Response({
    'calendar_data': calendar_data
  })
  
# API endpoint for saving calendar data in the student dashboard
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def save_calendar_data(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Update student's calendar data
    student.calendar_data  = request.data.get('calendar_data')
    student.save()

    return Response(status=status.HTTP_201_CREATED)    



### The following API endpoints are used to handle the session report ###

# API endpoint for getting the list of session report headers (date and section)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_session_reports(request):
    # Retrieve the authenticated student
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve session reports for the student
    session_reports = CoachingReportRecord.objects.filter(student_id=student.id, phase=student.phase).order_by('coaching_date').values_list('id', 'section')

    # Prepare data for response
    data = [{'id': report[0], 'section': report[1]} for report in session_reports]

    return Response(data = data, status=status.HTTP_200_OK)


# API endpoint for getting the detail of a session report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_session_report(request):
    # Retrieve report ID from request data
    report_id = request.data.get('report_id')

    # Retrieve the session report instance
    session_report = CoachingReportRecord.objects.get(id=report_id)

    # Retrieve associated Academic Coaching Record
    session_report.ACRecord = AcademicCoachingRecord.objects.filter(coaching_report_record_id=report_id)[0]

    # session_report.SAndCRecord = SAndCRecord.objects.filter(coaching_report_record_id=report_id)[0]

    # Serialize session report data
    session_report_serializer = CoachingReportRecordSerializer(session_report, many=False)

    return Response(session_report_serializer.data)


# API endpoint for adding a session report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def add_session_report(request):
    # Retrieve student and coach IDs from request data
    student_id = request.data.get('student_id')
    coach_id = request.data.get('coach_id')

    # Check if coach-student mapping exists
    if not CoachStudentMapping.objects.filter(student_id=student_id, coach_id=coach_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Extract report data from request
    report = request.data.get('report')

    # Create new session report instance and populate it with data
    session_report = CoachingReportRecord()
    session_report.student_id = student_id
    session_report.coach_id = coach_id
    session_report.coaching_date = report['coaching_date']
    session_report.section = report['section']
    session_report.phase = User.objects.get(id=student_id).phase
    session_report.comment = report['comment']
    session_report.duration = report['duration']
    session_report.save()

    # s_and_c_record = SAndCRecord()
    # s_and_c_record.coaching_report_record_id = session_report.id
    # s_and_c_record.save()

    # Create corresponding Academic Coaching Record
    ac_record = AcademicCoachingRecord()
    ac_record.coaching_report_record_id = session_report.id
    ac_record.save() 

    return Response(status=status.HTTP_201_CREATED)


# API endpoint for editing a session report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def edit_session_report(request):
    # Retrieve report ID and data from request
    report = request.data.get('report')
    report_id = request.data.get('report_id')

    # Check if report exists
    if CoachingReportRecord.objects.filter(id=report_id).exists():
        # Retrieve and update session report instance
        session_report = CoachingReportRecord.objects.get(id=report_id)
        session_report.coaching_date = report['coaching_date']
        session_report.section = report['section']
        session_report.comment = report['comment']
        session_report.duration = report['duration']
        session_report.save()

    return Response(status=status.HTTP_200_OK)


# API endpoint for editing the Academic Coaching Focus/Model scores and comment in a session report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def edit_ac_record(request):
    # Retrieve report ID and data from request
    report = request.data.get('record')
    report_id = request.data.get('report_id')

    # Check if Academic Coaching Record exists
    if AcademicCoachingRecord.objects.filter(id=report_id).exists():
        # Retrieve and update Academic Coaching Record instance
        ACRecord = AcademicCoachingRecord.objects.get(id=report_id)
        for key in report:
            if key == 'id' or key == 'coaching_report_record':
                continue
            # Set attribute value from request data
            value = report[key]
            if report[key] == -1:
                value = None
            setattr(ACRecord, key, value)
        ACRecord.save()
    
    return Response(status=status.HTTP_200_OK)



### The following API endpoints are used to handle the final report ###

# API endpoint for getting the list of comments for a student in the final report
# These comments will be used to generate comments with GPT-3.5
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_comment_list(request):
    student_id = request.data.get('student_id')
    if not User.objects.filter(id=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    student = User.objects.get(id=student_id)


    # Get coaching reports and associated records for the student
    reports = CoachingReportRecord.objects.filter(student_id=student.id, phase=student.phase)
    ac = AcademicCoachingRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports)
    sc = SAndCRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports)

    # Get comments and choices for each model (Academic Coaching, S&C)
    sc_get = get_comments(sc, 's_and_c')
    sc_comments, sc_choices = sc_get[0], sc_get[1]
    ac_get = get_comments(ac, 'ac')
    ac_comments, ac_choices = ac_get[0], ac_get[1]    
    report_get = get_comments(reports, 'report')
    report_comments, report_choices = report_get[0], report_get[1]

    # Merge all comments into a single dictionary
    comment_list = {**report_comments, **sc_comments, **ac_comments}

    comment_dict = {'sc': sc_comments, 'ac':ac_comments, 'report': report_comments}
    return JsonResponse(comment_dict)


# API endpoint for getting the generated comment for a section in the final report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_gpt_comment(request):
    student_id = request.data.get('student_id')

    if not User.objects.filter(id=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    student = User.objects.get(id=student_id)

    if not(CoachingReportDashboard.objects.filter(student_id = student.id, phase=student.phase).exists()):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    report_dashboard = CoachingReportDashboard.objects.filter(student_id = student.id, phase=student.phase)[0]
    section = request.data.get('section')
    model_area = request.data.get('model_area')
    selected_comments = request.data.get('selected_comments')
    personalized_comments = request.data.get('personalized_comments')
    if section == 'general':
        section = 'general'
    scores = get_detail_score(model_area, section, report_dashboard)
    if (type(scores)!= list):
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    generated_comment = gpt_prompt(section, scores, selected_comments, personalized_comments) 
    return Response(data = generated_comment, status=status.HTTP_200_OK)


# API endpoint for getting the final report of a student
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_final_report(request):
    student_id = request.data.get('student_id')
    coach_id = request.data.get('coach_id')
    student = User.objects.get(id=student_id)

    # If the final report doesn't exist, create a new one (replication problem, create two record instead of one)
    if not(CoachingReportDashboard.objects.filter(student_id = student.id, phase=student.phase).exists()):
        report_dashboard = CoachingReportDashboard()
        report_dashboard.student_id = student_id
        report_dashboard.coach_id = coach_id
        report_dashboard.phase = student.phase
        report_dashboard.save()

    report_dashboard = CoachingReportDashboard.objects.filter(student_id = student.id, phase=student.phase)[0]

    # Fetch and set various lists and objects for the final report
    report_dashboard.s_and_c_list, report_dashboard.s_and_c_scores = get_model_list('s_and_c', report_dashboard)
    report_dashboard.ac_list, report_dashboard.ac_scores = get_model_list('ac', report_dashboard)
    report_dashboard.subject_list = CoachingReportDashboardSubjectComment.objects.filter(report_dashboard_id=report_dashboard.id)

    report_dashboard.student = student
    report_dashboard.coach = User.objects.get(id=coach_id)

    if UserSocialStyle.objects.filter(id = report_dashboard.before_social_style_id).exists():
        report_dashboard.before = UserSocialStyle.objects.get(id = report_dashboard.before_social_style_id)
    if UserSocialStyle.objects.filter(id = report_dashboard.after_social_style_id).exists():
        report_dashboard.after = UserSocialStyle.objects.get(id = report_dashboard.after_social_style_id)

    report_dashboard_serializer = CoachingReportDashboardSerializer(report_dashboard, many=False)
    return Response(report_dashboard_serializer.data)


# API endpoint for editing a part of the final report (Social Style/Academic Coaching Focus/ Skills & Competencies Model)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def edit_final_report(request):
    report = request.data.get('report')
    report_id = report['id']
    part = request.data.get('part')
    if CoachingReportDashboard.objects.filter(id=report_id).exists():
        report_dashboard = CoachingReportDashboard.objects.get(id=report_id)
        if (part == 'social_style'):
            # report_dashboard.before_social_style_id = report['before_social_style_id']
            report_dashboard.after_social_style_id = report['after_social_style']
            report_dashboard.social_style_comment = report['social_style_comment']
            report_dashboard.social_style_type = report['social_style_type']
        elif (part == 'ac' or part == 's_and_c'):
            set_model_score(part, report_dashboard, report)
        report_dashboard.save()
    return Response(status=status.HTTP_200_OK)


# API endpoint for getting the list of subject comments in the final report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_subject_comments(request):
    student_id = request.data.get('student_id')
    if not User.objects.filter(id=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    student = User.objects.get(id=student_id)
    report_dashboard = CoachingReportDashboard.objects.filter(student_id = student.id, phase=student.phase)[0]
    subject_comment = CoachingReportDashboardSubjectComment.objects.filter(report_dashboard_id=report_dashboard.id)
    subject_comment_serializer = CoachingReportDashboardSubjectCommentSerializer(subject_comment, many=True)
    return Response(subject_comment_serializer.data)


# API endpoint for adding a subject comment in the final report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_subject_comment(request):
    student_id = request.data.get('student_id')
    coach_id = request.data.get('coach_id')
    if not CoachStudentMapping.objects.filter(student_id=student_id, coach_id=coach_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    subject = request.data.get('subject')
    report_id = request.data.get('report_id')
    subject_comment = CoachingReportDashboardSubjectComment()
    subject_comment.report_dashboard_id = report_id
    subject_comment.subject_id = subject['subject']
    subject_comment.subject_comment = subject['comment']
    subject_comment.student_id = student_id
    subject_comment.save()
    return Response(status=status.HTTP_201_CREATED)


# API endpoint for editing a subject comment in the final report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def edit_subject_comment(request):
    student_id = request.data.get('student_id')
    coach_id = request.data.get('coach_id')
    if not CoachStudentMapping.objects.filter(student_id=student_id, coach_id=coach_id).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    subject = request.data.get('subject')
    report_id = request.data.get('report_id')

    if subject['subject'] == 0:
        report = CoachingReportDashboard.objects.get(id=report_id)
        report.subject_comment = subject['comment']
        report.save()
    else:
        if CoachingReportDashboardSubjectComment.objects.filter(subject_id=subject['subject'], report_dashboard_id=report_id).exists():
            subject_comment = CoachingReportDashboardSubjectComment.objects.get(subject_id=subject['subject'], report_dashboard_id=report_id)
            subject_comment.subject_comment = subject['comment']
            subject_comment.save()
    return Response(status=status.HTTP_200_OK)



### Other API endpoints ###

# API endpoint for the web app header, which returns the list of students of the logged-in coach
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def get_student_list(request):
    # Retrieve user information
    user = User.objects.get(username=request.user.username)
    role = user.role
    coach = get_coach(request)
    student_list = []

    # Check if the logged-in user is a superuser
    if request.user.is_superuser:
        role = 'coach'

    # Retrieve student list based on user role
    if role == 'coach':
        students_id = CoachStudentMapping.objects.filter(coach_id=user.id).values_list('student_id', flat=True)
        students = User.objects.filter(id__in=students_id)
        student_list = [{"id": student.id, "name": f"{student.name} {student.name_chinese} ({student.username})"} for student in students ]
    
   
    data = {"profiles": student_list, "role": role, "user_name": f"{user.name} {user.name_chinese} ({user.username})", "coach": {"id": coach.id, "name": f"{coach.name} - {coach.name_chinese} ({coach.username})"}}
    return Response(data = data, status=status.HTTP_200_OK)


# API endpoint for getting the list of social style records
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_social_style(request):
    # Retrieve student ID from request data
    student_id = request.data.get('student_id')

    # Check if student exists
    if not User.objects.filter(id=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve social style records for the student
    student = User.objects.get(id=student_id)
    social_style = UserSocialStyle.objects.filter(user_id=student.id)
    social_style = sorted(social_style, key=attrgetter('created_at'), reverse=True)
    social_style_serializer = UserSocialStyleSerializer(social_style, many=True)

    return Response(social_style_serializer.data)


# API endpoint for adding a social style score record
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def add_social_style(request):
    # Retrieve student information
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Retrieve social style data from request
    social_style = request.data.get('social_style')

    # Create and save new social style record
    new_social_style = UserSocialStyle()
    new_social_style.user_id = student.id
    new_social_style.analytical = social_style['analytical']
    new_social_style.driver = social_style['driver']
    new_social_style.amiable = social_style['amiable']
    new_social_style.expressive = social_style['expressive']
    new_social_style.save()

    return Response(status=status.HTTP_201_CREATED)


# API endpoint for getting the Pre-Academic Coaching Focus/Model Scores for a student. It is used in the AC Focus graph in the final report
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_pre_ac_record(request):
    # Retrieve student information
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if Pre-Academic Coaching Focus/Model Scores exist for the student
    if PreAcademicCoachingRecord.objects.filter(student_id=student.id, phase=student.phase).exists():
        pre_ac_record = PreAcademicCoachingRecord.objects.filter(student_id=student.id, phase=student.phase)[0]
        pre_ac_record_serializer = PreAcademicCoachingRecordSerializer(pre_ac_record, many=False)
        return Response(pre_ac_record_serializer.data)        
    return Response(status=status.HTTP_404_NOT_FOUND)


# API endpoint for adding or editing the Pre-Academic Coaching Focus/Model Scores for a student
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_edit_pre_ac_record(request):
    # Retrieve student and coach information
    student = get_student(request)
    coach_id = request.data.get('coach_id')
    data = request.data.get('record')
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if Pre-Academic Coaching Focus/Model Scores exist for the student
    if PreAcademicCoachingRecord.objects.filter(student_id=student.id, phase=student.phase).exists():
        pre_ac_record = PreAcademicCoachingRecord.objects.filter(student_id=student.id, phase=student.phase)[0]
    else:
        pre_ac_record = PreAcademicCoachingRecord()
        pre_ac_record.student_id = student.id
        pre_ac_record.coach_id = coach_id
        pre_ac_record.phase = student.phase

    # Update Pre-Academic Coaching Focus/Model Scores and save
    pre_ac_record.learning_strategy = data['learning_strategy']
    pre_ac_record.goal_setting = data['goal_setting']
    pre_ac_record.organising = data['organising']
    pre_ac_record.motivation_and_accountability = data['motivation_and_accountability']
    pre_ac_record.time_management = data['time_management']
    pre_ac_record.life_balance = data['life_balance']
    pre_ac_record.save()

    return Response(status=status.HTTP_200_OK)


# API endpoint for deleting a goal, task, eca, qualification, or study method
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def handle_delete(request):
    # Retrieve student information and section details from request data
    student_id = request.data.get('student_id')
    section = request.data.get('section')
    id = request.data.get('id')

    # Check if student exists
    if not User.objects.filter(id=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    student = User.objects.get(id=student_id)

    # Perform deletion based on section
    if section == 'goal':
        goal_delete(id, student)
    elif section == 'task':
        task_delete(id, student)
    elif section == 'eca':
        eca_delete(id, student)
    elif section == 'qualification':
        qualification_delete(id, student)
    # elif section == 'study_method':
    #     study_method_delete(id, student)

    return Response(status=status.HTTP_200_OK)


# API endpoint for signing out
@api_view(['GET'])
@permission_classes([AllowAny])
def signout(request):
    # Logout the user and flush session data
    logout(request)
    request.session.flush()
    
    return Response(status=status.HTTP_204_NO_CONTENT)
    


### Helper functions ###

# The function used to evaluate subgoals once a goal is evaluated
def evaluate_sub_goal(goal_id, student_id, evaluation):
    goal=Goal.objects.filter(id=goal_id, goal_status="on going", student_id=student_id)
    if goal.exists():
        for subgoal in Goal.objects.filter(parent_id=goal_id):
            evaluate_sub_goal(subgoal.id, student_id, evaluation)
            subgoal.goal_status = evaluation['status']
            subgoal.final_result = evaluation['final_result']
            subgoal.end_at = datetime.now()
            subgoal.save()

# The function used to evaluate subtasks once a task is evaluated
def evaluate_sub_task(task_id, student_id, evaluation):
    task=Task.objects.filter(id=task_id, status="on going", student_id=student_id)
    if task.exists():
            sub_task_id = TaskTaskMapping.objects.filter(parent_task_id=task_id).values('child_task_id')
            for subtask in Task.objects.filter(id__in=sub_task_id):
                evaluate_sub_task(subtask.id, student_id, evaluation)
                subtask.status = evaluation['status']
                subtask.completeness = evaluation['completeness']
                subtask.end_at = datetime.now()
                subtask.save()

# The function used to get the list of comments for a type of model (S&C/AC) in the final report
def get_comments(queryset, comment_type):
    column_map = COMMENT_LIST_DICT
    comment_list = {}
    choice_list = {}
    columns = column_map.get(comment_type, [])
    
    # Retrieve all rows with relevant columns in one query
    data = queryset.values(*columns)
    for column in columns:
        comments = [item[column] for item in data if item[column] not in (None, '')]
        comment_list[column] = comments
        choice_list[column] = [(i, v) for i, v in enumerate(comments)]
    return comment_list, choice_list

# The function used to delete a goal
def goal_delete(goal_id, student):
    goal=Goal.objects.filter(id=goal_id, goal_status="on going", student_id=student.id)
    if goal.exists():
        for subgoal in Goal.objects.filter(parent_id=goal_id):
            goal_delete(subgoal.id, student)
        # if StudentMethodMapping.objects.filter(related_goal_id=goal_id).exists():
        #     method_list = StudentMethodMapping.objects.filter(related_goal_id=goal_id)
        #     for method in method_list:
        #         method.related_goal = None
        #         method.save()
        if TaskGoalMapping.objects.filter(goal_id=goal_id).exists():
            TaskGoalMapping.objects.filter(goal_id=goal_id).delete()
        
        Goal.objects.get(id=goal_id).delete()
    return True

# The function used to delete a task
def task_delete(task_id, student):
    task=Task.objects.filter(id=task_id, status="on going", student_id=student.id)
    if task.exists():
        sub_task_id = TaskTaskMapping.objects.filter(parent_task_id=task_id).values('child_task_id')
        for subtask in Task.objects.filter(id__in=sub_task_id):
            task_delete(subtask.id, student)
        TaskGoalMapping.objects.filter(task_id=task_id).delete()
        # TaskMethodMapping.objects.filter(task_id=task_id).delete()
        TaskTaskMapping.objects.filter(child_task=task_id).delete()
        TaskTaskMapping.objects.filter(parent_task=task_id).delete()
        TaskSubjectMapping.objects.filter(task_id=task_id).delete()         
        Task.objects.filter(id=task_id).delete()
    return True

# The function used to delete a eca
def eca_delete(eca_id, student):
    if UserEca.objects.filter(eca=eca_id, user_id=student.id).exists():
        user_eca = UserEca.objects.filter(eca=eca_id)
        user_eca.delete()
    return True

# The function used to delete a qualification
def qualification_delete(qualification_id, student):
    if UserQualification.objects.filter(qualification=qualification_id, user_id=student.id).exists():
        user_qualification = UserQualification.objects.filter(qualification=qualification_id)
        user_qualification.delete()
    return True

# The function used to delete a study method
# def study_method_delete(method_id, student):
#     if StudentMethodMapping.objects.filter(student_id=student.id, id=method_id, status="on going").exists():
#         StudentMethodSubjectMapping.objects.filter(student_method_mapping_id=method_id).delete()
#         TaskMethodMapping.objects.filter(student_method_mapping_id=method_id).delete()
#         StudentMethodMapping.objects.filter(id=method_id).delete()
#     return redirect('study_method')

# The function used to get the current/selected student
def get_student(request):
    # get the user object for the current user
    user = User.objects.get(username=request.user.username)

    # get the role for the current user
    role = user.role
    # if the current user is a superuser, set the role to 'coach'
    if request.user.is_superuser:
        role = 'coach'

    # if the current user is a coach, get the student they are viewing
    if role == 'coach':
        student_id = request.data.get('student_id')
        if User.objects.filter(id = student_id).exists():
            student = User.objects.filter(id = student_id)[0]
        else:
            student = User.objects.last()
    else:
        # get the student object for the current user
        student = user

    return student

# The function used to get the coach for the current user
def get_coach(request):
    user = User.objects.get(username=request.user.username)
    role = user.role
    if request.user.is_superuser or role == 'coach':
        coach = user
    else:
        if CoachStudentMapping.objects.filter(student_id=user.id).exists():
            coach = User.objects.get(
                id=CoachStudentMapping.objects.get(student_id=user.id).coach_id
            )
        else:
            coach = None

    return coach

# The function used to get the Chinese translation of the goal types (for display)
def get_goal_type_chin(goal_type_list):
    goal_type_dict = {"interest": "興趣", "academic": "學業", "career": "事業", "wellbeing": "健康"}
    if type(goal_type_list) == list:
        for goal_type in goal_type_list:
            goal_type = goal_type_dict[goal_type]
    else:
        goal_type_list = goal_type_dict[goal_type_list]
    return goal_type_list

# The function used to get the Chinese translation of the goal difficulties (for display)
def get_difficulty_chin(difficulty_list):
    difficulty_dict = {"easy": "容易", "moderate": "合適", "ambitious": "有挑戰性"}
    if type(difficulty_list) == list:
        for difficulty in difficulty_list:
            difficulty = difficulty_dict[difficulty]
    else:
        difficulty_list = difficulty_dict[difficulty_list]
    return difficulty_list

# The function used to get the Chinese translation of the model (for display)
def get_model_chin(model_type, model_list):
    if model_type == 's_and_c':
        model_dict = {s_and_c: MODEL_DICT_CHIN[model_type][i] for i, s_and_c in enumerate(MODEL_DICT[model_type])}
    elif model_type == 'ac':
        model_dict = {ac: MODEL_DICT_CHIN[model_type][i] for i, ac in enumerate(MODEL_DICT[model_type])}
    if type(model_list) == list:
        for model in model_list:
            model = model_dict[model]
    else:
        model_list = model_dict[model_list]
    return model_list

# The function used to get the model scores (S&C/AC) for a student
def get_model_score(model_type, area, student):
    column_map = MODEL_SCORE_DICT
    reports = CoachingReportRecord.objects.filter(student_id=student.id, phase=student.phase)

    model_data = SAndCRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports) if model_type == 's_and_c' else AcademicCoachingRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports) if model_type == 'ac' else None

    column_list = [*column_map[model_type][area]]
    scores_list = {}
    data = model_data.values('coaching_report_record', *column_list)

    for column in column_map[model_type][area]:
        scores = [(reports.filter(id=item['coaching_report_record'])[0], item[column]) for item in data if item[column] not in (None, '')]
        scores_list[column] = scores

    displayed = []
    for key in scores_list:
        if len(scores_list[key])!=0:
            average = sum([item[1] for item in scores_list[key]])/len(scores_list[key])
        else:
            average = 0
        displayed_scores = [f"Section-{item[0].section}: {item[1]}" for item in scores_list[key]]
        displayed.append((key, f"AVG: {average} | "+ " ; ".join(displayed_scores)))
    return displayed

# The function used to get the overall model scores (S&C and AC) for a student in the final report
def get_model_list(model_type, report_dashboard):
    model_list = []
    model_scores = []
    if model_type == 's_and_c' or model_type == 'ac':
        for model_area in MODEL_DICT[model_type]:
            if model_type == 'ac':
                display_score = get_model_score(model_type, model_area, report_dashboard.student)
                model_scores.append(display_score)
            score = getattr(report_dashboard, f"{model_area}_score")
            comment = getattr(report_dashboard, f"{model_area}_comment")
            if score == None:
                score = 0
            if comment == None:
                comment = ""
            model_list.append((model_area, get_model_chin(model_type, model_area), score, comment))
    return model_list, model_scores

# The function used to get the list of model scores (all areas in S&C/AC) for a student in the final report
def get_detail_score(model_area, model_type, report):
    student = User.objects.get(id=report.student_id)
    scores = []
    last_name = student.name_chinese[0]
    if len(student.name_chinese) == 4:
        last_name = f"{student.name_chinese[0:2]}"
    scores.append(last_name+'同學')
    if model_type == 's_and_c' or model_type == 'ac':
        scores.append(model_area)
        for area in MODEL_SCORE_DICT[model_type][model_area]:
            if getattr(report, area) == None:
                return "not enough data"
            scores.append(getattr(report, area))
        return scores
    elif model_type == 'social_style':
        scores.append(report.social_style_type)
        if UserSocialStyle.objects.filter(id=report.after_social_style_id).exists():
            user_social_style = UserSocialStyle.objects.get(id=report.after_social_style_id)
            scores += [user_social_style.analytical, user_social_style.amiable, user_social_style.expressive, user_social_style.driver]
            return scores
        return "not enough data"
    elif model_type == 'general':
        return scores.append(model_type)
    return "incorrect model type"

# The function used to set the model scores and comments in the final report
def set_model_score(model_type, report_dashboard, report):
    if model_type == 's_and_c' or model_type == 'ac':
        for model_area in MODEL_DICT[model_type]:
            scores = []
            for area in MODEL_SCORE_DICT[model_type][model_area]:
                if (report[area] != -1):
                    scores.append(report[area] + 1)
                    setattr(report_dashboard, area, report[area] + 1)
                else:
                    setattr(report_dashboard, area, None)
            if len(scores) != 0:
                score = int(round(sum(scores)/len(scores),0))
                setattr(report_dashboard, f"{model_area}_score", score)
            setattr(report_dashboard, f"{model_area}_comment", report[f"{model_area}_comment"])

# The function used to get all the goals of a student, isFinal returns all the goals if True, else only the ongoing goals
def get_goals(student, isFinal):
    if isFinal:
        goals = Goal.objects.filter(student_id=student.id)
    else:
        goals = Goal.objects.filter(student_id=student.id, goal_status='on going')
    goals = sorted(goals, key=attrgetter('predicted_end_time'))
    goal_serializer = GoalSerializer(goals, many=True)
    for goal in goal_serializer.data:
        goal['progress'] = GoalEvaluate.objects.filter(goal_id=goal['id']).last().progress if GoalEvaluate.objects.filter(goal_id=goal['id']).exists() else 0
        
        goal['parent'] = GoalSerializer(Goal.objects.get(id=goal['parent']),many=False).data if goal['parent'] is not None else None
        goal['display_difficulty'] = get_difficulty_chin(goal['difficulty'])
        goal['display_goal_type'] = get_goal_type_chin(goal['goal_type'])

        goal['goal_evaluate'] = GoalEvaluateSerializer(GoalEvaluate.objects.filter(goal_id=goal['id']).last(), many=False).data if GoalEvaluate.objects.filter(goal_id=goal['id']).exists() else None

    
    return goal_serializer.data

# The function used to get all the tasks of a student, isFinal returns all the tasks if True, else only the ongoing tasks
def get_tasks(student, isFinal):
    if isFinal:
        tasks = Task.objects.filter(student_id=student.id)
    else:
        tasks = Task.objects.filter(student_id=student.id, status="on going")
    task_serializer = TaskSerializer(tasks, many=True)
    for task in task_serializer.data:
        parent_tasks_id = TaskTaskMapping.objects.filter(child_task=task['id']).values_list('parent_task', flat=True)
        parent_tasks = Task.objects.filter(id__in=parent_tasks_id)
        parent_tasks_serializer = TaskSerializer(parent_tasks, many=True)
        
        parent_goal_id = TaskGoalMapping.objects.filter(task_id=task['id']).values_list('goal_id', flat=True)
        parent_goals = Goal.objects.filter(id__in=parent_goal_id)
        parent_goals_serializer = GoalSerializer(parent_goals, many=True)
        
        # parent_method_id = TaskMethodMapping.objects.filter(task_id=task['id']).values_list('student_method_mapping_id', flat=True)
        # parent_methods = StudentMethodMapping.objects.filter(id__in=parent_method_id)
        # parent_methods_serializer = MethodSerializer(parent_methods, many=True)
        
        
        subject_id_list = TaskSubjectMapping.objects.filter(task_id=task['id']).values_list('subject_id', flat=True)
        subject_list = Subject.objects.filter(id__in=subject_id_list)
        subject_serializer = SubjectSerializer(subject_list, many=True)
        
        task['subject']=subject_serializer.data
        task['goals'] = parent_goals_serializer.data
        # task['methods'] = parent_methods_serializer.data
        task['tasks'] = parent_tasks_serializer.data
    return task_serializer.data

# The function used to get all the subjects of a student
def get_subjects(student):
    subject_id_list = UserSubjectList.objects.filter(
        user_id=student.id).values_list('subject_id', flat=True)
    subjects = Subject.objects.filter(
        id__in=subject_id_list)
    subject_serializer = SubjectSerializer(subjects, many=True)
    for subject in subject_serializer.data:
        subject['display_name'] = f"{subject['name_abbr']} - {subject['name_chin']}"
    return subject_serializer.data





### The following are the API that are not used in V2 ###

"""
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([SessionAuthentication]) 
def signup(request):
    sign_up_form = UserCreationForm(request.data)
    user_info_form = forms.UserInfoForm(request.data)
    if (not sign_up_form.is_valid()) or (not user_info_form.is_valid()):
        # Render signup form with errors
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    sign_up_form.save()
    username = sign_up_form.cleaned_data.get('username')
    password = sign_up_form.cleaned_data.get('password1')
    user = authenticate(username=username, password=password)

    login(request, user)
    
    new_user = User()
    new_user.username = username
    new_user.name = user_info_form.cleaned_data['name']
    new_user.name_chinese = user_info_form.cleaned_data['name_chinese']
    new_user.email = user_info_form.cleaned_data['email']
    new_user.role = 'student'
    new_user.save()
    # Redirect to subject record after successful signup
    return Response(status=status.HTTP_201_CREATED)
"""

    
"""
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication]) 
def add_method(request):    
    student = get_student(request)
    if student is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    method_id = int(request.data.get['method_id'])
    if method_id != 0 and StudentMethodMapping.objects.filter(student_id=student.id, method_id=method_id, status="ongoing").exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)    
    student_method_mapping = StudentMethodMapping()
    student_method_mapping.student_id = student.id
    student_method_mapping.method_id = method_id
    if int(request.data.get['goal']) != 0:
        student_method_mapping.related_goal_id = int(request.data.get['goal'])
    student_method_mapping.personalization = request.data.get['personalization']
    student_method_mapping.status = "on going"
    # student_method_mapping.name = method.name_chin
    # student_method_mapping.description = method.description_chin
    student_method_mapping.save()
    return Response(status=status.HTTP_201_CREATED)
"""

"""
# View function for user profile
@api_view(['GET', 'POST'])
def profile(request):
    user = User.objects.get(username=request.user.username)
    role = user.role
    coach = get_coach(request)
    
    coach_button_list = [
        {'name': 'Coaching Report', 'url': '../coaching_report_entry'},
    ]

    coach_as_student_button_list = [
        {'name': 'Social Style Score', 'url': '../social_style_score'},
        {'name': 'Reset to Original View', 'url': '../reset_coach_as_student'}

    ]

    student_button_list = [
        {'name': 'Social Style Questionnaire', 'url': '../social_style'},
        {'name': 'Goal', 'url': '../goal'},
        {'name': 'Task', 'url': '../task'},
        {'name': 'Study Method', 'url': '../study_method'},
        {'name': 'ECA', 'url': '../eca'},
        {'name': 'Qualification', 'url': '../qualification'},
        {'name': 'Subject Grade', 'url': '../subject_grade'},
        
    ]
    student = get_student(request)
    if student is not None:
        if role == 'coach' or CoachStudentMapping.objects.filter(student_id=student.id).exists():
            student_button_list.append({'name': 'Final Evaluation', 'url': '../final_evaluation'})

    admin_button_list = [
        {'name': 'User Role', 'url': '../user_role'},
        {'name': 'Coach Student Select', 'url': '../coach_student_select'},
        {'name': 'Coaching Report', 'url': '../coaching_report_entry'},
    ]
    
    personal_info_button_list = [
        {'name': 'Edit Personal Info', 'url': '../edit_personal_info'},
        {'name': 'Change Password', 'url': '../change_password'},
    ]

    button_list = []


    # change coach to student they selected in the student form
    if request.method == 'POST':
        student_form = StudentForm(request.data)
        
        if student_form.is_valid():
            request.session['coach_as_student'] = student_form.cleaned_data['student']

            
            return Response({
                'button_list': coach_as_student_button_list + student_button_list,
                'role': role,
                'coach': coach,
            })
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # student look of the profile page
    if user.role == 'student':
        
        
        
        button_list = student_button_list + personal_info_button_list


        return Response({
            'button_list': button_list,
            'role': role,
        })
        

    # coach look of the profile page when they are looking at a student
    if request.session['coach_as_student'] != -1:
        button_list = coach_as_student_button_list + student_button_list

        
        return Response({
            'button_list': button_list,
            'role': role,
            'coach': coach,
        })

    # admin look of the profile page
    if request.user.is_superuser:
        button_list = admin_button_list + personal_info_button_list + coach_button_list

        
        return Response({
            'button_list': button_list,
            'role': role,
        })

    # coach look of the profile page when they are not looking at a student
    if user.role == 'coach':
        button_list = coach_button_list + personal_info_button_list


        return Response({
            'button_list': button_list,
            'role': role,
        })


"""

"""
def get_methods(student):
    methods = StudentMethodMapping.objects.filter(
        student_id=student.id, status="on going")
    method_serializer = StudentMethodMappingSerializer(methods, many=True)
    for method in method_serializer.data:
        method_subject_list = StudentMethodSubjectMapping.objects.filter(student_method_mapping_id=method['id']).values_list('subject_id', flat=True)
        method['subject'] = SubjectSerializer(Subject.objects.filter(id__in=method_subject_list), many=True).data
    return method_serializer.data
"""
