from datetime import datetime
from django.db.models import Q, Exists, OuterRef
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User as AuthUser
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . import forms
from coaching.models import *
from operator import attrgetter
from .gpt_gen import *

S_AND_C = ['critical_thinking', 'problem_solving', 'managing_information', 'creativity_and_innovation', 'communication', 'collaboration', 'cultural_and_global_citizenship', 'personal_growth_and_wellbeing']

S_AND_C_CHIN = ['批判性思維', '解決問題', '管理資訊', '創意與創新', '表達與溝通', '團隊合作', '文化和全球公民意識', '個人成長']

AC = ['learning_strategy', 'goal_setting', 'organising', 'motivation_and_accountability', 'time_management', 'life_balance']

AC_CHIN = ['學習策略', '目標設定', '組織管理', '動機與責任', '時間管理', '生活平衡']

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


COMMENT_LIST_DICT = {'s_and_c': ['critical_thinking_comment', 'problem_solving_comment', 'managing_information_comment',                'creativity_and_innovation_comment', 'communication_comment', 'collaboration_comment',                 'cultural_and_global_citizenship_comment', 'personal_growth_and_wellbeing_comment'], 'ac': ['learning_strategy_comment', 'goal_setting_comment', 'organising_comment', 'motivation_and_accountability_comment', 'time_management_comment', 'life_balance_comment'], 'report': ['comment']}


# View function for user signup
def signup(request):
    if not request.method == 'POST':
        sign_up_form = UserCreationForm()
        user_info_form = forms.UserInfoForm()
        # Render signup form
        return render(request, 'signup.html', {'sign_up_form': sign_up_form, 'user_info_form': user_info_form})

    sign_up_form = UserCreationForm(request.POST)
    user_info_form = forms.UserInfoForm(request.POST)
    if (not sign_up_form.is_valid()) or (not user_info_form.is_valid()):
        # Render signup form with errors
        return render(request, 'signup.html', {'sign_up_form': sign_up_form, 'user_info_form': user_info_form})

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
    return redirect('user_subject_record')


# View function for user login
def signin(request):
    if request.user.is_authenticated:
        # Redirect to home if user is already authenticated
        return render(request, 'profile.html')

    if not request.method == 'POST':
        form = AuthenticationForm()
        # Render login form
        return render(request, 'login.html', {'form': form})

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        msg = 'Error Login'
        form = AuthenticationForm(request.POST)
        # Render login form with error message
        return render(request, 'login.html', {'form': form, 'msg': msg})

    login(request, user)
    if User.objects.get(username=request.user.username).role == 'coach' or user.is_superuser:
        request.session['coach_as_student'] = -1
    return redirect('profile')  # Redirect to profile after successful login


# View function for user profile
@login_required(login_url='signin')
def profile(request):

    role, student_form, user, student, coach = get_student_form(request)

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
    ]
    
    personal_info_button_list = [
        {'name': 'Edit Personal Info', 'url': '../edit_personal_info'},
        {'name': 'Change Password', 'url': '../change_password'},
    ]

    button_list = []

    # button_list = [
    #     {'name': 'Social Style Questionnaire', 'url': '../social_style'},
    #     {'name': 'Social Style Score', 'url': '../social_style_score'},
    #     {'name': 'Goal', 'url': '../goal'},
    #     {'name': 'Task', 'url': '../task'},
    #     {'name': 'Coaching Report', 'url': '../coaching_report_entry'},
    #     {'name': 'Final Evaluation', 'url': '../final_evaluation'},
    #     {'name': 'Edit Personal Info', 'url': '../edit_personal_info'},
    #     {'name': 'Change Password', 'url': '../change_password'},
    #     {'name': 'ECA', 'url': '../eca'},
    #     {'name': 'Subject Grade', 'url': '../subject_grade'},
    # ]

    # change coach to student they selected in the student form
    if request.method == 'POST':
        if student_form.is_valid():
            request.session['coach_as_student'] = student_form.cleaned_data['student']
            return redirect('profile')

    # student look of the profile page
    if user.role == 'student':
        button_list = student_button_list + personal_info_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role})
    
    # admin look of the profile page
    if request.user.is_superuser and request.session['coach_as_student'] == -1:
        button_list = admin_button_list + coach_button_list + personal_info_button_list 

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form})
    elif request.user.is_superuser and request.session['coach_as_student'] != -1:
        button_list = coach_as_student_button_list + student_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form, 'student': student, 'coach': coach})

    # coach look of the profile page when they are looking at a student
    if request.session['coach_as_student'] != -1:
        button_list = coach_as_student_button_list + student_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form, 'student': student, 'coach': coach})

    # coach look of the profile page when they are not looking at a student
    if user.role == 'coach':
        button_list = coach_button_list + personal_info_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form})
    

# reset the coach as student session variable
@login_required(login_url='signin')
def reset_coach_as_student(request):
    if request.user.is_superuser or User.objects.get(username=request.user.username).role == 'coach':
        request.session['coach_as_student'] = -1
    return redirect('profile')


# View function for user logout
def signout(request):
    logout(request)
    return redirect('profile')  # Redirect to profile after logout


# View function for user record creation
@login_required(login_url='signin')
def user_subject_record(request):

    if not request.method == 'POST':
        form = forms.SubjectForm()
        # Render user record form
        return render(request, 'user_subject_record.html', {'form': form})

    form = forms.SubjectForm(request.POST)

    if not form.is_valid():
        # Render user record form with errors
        return render(request, 'user_subject_record.html', {'form': form})
    selected_options = form.cleaned_data['choices']

    for option in range(1, 5):
        new_user_subject_list = UserSubjectList()
        new_user_subject_list.user_id = User.objects.get(
            username=request.user.username).id
        new_user_subject_list.subject_id = option
        new_user_subject_list.save()

    for option in selected_options:
        new_user_subject_list = UserSubjectList()
        new_user_subject_list.user_id = User.objects.get(
            username=request.user.username).id
        new_user_subject_list.subject_id = option
        new_user_subject_list.save()

    # Redirect to profile after successful user record creation
    return redirect('student_pre_assessment')


# View function for social style questionnaire
@login_required(login_url='signin')
def social_style(request):

    student = get_student(request)
    social_style_score = UserSocialStyle.objects.filter(user_id=student.id).last()

    option_mapping = {
        '1': '分析型',
        '2': '友善型',
        '3': '表達型',
        '4': '推動型',
    }
    # Render social style questionnaire form
    if not request.method == 'POST':
        form = forms.SocialStyleForm()
        return render(request, 'social_style.html', {'form': form, 'social_style_score': social_style_score})

    form = forms.SocialStyleForm(request.POST)

    if not form.is_valid():
        return render(request, 'social_style.html', {'form': form, 'social_style_score': social_style_score})

    selected_options = form.cleaned_data.values()
    option_counts = {option: 0 for option in option_mapping.values()}

    for option in selected_options:
        option_text = option_mapping.get(option)
        if option_text:
            option_counts[option_text] += 1
    for option in option_counts:
        option_counts[option] *= 5

    new_user_social_style = UserSocialStyle()

    new_user_social_style.user_id = student.id

    new_user_social_style.driver = option_counts['推動型']
    new_user_social_style.amiable = option_counts['友善型']
    new_user_social_style.analytical = option_counts['分析型']
    new_user_social_style.expressive = option_counts['表達型']
    new_user_social_style.save()

    # Render result with option counts
    return render(request, 'count.html', {'option_counts': option_counts})


@login_required(login_url='signin')
def social_style_score(request):
    student = get_student(request)
    social_style_score = UserSocialStyle.objects.filter(user_id=student.id).last()

    # Render social style questionnaire form
    if not request.method == 'POST':
        form = forms.SocialStyleScoreForm()
        return render(request, 'social_style_score.html', {'form': form, 'social_style_score': social_style_score})

    form = forms.SocialStyleScoreForm(request.POST)

    if not form.is_valid():
        return render(request, 'social_style_score.html', {'form': form, 'social_style_score': social_style_score})

    new_user_social_style = UserSocialStyle()
    new_user_social_style.user_id = student.id
    new_user_social_style.driver = form.cleaned_data['driver']
    new_user_social_style.amiable = form.cleaned_data['amiable']
    new_user_social_style.analytical = form.cleaned_data['analytic']
    new_user_social_style.expressive = form.cleaned_data['expressive']
    new_user_social_style.save()

    # Render result with option counts
    return render(request, 'count.html', {'option_counts': form.cleaned_data})


@login_required(login_url='signin')
def student_pre_assessment(request):
    student = get_student(request)

    if not request.method == 'POST':
        form = forms.StudentPreAssessmentForm()
        # Render student pre-assessment form
        return render(request, 'student_pre_assessment.html', {'form': form})
    form = forms.StudentPreAssessmentForm(request.POST)
    if not form.is_valid():
        # Render student pre-assessment form with errors
        return render(request, 'student_pre_assessment.html', {'form': form})
    new_student_pre_assessment = StudentPreAssessment()
    new_student_pre_assessment.student_id = student.id
    new_student_pre_assessment.long_term_goal = form.cleaned_data['long_term_goal']
    new_student_pre_assessment.area_to_improve = form.cleaned_data['area_to_improve']
    new_student_pre_assessment.interested_question = form.cleaned_data['interested_question']
    new_student_pre_assessment.preferable_time_1 = datetime.combine(
        form.cleaned_data['preferable_time_1_date'], form.cleaned_data['preferable_time_1_time'])
    if form.cleaned_data['preferable_time_2_date'] and form.cleaned_data['preferable_time_2_time']:
        new_student_pre_assessment.preferable_time_2 = datetime.combine(
            form.cleaned_data['preferable_time_2_date'], form.cleaned_data['preferable_time_2_time'])
    if form.cleaned_data['preferable_time_3_date'] and form.cleaned_data['preferable_time_3_time']:
        new_student_pre_assessment.preferable_time_3 = datetime.combine(
            form.cleaned_data['preferable_time_3_date'], form.cleaned_data['preferable_time_3_time'])
    new_student_pre_assessment.save()
    # Redirect to profile after successful student pre-assessment creation
    return redirect('profile')


@login_required(login_url='signin')
def goal(request):
    student = get_student(request)

    goal_list = []
    if Goal.objects.filter(student_id=student.id).exists():
        goal_list = Goal.objects.filter(
            student_id=student.id, goal_status='on going')
    goals = []
    if goal_list:
        for goal in goal_list:
            goals.append((goal.id, goal.name))
            goal.display_difficulty = get_difficulty_chin(goal.difficulty)
            goal.display_goal_type = get_goal_type_chin(goal.goal_type)
        goal_list = sorted(goal_list, key=attrgetter('predicted_end_time'))
    goals.insert(0,(0,'沒有所屬目標'))
    if not request.method == 'POST':
        form = forms.GoalForm(goals=goals)
        # Render student pre-assessment form
        return render(request, 'goal.html', {'form': form, 'goal_list': goal_list})
    form = forms.GoalForm(goals=goals,data=request.POST)
    if not form.is_valid():
        # Render student pre-assessment form with errors
        return render(request, 'goal.html', {'form': form, 'goal_list': goal_list})
    new_goal = Goal()
    new_goal.student_id = student.id
    new_goal.goal_type = form.cleaned_data['goal_type']
    new_goal.difficulty = form.cleaned_data['difficulty']
    new_goal.description = form.cleaned_data['description']
    new_goal.predicted_end_time = form.cleaned_data['predicted_end_time']
    new_goal.name = form.cleaned_data['name']
    new_goal.goal_status = 'on going'
    goal_parent_id = int(form.cleaned_data['goal'])
    if goal_parent_id!=0:
        new_goal.parent_id = goal_parent_id
        new_goal.is_subgoal = 1
    else:
        new_goal.is_subgoal = 0
    new_goal.save()
    return redirect('goal')


@login_required(login_url='signin')
def goal_delete_page(request):
    student = get_student(request)
    goal_list = []
    if Goal.objects.filter(student_id=student.id, goal_status = "on going").exists():
        goal_list = Goal.objects.filter(
            student_id=student.id, goal_status = "on going")
    if goal_list:
        for goal in goal_list:
            goal.display_difficulty = get_difficulty_chin(goal.difficulty)
            goal.display_goal_type = get_goal_type_chin(goal.goal_type)
    return render(request, 'goal_delete_page.html', {'goal_list': goal_list})


@login_required(login_url='signin')
def goal_delete(request, goal_id):
    student = get_student(request)
    goal=Goal.objects.filter(id=goal_id, goal_status="on going", student_id=student.id)
    if goal.exists():
        for subgoal in Goal.objects.filter(parent_id=goal_id):
            goal_delete(request, subgoal.id)
        if StudentMethodMapping.objects.filter(related_goal_id=goal_id).exists():
            method_list = StudentMethodMapping.objects.filter(related_goal_id=goal_id)
            for method in method_list:
                method.related_goal = None
                method.save()
        if TaskGoalMapping.objects.filter(goal_id=goal_id).exists():
            TaskGoalMapping.objects.filter(goal_id=goal_id).delete()
        
        Goal.objects.get(id=goal_id).delete()
    return redirect('goal')


@login_required(login_url='signin')
def goal_evaluation(request, goal_id):
    student = get_student(request)
    if not Goal.objects.filter(id=goal_id, student_id=student.id, goal_status="on going").exists():
        return redirect('goal')
    
    goal = Goal.objects.get(id=goal_id)
    goal.display_difficulty = get_difficulty_chin(goal.difficulty)
    goal.display_goal_type = get_goal_type_chin(goal.goal_type)
    if not request.method == 'POST':
        form = forms.GoalEvaluationForm()
        return render(request, 'goal_evaluation.html', {'form': form, 'goal': goal})
    form = forms.GoalEvaluationForm(request.POST)
    if not form.is_valid():
        return render(request, 'goal_evaluation.html', {'form': form, 'goal': goal})
    goal_evaluation = forms.GoalEvaluationForm()
    goal_evaluation.effort = form.cleaned_data['effort']
    goal_evaluation.progress = form.cleaned_data['progress']
    goal_evaluation.comment = form.cleaned_data['comment']
    goal_evaluation.goal_id = goal_id
    goal.goal_status = form.cleaned_data['status']
    goal.final_result = form.cleaned_data['final_result']
    goal.end_at = datetime.now()

    def evaluate_sub_goal(request, goal_id, student_id):
        goal=Goal.objects.filter(id=goal_id, goal_status="on going", student_id=student_id)
        if goal.exists():
            for subgoal in Goal.objects.filter(parent_id=goal_id):
                evaluate_sub_goal(request, subgoal.id, student_id)
                subgoal.goal_status = form.cleaned_data['status']
                subgoal.final_result = form.cleaned_data['final_result']
                subgoal.end_at = datetime.now()
                subgoal.save()

    evaluate_sub_goal(request, goal_id, student.id)
    goal.save()

    return redirect('goal')


@login_required(login_url='signin')
def home(request):

    return redirect('profile')


@login_required(login_url='signin')
def task(request):
    student = get_student(request)

    # ******************** Task Form*************************#
    # subject list generation for task form
    subject_id_list = UserSubjectList.objects.filter(
        user_id=student.id).values_list('subject_id', flat=True)
    subjects = Subject.objects.filter(
        id__in=subject_id_list).values('id', 'name_abbr', 'name_chin')
    subjects_list = [
        (subject['id'], f"{subject['name_abbr']} - {subject['name_chin']}") for subject in subjects]

    # goal list generation for task form
    goals = Goal.objects.filter(student_id=student.id, goal_status='on going').values('id', 'name')
    if goals.exists():
        goals = [(goal['id'], goal['name']) for goal in goals]
    else:  
        goals = []

    # method list generation for task form
    methods = StudentMethodMapping.objects.filter(
        student_id=student.id, status="on going").values('id', 'name')
    if methods.exists():
        methods = [(method['id'], method['name']) for method in methods]
    else:
        methods = []

    # task list generation for task form
    tasks = Task.objects.filter(student_id=student.id, status = "on going").values('id', 'name')
    if tasks.exists():
        tasks = [(task['id'], task['name']) for task in tasks]
    else:
        tasks = []

    # subject name generation for task list
    task_list = Task.objects.filter(student_id=student.id, status = "on going")
    get_task_parents(task_list)

    task_list = sorted(task_list, key=attrgetter('predicted_end_time'))

    if not request.method == 'POST':
        form = forms.TaskForm(subjects=subjects_list,
                              goals=goals, methods=methods, tasks=tasks)
        return render(request, 'task.html', {'form': form, 'task_list': task_list})
    form = forms.TaskForm(subjects=subjects_list, goals=goals,
                          methods=methods, tasks=tasks, data=request.POST)
    if not form.is_valid():
        return render(request, 'task.html', {'form': form, 'task_list': task_list})

    # ******************** Task DB Entry*************************#
    new_task = Task()
    new_task.name = form.cleaned_data['name']
    new_task.student_id = student.id
    new_task.predicted_end_time = form.cleaned_data['predicted_end_time']
    new_task.description = form.cleaned_data['description']
    new_task.status = 'on going'
    new_task.priority = form.cleaned_data['priority']
    new_task.save()

    # ******************** Task Mapping DB Entry*************************#
    for subject in form.cleaned_data['subject']:
        new_task_subject_mapping = TaskSubjectMapping()
        new_task_subject_mapping.task_id = new_task.id
        new_task_subject_mapping.subject_id = subject
        new_task_subject_mapping.save()
    
    for goal in form.cleaned_data['goal']:
        new_task_goal_mapping = TaskGoalMapping()
        new_task_goal_mapping.task_id = new_task.id
        new_task_goal_mapping.goal_id = goal
        new_task_goal_mapping.save()

    for method in form.cleaned_data['method']:
        new_task_method_mapping = TaskMethodMapping()
        new_task_method_mapping.task_id = new_task.id
        new_task_method_mapping.student_method_mapping_id = method
        new_task_method_mapping.save()

    for task in form.cleaned_data['task']:
        new_task_task_mapping = TaskTaskMapping()
        new_task_task_mapping.child_task_id = new_task.id
        new_task_task_mapping.parent_task_id = task
        new_task_task_mapping.save()

    return redirect('task')


@login_required(login_url='signin')
def task_evaluation(request, task_id):
    student = get_student(request)

    if not Task.objects.filter(id=task_id, status = 'on going', student_id = student.id).exists():
        return redirect('task')
    
    task = Task.objects.get(id=task_id)
    get_task_parents([task])
    if not request.method == 'POST':
        form = forms.TaskEvaluationForm(initial={"priority":task.priority})
        return render(request, 'task_evaluation.html', {'form': form, 'task': task})
    form = forms.TaskEvaluationForm( initial={"priority":task.priority}, data=request.POST)
    if not form.is_valid():
        return render(request, 'task_evaluation.html', {'form': form, 'task': task})

    task.effort = form.cleaned_data['effort']
    task.effectiveness = form.cleaned_data['effectiveness']
    task.comment = form.cleaned_data['comment']
    task.willingness = form.cleaned_data['willingness']
    task.status = form.cleaned_data['status']
    task.completeness = form.cleaned_data['completeness']
    task.time_spent = form.cleaned_data['time_spent']
    task.priority = form.cleaned_data['priority']
    task.end_at = datetime.now()

    def evaluate_sub_task(request, task_id, student_id):
        task=Task.objects.filter(id=task_id, status="on going", student_id=student_id)
        if task.exists():
            sub_task_id = TaskTaskMapping.objects.filter(parent_task_id=task_id).values('child_task_id')
            for subtask in Task.objects.filter(id__in=sub_task_id):
                evaluate_sub_task(request, subtask.id, student_id)
                subtask.status = form.cleaned_data['status']
                subtask.completeness = form.cleaned_data['completeness']
                subtask.end_at = datetime.now()
                subtask.save()

    evaluate_sub_task(request, task_id, student.id)
    task.save()

    return redirect('task')


@login_required(login_url='signin')
def task_delete(request, task_id):
    student = get_student(request)
    task=Task.objects.filter(id=task_id, status="on going", student_id=student.id)
    if task.exists():
        sub_task_id = TaskTaskMapping.objects.filter(parent_task_id=task_id).values('child_task_id')
        for subtask in Task.objects.filter(id__in=sub_task_id):
            task_delete(request, subtask.id)
        TaskGoalMapping.objects.filter(task_id=task_id).delete()
        TaskMethodMapping.objects.filter(task_id=task_id).delete()
        TaskTaskMapping.objects.filter(child_task=task_id).delete()
        TaskTaskMapping.objects.filter(parent_task=task_id).delete()
        TaskSubjectMapping.objects.filter(task_id=task_id).delete()         
        Task.objects.filter(id=task_id).delete()
    return redirect('task')


@login_required(login_url='signin')
def task_delete_page(request):
    student = get_student(request)

    task_list = []
    if Task.objects.filter(student_id=student.id, status="on going").exists():
        task_list = Task.objects.filter(student_id=student.id, status="on going")
        get_task_parents(task_list)

    return render(request, 'task_delete_page.html', {'task_list': task_list})


@login_required(login_url='signin')
def coaching_report(request):

    coaching_report_id = request.session['coaching_report_id']
    
    form_instance = CoachingReportRecord.objects.get(
        id=coaching_report_id) if CoachingReportRecord.objects.filter(id=coaching_report_id).exists() else None
    
    if not request.method == 'POST':
        form = forms.CoachingReportForm(instance=form_instance)
        return render(request, 'coaching_report.html', {'form': form})
    form = forms.CoachingReportForm(request.POST, instance=form_instance)
    if not form.is_valid():
        return render(request, 'coaching_report.html', {'form': form})


    form.save()

    return redirect('coaching_report_landing')


@login_required(login_url='signin')
def coaching_report_entry(request):
    role, student_form, user, student, coach = get_student_form(request)

    if not request.method == 'POST':
        return render(request, 'coaching_report_entry.html', {'student_form': student_form})

    request.session['coaching_report_student_id']=student.id
    return redirect('coaching_report_landing')


@login_required(login_url='signin')
def coaching_report_landing(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_student_id'])
    coaching_report_list = CoachingReportRecord.objects.filter(
        student_id=request.session['coaching_report_student_id'], phase=student.phase).order_by('section')
    
    if coaching_report_list.exists():
        coaching_report_num = coaching_report_list.last().section+1
    else:
        coaching_report_num = coaching_report_list.count()+1

    if not request.method == 'POST':
        return render(request, 'coaching_report_landing.html', {'coaching_report_list': coaching_report_list, 'student': student})

    new_coaching_report = CoachingReportRecord()
    new_coaching_report.student_id = student.id
    new_coaching_report.coach_id = coach.id
    new_coaching_report.section = coaching_report_num
    new_coaching_report.phase = student.phase
    new_coaching_report.save()
    request.session['coaching_report_id'] = new_coaching_report.id
    return redirect('s_and_c_record')


@login_required(login_url='signin')
def coaching_report_edit(request,coaching_report_id):
    request.session['coaching_report_id'] = coaching_report_id
    return redirect('s_and_c_record')


@login_required(login_url='signin')
def s_and_c_record(request):
    coaching_report_id = request.session['coaching_report_id']

    form_instance = SAndCRecord.objects.get(
        coaching_report_record_id=coaching_report_id) if SAndCRecord.objects.filter(coaching_report_record_id=coaching_report_id).exists() else None

    if not request.method == 'POST':
        form = forms.SAndCRecordForm(instance=form_instance)
        return render(request, 's_and_c_record.html', {'form': form})

    form = forms.SAndCRecordForm(request.POST, instance=form_instance)

    if not form.is_valid():
        return render(request, 's_and_c_record.html', {'form': form})

    form.save(coaching_report_record=CoachingReportRecord.objects.get(id=coaching_report_id))
    return redirect('academic_coaching_record')


@login_required(login_url='signin')
def academic_coaching_record(request):
    coaching_report_id = request.session['coaching_report_id']
    form_instance = AcademicCoachingRecord.objects.get(
        coaching_report_record_id=coaching_report_id) if AcademicCoachingRecord.objects.filter(coaching_report_record_id=coaching_report_id).exists() else None

    last_record = None
    if not request.method == 'POST':
        form = forms.AcademicCoachingRecordForm(instance=form_instance)
        return render(request, 'academic_coaching_record.html', {'form': form, 'last_record': last_record})
    form = forms.AcademicCoachingRecordForm(request.POST, instance=form_instance)
    if not form.is_valid():
        return render(request, 'academic_coaching_record.html', {'form': form, 'last_record': last_record})
    form.save(coaching_report_record=CoachingReportRecord.objects.get(
        id=coaching_report_id))
    return redirect('coaching_report')


@login_required(login_url='signin')
def final_evaluation(request):
    student = get_student(request)
    coach = get_coach(request)

    form = forms.FinalEvaluationForm()
    if not request.method == 'POST':
        return render(request, 'final_evaluation.html', {'form': form, })
    form = forms.FinalEvaluationForm(request.POST)
    if not form.is_valid():
        return render(request, 'final_evaluation.html', {'form': form, })
    form.student_id = student.id
    form.coach_id = coach.id
    form.save()
    return redirect('profile')


@login_required(login_url='signin')
def edit_personal_info(request):

    user = User.objects.get(username=request.user.username)
    initial = {
        'name': user.name,
        'name_chinese': user.name_chinese,
        'email': user.email
    }
    if not request.method == 'POST':
        form = forms.UserInfoForm(initial=initial)
        return render(request, 'edit_personal_info.html', {'form': form})
    form = forms.UserInfoForm(request.POST)
    if not form.is_valid():
        return render(request, 'edit_personal_info.html', {'form': form})
    user.name = form.cleaned_data['name']
    user.name_chinese = form.cleaned_data['name_chinese']
    user.email = form.cleaned_data['email']
    user.save()
    return redirect('profile')


@login_required(login_url='signin')
def student_profile(request):

    form = UserChangeForm()
    return render(request, 'student_profile.html', {'form': form})


@login_required(login_url='signin')
def change_password(request):

    if not request.method == 'POST':
        form = forms.ChangePasswordForm(request.user)
        return render(request, 'change_password.html', {'form': form})
    form = forms.ChangePasswordForm(request.user, request.POST)
    if not form.is_valid():
        return render(request, 'change_password.html', {'form': form})

    user = form.save()
    update_session_auth_hash(request, user)
    return redirect('profile')


@login_required(login_url='signin')
def eca(request):
    student = get_student(request)

    # get eca names from user_eca table which links user and eca
    user_eca_list = UserEca.objects.filter(user_id = student.id).values('eca_id')
    eca_list = Eca.objects.filter(id__in=user_eca_list).order_by('name')
    eca_name_list = [eca.name for eca in eca_list]

    # All eca names from eca table except those in user_eca table
    eca_option_list = Eca.objects.exclude(
        name__in=eca_name_list).values('name')
    # Add others option to eca_option_list
    eca_option_list = list(eca_option_list)
    eca_option_list.insert(0, {'name': '其他課外活動'})
    # Turn eca_option_list into a form option list
    eca_option_list = [(eca['name'], eca['name']) for eca in eca_option_list]

    if not request.method == 'POST':
        form = forms.ECAForm(eca=eca_option_list)
        return render(request, 'eca.html', {'form': form, 'eca_list': eca_list})
    form = forms.ECAForm(data=request.POST, eca=eca_option_list)
    if not form.is_valid():
        return render(request, 'eca.html', {'form': form, 'eca_list': eca_list})
    user_eca = None

    if form.cleaned_data['eca'] == '其他課外活動' and form.cleaned_data['others'] != '':
        new_eca = Eca()
        new_eca.name = form.cleaned_data['others']
        new_eca.save()
        user_eca = new_eca
    elif form.cleaned_data['eca'] == '其他課外活動' and form.cleaned_data['others'] == '':
        return render(request, 'eca.html', {'form': form, 'eca_list': eca_list, 'msg': 'Please enter a valid ECA name'})
    else:
        user_eca = Eca.objects.get(name=form.cleaned_data['eca'])

    new_user_eca_mapping = UserEca()
    new_user_eca_mapping.user_id = student.id
    new_user_eca_mapping.eca_id = user_eca.id
    new_user_eca_mapping.save()
    return redirect('eca')


@login_required(login_url='signin')
def eca_delete(request, eca_id):
    student=get_student(request)

    if UserEca.objects.filter(eca=eca_id, user_id=student.id).exists():
        user_eca = UserEca.objects.filter(eca=eca_id)
        user_eca.delete()
    return redirect('eca')


@login_required(login_url='signin')
def qualification(request):
    student = get_student(request)

    # get eca names from user_eca table which links user and eca
    user_qualification_list = UserQualification.objects.filter(
        user_id=student.id).values('qualification_id')
    qualification_list = Qualification.objects.filter(
        id__in=user_qualification_list).order_by('name')
    qualification_name_list = [
        qualification.name for qualification in qualification_list]

    # All qualification names from qualification table except those in user_qualification table
    qualification_option_list = Qualification.objects.exclude(
        name__in=qualification_name_list).values('name')
    # Add others option to qualification_option_list
    qualification_option_list = list(qualification_option_list)
    qualification_option_list.insert(0, {'name': '其他資格'})
    # Turn qualification_option_list into a form option list
    qualification_option_list = [(qualification['name'], qualification['name']) for qualification in qualification_option_list]

    if not request.method == 'POST':
        form = forms.QualificationForm(qualification=qualification_option_list)
        return render(request, 'qualification.html', {'form': form, 'qualification_list': qualification_list})
    form = forms.QualificationForm(data=request.POST, qualification=qualification_option_list)
    if not form.is_valid():
        return render(request, 'qualification.html', {'form': form, 'qualification_list': qualification_list})
    user_qualification = None

    if form.cleaned_data['qualification'] == '其他資格' and form.cleaned_data['others'] != '':
        new_qualification = Qualification()
        new_qualification.name = form.cleaned_data['others']
        new_qualification.save()
        user_qualification = new_qualification
    elif form.cleaned_data['qualification'] == '其他資格' and form.cleaned_data['others'] == '':
        return render(request, 'qualification.html', {'form': form, 'qualification_list': qualification_list, 'msg': 'Please enter a valid QUALIFICATION name'})
    else:
        user_qualification = Qualification.objects.get(name=form.cleaned_data['qualification'])

    new_user_qualification_mapping = UserQualification()
    new_user_qualification_mapping.user_id = student.id
    new_user_qualification_mapping.qualification_id = user_qualification.id
    new_user_qualification_mapping.save()

    return redirect('qualification')


@login_required(login_url='signin')
def qualification_delete(request, qualification_id):
    student=get_student(request)

    if UserQualification.objects.filter(qualification=qualification_id, user_id=student.id).exists():
        user_qualification = UserQualification.objects.filter(qualification=qualification_id)
        user_qualification.delete()
    return redirect('qualification')


@login_required(login_url='signin')
def subject_grade(request):
    student = get_student(request)
    # Get a list of all the subjects the user has chosen
    subject_id_list = UserSubjectList.objects.filter(
        user_id=student.id).values_list('subject_id', flat=True)

    # Get the details of each subject the user has chosen
    subjects = Subject.objects.filter(
        id__in=subject_id_list).values('id', 'name_abbr', 'name_chin')

    # Create a list of all the subjects the user has chosen
    subjects_list = [
        (subject['id'], f"{subject['name_abbr']} - {subject['name_chin']}") for subject in subjects]
    subjects_list_dict = {subject[0]: subject[1] for subject in subjects_list} 
 
    # Get the last subject record of the user
    last_subject_record = None
    last_subject_grades = None
    if UserGradeRecord.objects.filter(user_id=student.id).exists():
        last_subject_record = UserGradeRecord.objects.filter(user_id=student.id).last() 
        last_subject_grades = UserSubjectGradeRecord.objects.filter(parent=last_subject_record.id).values_list('subject', 'grade') 
        last_subject_grades = [(subjects_list_dict[subject_grade[0]], subject_grade[1]) for subject_grade in last_subject_grades] 

    # If user has not submitted the form, create a new SubjectGradeForm and render the template
    if not request.method == 'POST':
        form = forms.SubjectGradeForm(subjects=subjects_list)
        return render(request, 'subject_grade.html', {'form': form,'last_subject_grades': last_subject_grades, 
                                                        'last_grade_date': last_subject_record})

    # If user has submitted the form, create a new SubjectGradeForm with the submitted form data
    form = forms.SubjectGradeForm(subjects=subjects_list, data=request.POST)

    # If the form is not valid, render the template with the form
    if not form.is_valid():
        return render(request, 'subject_grade.html', {'form': form,'last_subject_grades': last_subject_grades, 
                                                        'last_grade_date': last_subject_record})

    # Create a new UserGradeRecord
    new_user_grade = UserGradeRecord()
    new_user_grade.user_id = student.id
    new_user_grade.created_at = form.cleaned_data['record_date']
    new_user_grade.comment = form.cleaned_data['comment']
    new_user_grade.save()

    # Get the id of the new UserGradeRecord
    user_grade_id = UserGradeRecord.objects.get(id=new_user_grade.id)

    # Loop through each subject the user has chosen
    for subject in subjects_list:

        # If the user has not selected N/A for the subject, create a new UserSubjectGradeRecord
        if not (form.cleaned_data[subject[1]] == 'N/A'):
            new_subject_grade = UserSubjectGradeRecord()

            # Associate the new UserSubjectGradeRecord with the new UserGradeRecord
            new_subject_grade.parent = user_grade_id

            # Associate the new UserSubjectGradeRecord with the subject
            new_subject_grade.subject = Subject.objects.get(id=subject[0])

            # Set the grade of the new UserSubjectGradeRecord
            new_subject_grade.grade = form.cleaned_data[subject[1]]
            new_subject_grade.save()

    return redirect('subject_grade')


@login_required(login_url='signin')
def study_method(request):
    student = get_student(request)
    subject_id = MethodSubjectMapping.objects.values_list('subject_id', flat=True).distinct()
    subjects = Subject.objects.filter(id__in=subject_id).values('id', 'name_abbr', 'name_chin')
    subjects_list = [
        (subject['id'], f"{subject['name_abbr']} - {subject['name_chin']}") for subject in subjects]
    subjects_list.insert(0, (0,'全部科目'))
    focus_id = MethodFocusMapping.objects.values_list('focus_id', flat=True).distinct()
    focuses = Focus.objects.filter(id__in=focus_id).values('id', 'name_chin')
    focuses_list = [
        (focus['id'], focus['name_chin']) for focus in focuses]
    focuses_list.insert(0, (0,'全部學習重點'))
    student_methods_id = StudentMethodMapping.objects.filter(student_id=student.id, status="on going").values_list('method_id', flat=True)
    study_methods = Method.objects.exclude(id__in=student_methods_id)
    
    if student_methods_id.exists():
        student_methods = StudentMethodMapping.objects.filter(student_id=student.id, status="on going")
    else:
        student_methods = None
                
    # First, gather all method_ids
    method_ids = [method.id for method in study_methods]

    # Fetch MethodFocusMapping and MethodSubjectMapping data in bulk
    method_focus_mapping = MethodFocusMapping.objects.filter(method_id__in=method_ids).values_list(
        'method_id', 'focus_id')
    method_subject_mapping = MethodSubjectMapping.objects.filter(method_id__in=method_ids).values_list(
        'method_id', 'subject_id')

    # Create dictionaries for focus and subject mapping
    focus_dict = {focus.id: focus.name_chin for focus in Focus.objects.all()}
    subject_dict = {subject.id: subject.name_chin for subject in Subject.objects.all()}

    # Now, update the study_methods list
    for method in study_methods:
        method_id = method.id

        # Retrieve focus data from the pre-fetched mapping
        focus_ids = [focus_id for method_id_db, focus_id in method_focus_mapping if method_id_db == method_id]
        method.focus_id = focus_ids
        method.focus = ", ".join([focus_dict[focus_id] for focus_id in focus_ids])

        # Retrieve subject data from the pre-fetched mapping
        subject_ids = [subject_id for method_id_db, subject_id in method_subject_mapping if method_id_db == method_id]
        method_subjects = [subject_dict[subject_id] for subject_id in subject_ids]
        method.subject_id = subject_ids
        method.subject = "All" if len(method_subjects) == 0 else ", ".join(method_subjects)
    
    if not request.method == 'POST':
        form = forms.StudyMethodFilterForm(subjects=subjects_list, focuses=focuses_list)
        return render(request, 'study_method.html', {'form': form, 'study_methods': study_methods, 'student_methods':student_methods})
    
    form = forms.StudyMethodFilterForm(subjects=subjects_list, focuses=focuses_list, data=request.POST)
    if not form.is_valid():
        return render(request, 'study_method.html', {'form': form, 'study_methods': study_methods, 'student_methods':student_methods})

    social_style_weight = {"not matched":0.7, "all":0.8, "matched":1}
    time_consumption_weight = {"Low": {"Low": 1, "Middle":0.75, "High":0.5}, "Middle": {"Low": 1, "Middle":1, "High":0.75}, "High": {"Low": 1, "Middle":1, "High":1}}
    subject_weight = {"not matched":0.5, "all":1.25, "matched":1.5}
    focus_weight = {"not matched":1, "all":1.25, "matched":1.5}

    social_style = int(form.cleaned_data['social_style'])
    time_consumption = form.cleaned_data['time_consumption']
    subject = int(form.cleaned_data['subject'])
    focus = int(form.cleaned_data['study_focus'])

    for method in study_methods:
        if social_style == 4:
            social_style_match = 'all'
        else:
            method_social_style=[method.social_style_analytic, method.social_style_amiable, method.social_style_driver, method.social_style_expressive]
            if method_social_style[0] == method_social_style[1] == method_social_style[2] == method_social_style[3] ==1:
                social_style_match = 'all'
            elif method_social_style[social_style] == 1:
                social_style_match = 'matched'
            else:
                social_style_match = 'not matched'
        social_style_score = social_style_weight[social_style_match]

        if time_consumption == 'All':
            time_consumption_score = 1
        else:
            time_consumption_score = time_consumption_weight[time_consumption][method.time_consumption]

        if subject == 0:
            subject_match = 'all'
        elif subject in method.subject_id:
            subject_match = 'matched'
        else:
            subject_match = 'not matched'
        subject_score = subject_weight[subject_match]

        if focus == 0:
            focus_match = 'all'
        elif focus in method.focus_id:
            focus_match = 'matched'
        else:
            focus_match = 'not matched'
        focus_score = focus_weight[focus_match]
        method.score = social_style_score + time_consumption_score + subject_score + focus_score

    study_methods = sorted(study_methods, key=attrgetter('score'), reverse=True)
    return render(request, 'study_method.html', {'form': form, 'study_methods': study_methods, 'student_methods':student_methods})


@login_required(login_url='signin')
def study_method_add(request, method_id):
    student = get_student(request)
    if StudentMethodMapping.objects.filter(student_id=student.id, method_id=method_id, status="ongoing").exists():
        return redirect('study_method')
    if not Method.objects.filter(id=method_id).exists():
        return redirect('study_method')

    method = Method.objects.get(id=method_id)
    goals = Goal.objects.filter(student_id=student.id, goal_status="on going").values('id', 'name')
    goals = [('0', '沒有相關目標')] + [(goal['id'], goal['name']) for goal in goals]

    subject_id_list = UserSubjectList.objects.filter(
        user_id=student.id).values_list('subject_id', flat=True)
    subjects = Subject.objects.filter(
        id__in=subject_id_list).values('id', 'name_abbr', 'name_chin')
    subjects_list = [
        (subject['id'], f"{subject['name_abbr']} - {subject['name_chin']}") for subject in subjects]
    if not request.method == 'POST':
        form = forms.StudyMethodAddForm(goals=goals, subjects=subjects_list)
        return render(request, 'study_method_add.html', {'form': form, 'method': method})
    form = forms.StudyMethodAddForm(goals=goals, subjects=subjects_list ,data=request.POST)
    if not form.is_valid():
        return render(request, 'study_method_add.html', {'form': form, 'method': method})

    student_method_mapping = StudentMethodMapping()
    student_method_mapping.student_id = student.id
    student_method_mapping.method_id = method_id
    if int(form.cleaned_data['goal']) != 0:
        student_method_mapping.related_goal_id = int(form.cleaned_data['goal'])
    student_method_mapping.personalization = form.cleaned_data['personalization']
    student_method_mapping.status = "on going"
    student_method_mapping.name = method.name_chin
    student_method_mapping.description = method.description_chin
    student_method_mapping.save()

    for subject in form.cleaned_data['subject']:
        student_method_subject_mapping = StudentMethodSubjectMapping()
        student_method_subject_mapping.student_method_mapping_id = student_method_mapping.id
        student_method_subject_mapping.subject_id = subject
        student_method_subject_mapping.save()
    return redirect('study_method')   


@login_required(login_url='signin')
def study_method_evaluation(request, method_id):
    student = get_student(request)
    if not StudentMethodMapping.objects.filter(student_id=student.id, id=method_id).exists():
        return redirect('study_method')
    
    method = StudentMethodMapping.objects.get(student_id=student.id, id=method_id)
    if not request.method == 'POST':
        form = forms.StudyMethodEvaluationForm(initial={'personalization': method.personalization})
        return render(request, 'study_method_evaluation.html', {'form': form, 'method': method})
    form = forms.StudyMethodEvaluationForm(initial={'personalization': method.personalization}, data=request.POST)
    
    if not form.is_valid():
        return render(request, 'study_method_evaluation.html', {'form': form, 'method': method})

    if form.cleaned_data['status'] == '1':
        method.status = 'finished'
    elif form.cleaned_data['status'] == '2':
        method.status = 'failed'
    method.personalization = form.cleaned_data['personalization']
    method.save()

    method_evaluation = StudentMethodEvaluate()
    method_evaluation.student_method_mapping_id = method_id
    method_evaluation.suitable = form.cleaned_data['suitable']
    method_evaluation.willingness = form.cleaned_data['willingness']
    method_evaluation.comment = form.cleaned_data['comment']
    method_evaluation.save()
    return redirect('study_method')


@login_required(login_url='signin')
def study_method_delete(request, method_id):
    student = get_student(request)
    if StudentMethodMapping.objects.filter(student_id=student.id, id=method_id, status="on going").exists():
        StudentMethodSubjectMapping.objects.filter(student_method_mapping_id=method_id).delete()
        TaskMethodMapping.objects.filter(student_method_mapping_id=method_id).delete()
        StudentMethodMapping.objects.filter(id=method_id).delete()
    return redirect('study_method')


@login_required(login_url='signin')
def study_method_delete_page(request):
    student = get_student(request)
    method_list = []
    status_dict = {'on going': '進行中', 'finished': '以完結', 'failed': '已放棄'}
    if StudentMethodMapping.objects.filter(student_id=student.id).exists():
        method_list = StudentMethodMapping.objects.filter(student_id=student.id, status="on going")
        for method in method_list:
            method.display_status = status_dict[method.status]
    return render(request, 'study_method_delete_page.html', {'method_list': method_list})


@login_required(login_url='signin')
def coaching_report_dashboard_entry(request):
    role, student_form, user, student, coach = get_student_form(request)

    if not request.method == 'POST':
        return render(request, 'coaching_report_dashboard_entry.html', {'student_form': student_form})

    request.session['coaching_report_dashboard_student_id']=student.id
    return redirect('coaching_report_dashboard')


@login_required(login_url='signin')
def coaching_report_dashboard(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_dashboard_student_id'])

    report_dashboard = CoachingReportDashboard.objects.filter(student_id=student.id, phase=student.phase)

    if report_dashboard.count() <1:
        report_dashboard = CoachingReportDashboard()
        report_dashboard.student_id = student.id
        report_dashboard.phase = student.phase
        report_dashboard.save()

    report_dashboard = report_dashboard[0]
    report_dashboard.s_and_c_list = get_model_list('s_and_c', report_dashboard)
    report_dashboard.ac_list = get_model_list('ac', report_dashboard)
    report_dashboard.subject_list = CoachingReportDashboardSubjectComment.objects.filter(report_dashboard_id=report_dashboard.id).values_list('subject_display_name', 'subject_comment')


    request.session['coaching_report_dashboard_student_id']=student.id

    return render(request, 'coaching_report_dashboard.html', {'report_dashboard': report_dashboard, 'student': student})


@login_required(login_url='signin')
def coaching_report_dashboard_social_style(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_dashboard_student_id'])

    report_dashboard = CoachingReportDashboard.objects.filter(student_id=student.id, phase=student.phase)
    if report_dashboard.count() <1:
        return redirect('coaching_report_dashboard')
    report_dashboard = report_dashboard[0]

    comment_dict = get_selected_comment(student)
    sc_choices, ac_choices, report_choices, comment_list = comment_dict['sc'][1], comment_dict['ac'][1], comment_dict['report'][1], comment_dict['comment_list']
    sample_format = "請描述同學的特質和需要注意的事項，以下是其中一個例子：<br>特質分析：蘇同學在待人處事上展現了表達型和分析型的優點，而分析型的處事風格也彌補了表達型處事風格中可能缺乏事實和實際性的缺點。<br>注意事項：蘇同學有時候過於追求他人的肯定和贊賞，這樣的追求可能使他自身承受過多壓力。因此，蘇同學應該適當地降低對自己的要求，以減輕壓力的負擔。<br>同時，蘇同學在表達自己觀點和意見時，有時可能忽略了他人的感受和想法。為了改善這一點，他可以更加注重感受的重要性，並在表達意見時傾聽他人的觀點。"

    # Social Style Before/After/Comment
    social_styles = sorted(UserSocialStyle.objects.filter(user_id=student.id), key=attrgetter('created_at'), reverse=True)[:5]
    social_style_list = [(social_style.id, f"({social_style.created_at.strftime('%d %b %Y')}), Analytic: {social_style.analytical}, Driver: {social_style.driver}, Amiable: {social_style.amiable}, Expressive: {social_style.expressive}") for social_style in social_styles]
    social_style_list.insert(0, (0, '----- No Social Style -----'))
    initial = {}
    if  report_dashboard.before_social_style_id != None:
        initial['before_social_style'] = report_dashboard.before_social_style_id
    if  report_dashboard.after_social_style_id != None:
        initial['after_social_style'] = report_dashboard.after_social_style_id
    if  report_dashboard.social_style_comment != None:
        initial['social_style_comment'] = report_dashboard.social_style_comment

    if not request.method == 'POST':
        social_style_form = forms.CoachingReportDashboardSocialStyleForm(initial=initial, social_styles=social_style_list)
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format)
        return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form,'social_style_form': social_style_form, 'student': student, 'report_dashboard': report_dashboard})

    # When the coach try to generate the comment with the selected comments using Chat GPT
    if 'generate' in request.POST:
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format, data=request.POST)
        social_style_form = forms.CoachingReportDashboardSocialStyleForm(initial=initial, social_styles=social_style_list)

        # Check if the student has a social style record in the  report dashboard database
        if  report_dashboard.after_social_style_id == None:
            return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form,'social_style_form': social_style_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select an After Social Style'})

        if not selected_comment_form.is_valid():
            return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form, 'social_style_form': social_style_form, 'student': student, 'report_dashboard': report_dashboard})

        comments, comment_mix = handle_selected_comment(comment_list ,selected_comment_form.cleaned_data)

        if comments == "":
            return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form, 'social_style_form': social_style_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select at least one comment'})
        
        # the output will be a list (for future use of choosing the best comment)
        if comment_mix:
            general_comment = get_general_comment(comments)
            personalized_comment = gen_social_style_personalisation(general_comment[0])
        else:
            personalized_comment = [comments]

        after_social_style = report_dashboard.after_social_style
        surname = get_surname(student.name_chinese)
        social_style_type = get_social_style_type(after_social_style)
        scores = [surname, social_style_type, after_social_style.analytical, after_social_style.amiable, after_social_style.expressive, after_social_style.driver]
        
        generated_comment = get_social_style_comment(scores, personalized_comment[0])[0]

        return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form, 'social_style_form': social_style_form, 'student': student, 'generated_comment': generated_comment, 'report_dashboard': report_dashboard})

    # Social Style Report Input
    social_style_form = forms.CoachingReportDashboardSocialStyleForm(social_styles=social_style_list, data=request.POST)

    if not social_style_form.is_valid():
        return render(request, 'coaching_report_dashboard_social_style.html', {'selected_comment_form': selected_comment_form,'social_style_form': social_style_form, 'student': student, 'report_dashboard': report_dashboard})

    before_social_style = int(social_style_form.cleaned_data['before_social_style'])
    after_social_style = int(social_style_form.cleaned_data['after_social_style'])
    if before_social_style != 0:
        report_dashboard.before_social_style_id = before_social_style
    else:
        report_dashboard.before_social_style_id = None
    if after_social_style != 0:
        report_dashboard.after_social_style_id = after_social_style
        report_dashboard.social_style_type = get_social_style_type(report_dashboard.after_social_style)
    else:
        report_dashboard.after_social_style_id = None
        report_dashboard.social_style_type = None
    report_dashboard.social_style_comment = social_style_form.cleaned_data['social_style_comment']

    report_dashboard.coach = coach
    report_dashboard.updated_at = datetime.now()
    report_dashboard.save()
    return redirect('coaching_report_dashboard')


@login_required(login_url='signin')
def coaching_report_dashboard_s_and_c(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_dashboard_student_id'])

    initial_s_and_c = {'select':request.session['s_and_c_select'] if 's_and_c_select' in request.session else None}
    report_dashboard = CoachingReportDashboard.objects.filter(student_id=student.id, phase=student.phase)
    if report_dashboard.count() <1:
        return redirect('coaching_report_dashboard')
    report_dashboard = report_dashboard[0]
    report_dashboard.initial_s_and_c = initial_s_and_c['select']

    model_type = 's_and_c'
    report_dashboard.s_and_c_list = get_model_list(model_type, report_dashboard)
    choices = get_model_select_choices(model_type)
    area_scores = {}

    comment_dict = get_selected_comment(student)
    sc_choices, ac_choices, report_choices, comment_list = comment_dict['sc'][1], comment_dict['ac'][1], comment_dict['report'][1], comment_dict['comment_list']
    sample_format = "請列舉同學的相關行爲，以下是其中一個例子：<br> 1. 作議論文時每次都能做詳細資料搜集，文章邏輯清晰章邏輯清晰。| 2.  | 3."

    if report_dashboard.initial_s_and_c != None:
        report_dashboard.s_and_c_scores = get_model_score(model_type, initial_s_and_c['select'], student)
        for item in MODEL_SCORE_DICT[model_type][ initial_s_and_c['select']]:
            score = getattr(report_dashboard, item)
            area_scores[item] = score if score != None else 0
        report_dashboard.s_and_c_chin = get_model_chin(model_type, initial_s_and_c['select'])
        area_scores['model_comment'] = getattr(report_dashboard, f"{initial_s_and_c['select']}_comment")
        s_and_c_form = forms.CoachingReportDashboardModelScoreForm(areas=report_dashboard.s_and_c_scores, initial=area_scores)
    else:
        s_and_c_form = None
                
    if not request.method == 'POST':
        s_and_c_select_form = forms.CoachingReportDashboardSelectForm(choices=choices, model_name="S&C", initial=initial_s_and_c)
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format)
        return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'report_dashboard': report_dashboard})

    if 's_and_c_select' in request.POST:
        s_and_c_select_form = forms.CoachingReportDashboardSelectForm(choices=get_model_select_choices(model_type), model_name="S&C", data=request.POST)
        if s_and_c_select_form.is_valid():
            request.session['s_and_c_select'] = s_and_c_select_form.cleaned_data['select']
        return redirect('coaching_report_dashboard_s_and_c')

    if 'generate' in request.POST:
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format, data=request.POST)
        s_and_c_select_form = forms.CoachingReportDashboardSelectForm(choices=get_model_select_choices(model_type), model_name="S&C", initial=initial_s_and_c)

        if initial_s_and_c['select'] == None:
            return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select an S&C (Click the Select Button)'})
        
        if not selected_comment_form.is_valid():
            return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'report_dashboard': report_dashboard})
        comments, comment_mix = handle_selected_comment(comment_list ,selected_comment_form.cleaned_data)
        if comments == "":
            return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select at least one comment'})
        s_and_c_instruction = s_and_c_instruction_dict[initial_s_and_c['select']]
        surname = get_surname(student.name_chinese)
        skills_and_competencies_scores = [surname]
        for item in MODEL_SCORE_DICT[model_type][ initial_s_and_c['select']]:
            score = getattr(report_dashboard, item)
            skills_and_competencies_scores.append(str(score) if score != None else '0')
        generated_comment = get_s_and_c_comment(s_and_c_instruction, skills_and_competencies_scores, comments)[0]

        return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'generated_comment': generated_comment, 'report_dashboard': report_dashboard})

    s_and_c_select_form = forms.CoachingReportDashboardSelectForm(choices=choices, model_name="S&C", initial=initial_s_and_c)
    selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format)
    s_and_c_form = forms.CoachingReportDashboardModelScoreForm(areas=report_dashboard.s_and_c_scores, data=request.POST)
    if not s_and_c_form.is_valid():
        return render(request, 'coaching_report_dashboard_s_and_c.html', {'s_and_c_select_form':s_and_c_select_form ,'selected_comment_form': selected_comment_form, 's_and_c_form': s_and_c_form, 'student': student, 'report_dashboard': report_dashboard})
    
    score_list = []
    for item in MODEL_SCORE_DICT[model_type][ initial_s_and_c['select']]:
        setattr(report_dashboard, item, s_and_c_form.cleaned_data[item])
        score_list.append(s_and_c_form.cleaned_data[item])
    
    setattr(report_dashboard, f"{initial_s_and_c['select']}_comment", s_and_c_form.cleaned_data['model_comment'])

    count = sum(1 for item in score_list if item != 0)

    if count > 0:
        setattr(report_dashboard, f"{initial_s_and_c['select']}_score", round(sum(score_list)/count))

    report_dashboard.coach = coach
    report_dashboard.updated_at = datetime.now()
    report_dashboard.save()
    return redirect('coaching_report_dashboard')


@login_required(login_url='signin')
def coaching_report_dashboard_ac(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_dashboard_student_id'])

    initial_ac = {'select':request.session['ac_select'] if 'ac_select' in request.session else None}
    report_dashboard = CoachingReportDashboard.objects.filter(student_id=student.id, phase=student.phase)
    if report_dashboard.count() <1:
        return redirect('coaching_report_dashboard')
    report_dashboard = report_dashboard[0]
    report_dashboard.initial_ac = initial_ac['select']

    model_type = 'ac'
    report_dashboard.ac_list = get_model_list(model_type, report_dashboard)
    choices = get_model_select_choices(model_type)
    area_scores = {}

    comment_dict = get_selected_comment(student)
    sc_choices, ac_choices, report_choices, comment_list = comment_dict['sc'][1], comment_dict['ac'][1], comment_dict['report'][1], comment_dict['comment_list']
    sample_format = "請列舉同學的相關行爲，以下是其中一個例子：<br> 1. 作議論文時每次都能做詳細資料搜集，文章邏輯清晰章邏輯清晰。| 2.  | 3."

    if report_dashboard.initial_ac != None:
        report_dashboard.ac_scores = get_model_score(model_type, initial_ac['select'], student)
        for item in MODEL_SCORE_DICT[model_type][ initial_ac['select']]:
            score = getattr(report_dashboard, item)
            area_scores[item] = score if score != None else 0
        report_dashboard.ac_chin = get_model_chin(model_type, initial_ac['select'])
        area_scores['model_comment'] = getattr(report_dashboard, f"{initial_ac['select']}_comment")
        ac_form = forms.CoachingReportDashboardModelScoreForm(areas=report_dashboard.ac_scores, initial=area_scores)
    else:
        ac_form = forms.CoachingReportDashboardModelScoreForm(areas="")
                
    if not request.method == 'POST':
        ac_select_form = forms.CoachingReportDashboardSelectForm(choices=choices, model_name="AC", initial=initial_ac)
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format)
        return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'report_dashboard': report_dashboard})

    if 'ac_select' in request.POST:
        ac_select_form = forms.CoachingReportDashboardSelectForm(choices=get_model_select_choices(model_type), model_name="", data=request.POST)
        if ac_select_form.is_valid():
            request.session['ac_select'] = ac_select_form.cleaned_data['select']
        return redirect('coaching_report_dashboard_ac')

    if 'generate' in request.POST:
        selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format, data=request.POST)
        ac_select_form = forms.CoachingReportDashboardSelectForm(choices=get_model_select_choices(model_type), model_name="AC", initial=initial_ac)

        if initial_ac['select'] == None:
            return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select an AC (Click the Select Button)'})
        
        if not selected_comment_form.is_valid():
            return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'report_dashboard': report_dashboard})
        comments, comment_mix = handle_selected_comment(comment_list ,selected_comment_form.cleaned_data)
        if comments == "":
            return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'report_dashboard': report_dashboard, 'msg': 'Please select at least one comment'})
        
        # ac_instruction = ac_instruction_dict[initial_ac['select']]
        # surname = get_surname(student.name_chinese)
        # ac_scores = [surname]
        # for item in MODEL_SCORE_DICT[model_type][ initial_ac['select']]:
        #     score = getattr(report_dashboard, item)
        #     ac_scores.append(str(score) if score != None else '0')
        # generated_comment = get_ac_comment(ac_instruction, ac_scores, comments)[0]

        generated_comment = ''

        return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'generated_comment': generated_comment, 'report_dashboard': report_dashboard})

    ac_select_form = forms.CoachingReportDashboardSelectForm(choices=choices, model_name="AC", initial=initial_ac)
    selected_comment_form = forms.CoachingReportDashboardCommentForm(sc_choices=sc_choices, ac_choices=ac_choices, report_choices=report_choices, sample_format=sample_format)
    ac_form = forms.CoachingReportDashboardModelScoreForm(areas=report_dashboard.ac_scores, data=request.POST)
    if not ac_form.is_valid():
        return render(request, 'coaching_report_dashboard_ac.html', {'ac_select_form':ac_select_form ,'selected_comment_form': selected_comment_form, 'ac_form': ac_form, 'student': student, 'report_dashboard': report_dashboard})
    
    score_list = []
    for item in MODEL_SCORE_DICT[model_type][ initial_ac['select']]:
        setattr(report_dashboard, item, ac_form.cleaned_data[item])
        score_list.append(ac_form.cleaned_data[item])
    
    setattr(report_dashboard, f"{initial_ac['select']}_comment", ac_form.cleaned_data['model_comment'])

    count = sum(1 for item in score_list if item != 0)

    if count > 0:
        setattr(report_dashboard, f"{initial_ac['select']}_score", round(sum(score_list)/count))

    report_dashboard.coach = coach
    report_dashboard.updated_at = datetime.now()
    report_dashboard.save()
    return redirect('coaching_report_dashboard')


@login_required(login_url='signin')
def coaching_report_dashboard_subjects(request):
    coach = get_coach(request)
    student = User.objects.get(id=request.session['coaching_report_dashboard_student_id'])

    report_dashboard = CoachingReportDashboard.objects.filter(student_id=student.id, phase=student.phase)
    if report_dashboard.count() <1:
        return redirect('coaching_report_dashboard')
    report_dashboard = report_dashboard[0]

    subject_id_list = UserSubjectList.objects.filter(user_id=student.id).values_list('subject_id', flat=True)
    subjects = Subject.objects.filter(id__in=subject_id_list).annotate(
    has_comments=Exists(
        CoachingReportDashboardSubjectComment.objects.filter(
            subject_id=OuterRef('pk'), 
            report_dashboard_id=report_dashboard.id
        )))
    subjects = subjects.filter(has_comments=False).values('id', 'name_abbr', 'name_chin')
    subjects_list = [(subject['id'], f"{subject['name_abbr']} - {subject['name_chin']}") for subject in subjects]

    report_dashboard.subject_comments = CoachingReportDashboardSubjectComment.objects.filter(report_dashboard_id=report_dashboard.id).values_list('subject_display_name', 'subject_comment')

    if not request.method == 'POST':
        subject_comment_form = forms.CoachingReportDashboardSubjectCommentForm(choices=subjects_list)
        return render(request, 'coaching_report_dashboard_subjects.html', {'subject_comment_form': subject_comment_form, 'student': student, 'report_dashboard': report_dashboard})
    


    return redirect('coaching_report_dashboard')


@login_required(login_url='signin')
def user_role(request):
    if not request.user.is_superuser:
        redirect('profile')

    user_list = User.objects.all()

    user_forms = []
    if not request.method == 'POST':
        for user in user_list:
            form = forms.UserRoleForm(
                prefix=user.id, instance=user, username=user.username)
            user_forms.append(form)
        return render(request, 'user_role.html', {'forms': user_forms})
    for user in user_list:
        form = forms.UserRoleForm(
            data=request.POST, prefix=user.id, instance=user, username=user.username)
        if not form.is_valid():
            user_forms.append(form)
            continue
        form.save()
    return redirect('profile')


@login_required(login_url='signin')
def coach_student_select(request):
    if not request.user.is_superuser:
        redirect('profile')
    student_list = User.objects.filter(role='student')
    coach_list = User.objects.filter(role='coach')
    for coach in coach_list:
        coach.students = CoachStudentMapping.objects.filter(
            coach_id=coach.id).values_list('student_id', flat=True)

    data_list = []

    if not request.method == 'POST':
        for coach in coach_list:
            form = forms.CoachStudentSelectForm(
                prefix=coach.id, students=student_list, coach=coach)

            coach_student_list = (
                [student for student in student_list if student.id in coach.students])
            data_list.append((form, coach_student_list))
        return render(request, 'coach_student_select.html', {'data_list': data_list})

    for coach in coach_list:
        form = forms.CoachStudentSelectForm(
            data=request.POST, prefix=coach.id, students=student_list, coach=coach)
        if not form.is_valid():
            coach_student_list = (
                [student for student in student_list if student.id in coach.students])
            data_list.append((form, coach_student_list))
            continue

        if form.cleaned_data['student'] == '':
            continue

        new_mapping = CoachStudentMapping()
        new_mapping.coach_id = coach.id
        new_mapping.student_id = form.cleaned_data['student']
        new_mapping.save()

    return redirect('coach_student_select')


@login_required(login_url='signin')
def coach_student_mapping_delete(request, coach_id, student_id):
    if not request.user.is_superuser:
        redirect('profile')
    CoachStudentMapping.objects.filter(
        coach_id=coach_id, student_id=student_id).delete()
    return redirect('coach_student_select')


def get_student_form(request):
    user = User.objects.get(username=request.user.username)
    role = user.role
    if request.user.is_superuser:
        role = 'coach'
    student_form = None
    if role == 'coach':
        if 'coach_as_student' not in request.session:
            request.session['coach_as_student'] = -1
        
        if request.session['coach_as_student'] != -1:
            student = User.objects.get(
                id=request.session['coach_as_student'])
            coach = user
        else:
            student = None
            coach = user

        if request.method == 'POST':
            student_form = forms.StudentForm(data=request.POST, coach=user)
            if student_form.is_valid():
                student = User.objects.get(
                    id=student_form.cleaned_data['student'])

        else:
            student_form = forms.StudentForm(coach=user)
    else:
        student = user
        coach = None

    return role, student_form, user, student, coach


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
        if request.session['coach_as_student'] != -1:
            # get the student object for the student the coach is viewing
            try:
                student = User.objects.get(
                    id=request.session['coach_as_student'])
            except User.DoesNotExist:
                student = None
        else:
            # get the student objects for all students the coach is coaching
            students = User.objects.all()
            student_ids = CoachStudentMapping.objects.filter(
                coach_id=user.id).values_list('student_id', flat=True)
            student = [user for user in students if user.id in student_ids]

    else:
        # get the student object for the current user
        student = user

    return student


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


def get_goal_type_chin(goal_type_list):
    goal_type_dict = {"interest": "興趣", "academic": "學業", "career": "事業", "wellbeing": "健康"}
    if type(goal_type_list) == list:
        for goal_type in goal_type_list:
            goal_type = goal_type_dict[goal_type]
    else:
        goal_type_list = goal_type_dict[goal_type_list]
    return goal_type_list


def get_difficulty_chin(difficulty_list):
    difficulty_dict = {"easy": "容易", "moderate": "合適", "ambitious": "有挑戰性"}
    if type(difficulty_list) == list:
        for difficulty in difficulty_list:
            difficulty = difficulty_dict[difficulty]
    else:
        difficulty_list = difficulty_dict[difficulty_list]
    return difficulty_list


def get_task_parents(tasks):
    # print(type(tasks), " - ", tasks)
    task_ids = [task.id for task in tasks]

    # Fetch all related subjects, goals, methods, and parent tasks using select_related/prefetch_related
    subject_mappings = TaskSubjectMapping.objects.filter(task_id__in=task_ids).select_related('subject')
    goal_mappings = TaskGoalMapping.objects.filter(task_id__in=task_ids).select_related('goal')
    method_mappings = TaskMethodMapping.objects.filter(task_id__in=task_ids).select_related('student_method_mapping__method')
    task_mappings = TaskTaskMapping.objects.filter(child_task_id__in=task_ids).select_related('parent_task')

    # Create dictionaries for quick lookups
    subject_dict = {mapping.task_id: mapping.subject for mapping in subject_mappings}
    goal_dict = {mapping.task_id: mapping.goal for mapping in goal_mappings}
    method_dict = {mapping.task_id: mapping.student_method_mapping.method for mapping in method_mappings}

    # Prefetch related parent tasks for all child tasks
    task_dict = {}
    for mapping in task_mappings:
        if mapping.child_task_id not in task_dict:
            task_dict[mapping.child_task_id] = []
        task_dict[mapping.child_task_id].append(mapping.parent_task)

    # Process each task and populate the attributes
    for task in tasks:
        # Populating subject_name
        subject = subject_dict.get(task.id)
        task.subject_name = ', '.join([subject.name_abbr + ' - ' + subject.name_chin]) if subject else '/'

        # Populating goal_name
        goal = goal_dict.get(task.id)
        task.goal_name = goal.name if goal else '/'

        # Populating method_name
        method = method_dict.get(task.id)
        task.method_name = method.name_chin if method else '/'

        # Populating task_name
        parent_tasks = task_dict.get(task.id, [])
        task.task_name = ', '.join([parent_task.name for parent_task in parent_tasks]) if parent_tasks else '/'

    return tasks


def get_social_style_type(social_style):
    scores = {'友善': social_style.amiable,'表達': social_style.expressive, '分析': social_style.analytical, '推動': social_style.driver}
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    if (sorted_scores[0][1] == sorted_scores[2][1]):
        return '沒有主次的待人處事風格'
    def get_level(score):
        if score >= 40:
            return '高度'
        elif score >= 35:
            return '中高'
        elif score >= 25:
            return '中度'
        else: 
            return '低度'
    return f"{sorted_scores[0][0]}{sorted_scores[1][0]}型({get_level(sorted_scores[0][1])}{sorted_scores[0][0]},  {get_level(sorted_scores[1][1])}{sorted_scores[1][0]})"


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


def get_surname(name):
    if len(name) == 4:
        return name[0:2] + "同學"
    elif len(name)== 3:
        return name[0] + "同學"
    else:
        return "同學"


def get_selected_comment(student):
    # List of comments to be selected    
    reports = CoachingReportRecord.objects.filter(student_id=student.id, phase=student.phase)
    ac = AcademicCoachingRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports)
    sc = SAndCRecord.objects.select_related('coaching_report_record').filter(coaching_report_record_id__in=reports)

    sc_get = get_comments(sc, 's_and_c')
    sc_comments, sc_choices = sc_get[0], sc_get[1]
    ac_get = get_comments(ac, 'ac')
    ac_comments, ac_choices = ac_get[0], ac_get[1]    
    report_get = get_comments(reports, 'report')
    report_comments, report_choices = report_get[0], report_get[1]
    comment_list = {**report_comments, **sc_comments, **ac_comments}

    return {'sc': [sc_comments, sc_choices], 'ac': [ ac_comments, ac_choices], 'report': [report_comments, report_choices], 'comment_list': comment_list}


def handle_selected_comment(comment_list, selected):
    # get the list of selected comment and handle them to fit the format of the Chat GPT
    def all_value_empty(selected):
        for value in selected.values():
            if value:
                return False
        return True

    comment_mix = False

    if selected['personalized_comment'] != '':
        return selected['personalized_comment'], comment_mix

    if all_value_empty(selected):
        return "", comment_mix
    
    comment_mix = True

    selected_comment = []
    for k in selected:
        if (k == 'add_comment') and (selected[k] != ''):
            split_text = selected[k].split("//")
            for text in split_text:
                selected_comment.append(text)
        else:
            for i in selected[k]:
                selected_comment.append(comment_list[k][int(i)])
        
    comments = " | ".join(f"{i+1}. {s}" for i, s in enumerate(selected_comment))
    return comments, comment_mix


def get_model_chin(model_type, model_list):
    if model_type == 's_and_c':
        model_dict = {s_and_c: S_AND_C_CHIN[i] for i, s_and_c in enumerate(S_AND_C)}
    elif model_type == 'ac':
        model_dict = {ac: AC_CHIN[i] for i, ac in enumerate(AC)}
    if type(model_list) == list:
        for model in model_list:
            model = model_dict[model]
    else:
        model_list = model_dict[model_list]
    return model_list


def get_model_list(model_type, report_dashboard):
    model_list = []
    if model_type == 's_and_c':
        for s_and_c in S_AND_C:
            score = getattr(report_dashboard, f"{s_and_c}_score")
            comment = getattr(report_dashboard, f"{s_and_c}_comment")
            if score == None:
                score = 0
            if comment == None:
                comment = ""
            model_list.append((s_and_c, get_model_chin('s_and_c', s_and_c), score, comment))
    elif model_type == 'ac':
        for ac in AC:
            score = getattr(report_dashboard, f"{ac}_score")
            comment = getattr(report_dashboard, f"{ac}_comment")
            if score == None:
                score = 0
            if comment == None:
                comment = ""
            model_list.append((ac, get_model_chin('ac', ac), score, comment))
    return model_list


def get_model_select_choices(model_type):
    if model_type == 's_and_c':
        choices = [(s_and_c, get_model_chin(model_type, s_and_c)) for s_and_c in S_AND_C]
    elif model_type == 'ac':
        choices = [(ac, get_model_chin(model_type, ac)) for ac in AC]
    return choices


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
        displayed.append((key ,f"Area {key[-1]}", f"AVG: {average} | "+ " ; ".join(displayed_scores)))
    return displayed
    
    



