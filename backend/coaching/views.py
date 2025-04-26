from datetime import datetime
from django.db.models import Q
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
        {'name': 'Coaching Report', 'url': '../coaching_report_entry'},
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

    # coach look of the profile page when they are looking at a student
    if request.session['coach_as_student'] != -1:
        button_list = coach_as_student_button_list + student_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form, 'student': student, 'coach': coach})

    # admin look of the profile page
    if request.user.is_superuser:
        button_list = admin_button_list + personal_info_button_list + coach_button_list

        return render(request, 'profile.html', {'button_list': button_list, 'role': role, 'student_form': student_form})

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

    option_mapping = {
        '1': '分析型',
        '2': '友善型',
        '3': '表達型',
        '4': '推動型',
    }
    # Render social style questionnaire form
    if not request.method == 'POST':
        form = forms.SocialStyleForm()
        return render(request, 'social_style.html', {'form': form})

    form = forms.SocialStyleForm(request.POST)

    if not form.is_valid():
        return render(request, 'social_style.html', {'form': form})

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

    # Render social style questionnaire form
    if not request.method == 'POST':
        form = forms.SocialStyleScoreForm()
        return render(request, 'social_style_score.html', {'form': form})

    form = forms.SocialStyleScoreForm(request.POST)

    if not form.is_valid():
        return render(request, 'social_style_score.html', {'form': form})

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
    goal_evaluation = GoalEvaluate()
    goal_evaluation.effort = form.cleaned_data['effort']
    goal_evaluation.progress = form.cleaned_data['progress']
    goal_evaluation.comment = form.cleaned_data['comment']
    goal_evaluation.goal_id = goal_id
    goal_evaluation.save()
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
    
    task = Task.objects.filter(id=task_id)
    get_task_parents(task)

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
        form = forms.CoachingReportForm(instance = form_instance)
        return render(request, 'coaching_report.html', {'form': form})
    form = forms.CoachingReportForm(request.POST,instance=form_instance)
    if not form.is_valid():
        return render(request, 'coaching_report.html', {'form': form})
    
    form.save()
    return redirect('profile')


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
        student_id=request.session['coaching_report_student_id']).order_by('section')
    coaching_report_num = coaching_report_list.count() + 1

    if not request.method == 'POST':
        return render(request, 'coaching_report_landing.html', {'coaching_report_list': coaching_report_list})
    
    new_coaching_report = CoachingReportRecord()
    new_coaching_report.student_id = student.id
    new_coaching_report.coach_id = coach.id
    new_coaching_report.section = coaching_report_num
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


