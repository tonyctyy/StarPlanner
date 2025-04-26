"""
Serializers for converting CoachingReportDashboard objects to and from JSON representations.
These serializers handle the conversion of complex data structures into native Python datatypes 
that can be easily rendered into JSON, XML, or other content types for API requests and responses.
"""
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserSocialStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialStyle
        fields = '__all__'

class AcademicCoachingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicCoachingRecord
        fields = '__all__'

class SAndCRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SAndCRecord
        fields = '__all__'
        
class CoachInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachInfo
        fields = '__all__'
        
class CoachingReportDashboardSubjectCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingReportDashboardSubjectComment
        fields = '__all__'

class CoachingReportDashboardSerializer(serializers.ModelSerializer):
    # Serializing nested objects and custom fields
    subject_list = CoachingReportDashboardSubjectCommentSerializer(many=True)
    s_and_c_list = serializers.SerializerMethodField()
    ac_list = serializers.SerializerMethodField()
    s_and_c_scores = serializers.SerializerMethodField()
    ac_scores = serializers.SerializerMethodField()
    student = UserSerializer() # Serializing related model
    coach = UserSerializer() # Serializing related model
    before_social_style = UserSocialStyleSerializer() # Serializing related model
    after_social_style = UserSocialStyleSerializer() # Serializing related model

    # Custom methods to retrieve serialized data
    def get_s_and_c_list(self, obj):
        return [{'model': item[0], 'model_chinese': item[1], 'score': item[2], 'comment': item[3]} for item in obj.s_and_c_list]
    
    def get_ac_list(self, obj):
        return [{'model': item[0], 'model_chinese': item[1], 'score': item[2], 'comment': item[3]} for item in obj.ac_list]
    
    def get_s_and_c_scores(self, obj):
        # Extracting and formatting scores for S&C areas
        return_score = {}
        for area in obj.ac_scores:
            area_score = []
            key = area[0][0][0:-2]
            for item in area:
                area_score.append(item[1])
            return_score[key] = area_score
        return return_score
    
    def get_ac_scores(self, obj):
        # Extracting and formatting scores for AC areas
        return_score = {}
        for area in obj.ac_scores:
            area_score = []
            key = area[0][0][0:-2]
            for item in area:
                area_score.append(item[1])
            return_score[key] = area_score
        return return_score

    class Meta:
        model = CoachingReportDashboard
        fields = '__all__'
        
class CoachingReportRecordSerializer(serializers.ModelSerializer):
    ACRecord = AcademicCoachingRecordSerializer()
    # SAndCRecord = SAndCRecordSerializer()
    class Meta:
        model = CoachingReportRecord
        fields = '__all__'
        
class CoachStudentMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachStudentMapping
        fields = '__all__'
        
class EcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eca
        fields = '__all__'
        
class FinalEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalEvaluation
        fields = '__all__'
"""
class FocusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Focus
        fields = '__all__'
"""
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        
class GoalEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalEvaluate
        fields = '__all__'

"""
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'
        
class MethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Method
        fields = '__all__'
        
class MethodFocusMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodFocusMapping 
        fields = '__all__'
        
class MethodLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodLabel
        fields = '__all__'
        
class MethodLabelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodLabelMapping
        fields = '__all__'
        
class MethodSubjectMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodSubjectMapping
        fields = '__all__'
        
class MethodTaskSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodTaskSuggestion
        fields = '__all__'
"""

class PreAcademicCoachingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreAcademicCoachingRecord
        fields = '__all__'


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = '__all__'
"""
class StatusLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLabel
        fields = '__all__'
"""
class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = '__all__'
"""
class StudentMethodEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMethodEvaluate
        fields = '__all__'
    
class StudentMethodMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMethodMapping
        fields = '__all__'
        
class StudentMethodSubjectMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentMethodSubjectMapping
        fields = '__all__'
"""
class StudentPreAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentPreAssessment
        fields = '__all__'
"""
class StudentStatusRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentStatusRecord
        fields = '__all__'
"""
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
class TaskGoalMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGoalMapping
        fields = '__all__'
"""
class TaskMethodMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskMethodMapping
        fields = '__all__'
"""
class TaskTaskMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTaskMapping
        fields = '__all__'
"""
class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabel
        fields = '__all__'
        
class TaskLabelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabelMapping
        fields = '__all__'
        
class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = '__all__'
        
class TaskTemplateLabelMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplateLabelMapping
        fields = '__all__'
"""
class UserEcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEca
        fields = '__all__'
        
class UserGradeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGradeRecord
        fields = '__all__'
"""
class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest 
        fields = '__all__'
"""
class UserQualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQualification
        fields = '__all__'
        
class UserSubjectGradeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubjectGradeRecord
        fields = '__all__'
        
class UserSubjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubjectList
        fields = '__all__'
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'name', 'name_chinese', 'email']
        
        
    def save(self):
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
            name = self.validated_data['name'],
            name_chinese = self.validated_data['name_chinese'],
            role = 'student',
        )
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        if password1 != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password1)
        user.save()
            