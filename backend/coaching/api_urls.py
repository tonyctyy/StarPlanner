from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import api_views

urlpatterns = [
    # path('signin/', api_views.signin, name='signin'),
    path('signout/', api_views.signout, name='signout'),
    # path('profile/', api_views.profile, name='profile'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('student_dashboard_api/', api_views.student_dashboard_api, name='student_dashboard_api'),
    path('get_calendar_data/', api_views.get_calendar_data, name='get_calendar_data'),
    path('save_calendar_data/', api_views.save_calendar_data, name='save_calendar_data'),
    path('get_student_list/', api_views.get_student_list, name='get_student_list'),
    path('add_goal/', api_views.add_goal, name='add_goal'),
    path('add_task/', api_views.add_task, name='add_task'),
    path('add_session_report/', api_views.add_session_report, name='add_session_report'),
    path('add_social_style/', api_views.add_social_style, name='add_social_style'),
    path('add_subject_comment/', api_views.add_subject_comment, name='add_subject_comment'),
    path('edit_session_report/', api_views.edit_session_report, name='edit_session_report'),
    path('edit_final_report/', api_views.edit_final_report, name='edit_final_report'),
    path('add_edit_pre_ac_record/', api_views.add_edit_pre_ac_record, name='add_edit_pre_ac_record'),
    path('edit_ac_record/', api_views.edit_ac_record, name='edit_ac_record'),
    path('edit_subject_comment/', api_views.edit_subject_comment, name='edit_subject_comment'),
    path('evaluate_goal/', api_views.evaluate_goal, name='evaluate_goal'),
    path('evaluate_task/', api_views.evaluate_task, name='evaluate_task'),
    path('get_session_reports/', api_views.get_session_reports, name='get_session_reports'),
    path('get_session_report/', api_views.get_session_report, name='get_session_report'),
    path('get_final_report/', api_views.get_final_report, name='get_final_report'),
    path('get_comment_list/', api_views.get_comment_list, name='get_comment_list'),
    path('get_gpt_comment/', api_views.get_gpt_comment, name='get_gpt_comment'),
    path('get_social_style/', api_views.get_social_style, name='get_social_style'),
    path('get_subject_comments/', api_views.get_subject_comments, name='get_subject_comments'),
    path('get_pre_ac_record/', api_views.get_pre_ac_record, name='get_pre_ac_record'),
    path('handle_delete/', api_views.handle_delete, name='handle_delete'),
]