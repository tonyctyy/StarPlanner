from django import forms

from django.contrib.auth.forms import PasswordChangeForm


from coaching.models import *


from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput
from datetime import datetime
import random


class SocialStyleForm(forms.Form):

    options1 = [('1', '開放'), ('2', '令人敬畏'), ('3', '獨創的'), ('4', '令人信服'),]
    options2 = [('1', '謹慎'), ('2', '溫厚的'), ('3', '有說服力'), ('4', '進取'),]
    options3 = [('1', '開放'), ('2', '溫順或願意幫助別人'), ('3', '大膽或冒險'), ('4', '頑固'),]
    options4 = [('1', '冷靜'), ('2', '忠誠'), ('3', '迷人'), ('4', '堅定不退縮'),]
    options5 = [('1', '推動/摧迫'), ('2', '自願的/自動的'), ('3', '熱切'), ('4', '意志堅強'),]
    options6 = [('1', '自我'), ('2', '適意的'), ('3', '意氣高昂的'), ('4', '自信'),]
    options7 = [('1', '精確'), ('2', '適意的'), ('3', '生氣蓬勃'), ('4', '斷言'),]
    options8 = [('1', '持久的'), ('2', '快樂'), ('3', '非常活躍'), ('4', '有紀律'),]
    options9 = [('1', '服從的'), ('2', '有同情心的'), ('3', '即興'), ('4', '堅持'),]
    options10 = [('1', '事事操心的'), ('2', '忍耐'), ('3', '愛新鮮感'), ('4', '富競爭'),]
    options11 = [('1', '受尊敬'), ('2', '快活或快樂'), ('3', '富影響力'), ('4', '樂觀'),]
    options12 = [('1', '服從的'), ('2', '慷慨的'), ('3', '富感染力'), ('4', '不敗的'),]
    options13 = [('1', '怯懦'), ('2', '體貼'), ('3', '能適應'), ('4', '勇敢'),]
    options14 = [('1', '有耐性'), ('2', '親切'), ('3', '易受鼓動的'), ('4', '爭論'),]
    options15 = [('1', '可信的'), ('2', '輕鬆愉快的'), ('3', '說話溫和的'), ('4', '自力更生的'),]
    options16 = [('1', '隨和'), ('2', '和平的'), ('3', '冒險'), ('4', '正面'),]
    options17 = [('1', '自控的'), ('2', '有容納力的'), ('3', '激發思維的'), ('4', '精力旺盛的'),]
    options18 = [('1', '準確'), ('2', '寬大或仁慈'), ('3', '易與人融合'), ('4', '果斷'),]
    options19 = [('1', '循規蹈矩'), ('2', '易滿足'), ('3', '健談'), ('4', '坦率'),]
    options20 = [('1', '老練/優雅'), ('2', '廣為人識'), ('3', '好交友的'), ('4', '愛冒險的'),]

    for options in [options1, options2, options3, options4, options5, options6, options7, options8, options9, options10, options11, options12, options13, options14, options15, options16, options17, options18, options19, options20]:
        random.shuffle(options)

    question_1 = forms.ChoiceField(
        choices=options1, widget=forms.RadioSelect())
    question_2 = forms.ChoiceField(
        choices=options2, widget=forms.RadioSelect())
    question_3 = forms.ChoiceField(
        choices=options3, widget=forms.RadioSelect())
    question_4 = forms.ChoiceField(
        choices=options4, widget=forms.RadioSelect())
    question_5 = forms.ChoiceField(
        choices=options5, widget=forms.RadioSelect())
    question_6 = forms.ChoiceField(
        choices=options6, widget=forms.RadioSelect())
    question_7 = forms.ChoiceField(
        choices=options7, widget=forms.RadioSelect())
    question_8 = forms.ChoiceField(
        choices=options8, widget=forms.RadioSelect())
    question_9 = forms.ChoiceField(
        choices=options9, widget=forms.RadioSelect())
    question_10 = forms.ChoiceField(
        choices=options10, widget=forms.RadioSelect())
    question_11 = forms.ChoiceField(
        choices=options11, widget=forms.RadioSelect())
    question_12 = forms.ChoiceField(
        choices=options12, widget=forms.RadioSelect())
    question_13 = forms.ChoiceField(
        choices=options13, widget=forms.RadioSelect())
    question_14 = forms.ChoiceField(
        choices=options14, widget=forms.RadioSelect())
    question_15 = forms.ChoiceField(
        choices=options15, widget=forms.RadioSelect())
    question_16 = forms.ChoiceField(
        choices=options16, widget=forms.RadioSelect())
    question_17 = forms.ChoiceField(
        choices=options17, widget=forms.RadioSelect())
    question_18 = forms.ChoiceField(
        choices=options18, widget=forms.RadioSelect())
    question_19 = forms.ChoiceField(
        choices=options19, widget=forms.RadioSelect())
    question_20 = forms.ChoiceField(
        choices=options20, widget=forms.RadioSelect())

    # def __init__(self, student_list=None,*args, **kwargs):
    #     super(SocialStyleForm, self).__init__(*args, **kwargs)
    #     if student_list is not None:
    #         self.fields['student']=forms.ChoiceField(choices=student_list, widget=forms.Select())
    #     else:
    #         self.fields['student']=forms.ChoiceField(choices=[], widget=forms.Select(), required=False)


class SocialStyleScoreForm(forms.Form):
    analytic = forms.IntegerField(min_value=0, max_value=100,)
    amiable = forms.IntegerField(min_value=0, max_value=100)
    expressive = forms.IntegerField(min_value=0, max_value=100)
    driver = forms.IntegerField(min_value=0, max_value=100)

    def clean(self):
        cleaned_data = super().clean()
        analytic = cleaned_data.get('analytic')
        amiable = cleaned_data.get('amiable')
        expressive = cleaned_data.get('expressive')
        driver = cleaned_data.get('driver')
        if analytic + amiable + expressive + driver != 100:
            raise forms.ValidationError(
                'The sum of all scores must be 100.')
        if analytic % 5 != 0 or amiable % 5 != 0 or expressive % 5 != 0 or driver % 5 != 0:
            raise forms.ValidationError(
                'All scores must be multiples of 5.')
        return cleaned_data


class UserInfoForm(forms.Form):
    name = forms.CharField(max_length=60, label="English Name")
    name_chinese = forms.CharField(max_length=60, label="中文姓名")
    email = forms.EmailField(label="Email")


class SubjectForm(forms.Form):
    options = [
        (5, '生物 - Bio'),
        (6, '商業、會計及財務研究 - BAFS'),
        (7, '化學 - Chem'),
        (8, '中國文學 - Chi Lit'),
        (9, '設計與應用科技 - DAT'),
        (10, '健康管理與社會關懷 - Health Mgmt & Soc Care'),
        (11, '資訊及通訊科技 - ICT'),
        (12, '英文文學 - Eng Lit'),
        (13, '體育 - PE'),
        (14, '物理 - Phys'),
        (15, '科技與生活 - TL'),
        (16, '音樂 - Music'),
        (17, '視覺藝術 - VA'),
        (18, '地理 - Geo'),
        (19, '歷史 - Hist'),
        (20, '道德及宗教研究 - ERS'),
        (21, '旅遊與款待研究 - THS'),
        (22, '經濟 - Econ'),
        (23, '中國歷史 - Chi Hist'),
        (24, '數學 （微積分與統計學） - M1'),
        (25, '數學 （代數與微積分） - M2'),
    ]

    choices = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=options
    )

    def clean(self):
        cleaned_data = super().clean()
        selected_choices = cleaned_data.get('choices', [])
        num_choices = len(selected_choices)

        if num_choices < 2:
            raise forms.ValidationError(
                'At least two checkbox must be selected.')
        elif num_choices > 4:
            raise forms.ValidationError(
                'At most four checkboxes can be selected.')
        return cleaned_data


class StudentPreAssessmentForm(forms.Form):
    long_term_goal = forms.CharField(required=False, label="你爲自己訂立了哪些長期目標？ （學業/職業/興趣方面的目標", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    area_to_improve = forms.CharField(required=False, label="你希望在哪些方面有進步？（e.g., 中文作文/數學MC...）", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    interested_question = forms.CharField(required=False, label="你有沒有一些對未來升學或職業路綫感興趣的問題？（e.g., 如何入讀某大學的某科", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))

    preferable_time_1_date = forms.DateField(
        widget=DatePickerInput, label="適合進行培導的時間(第一選擇)", input_formats=['%Y-%m-%d'])
    preferable_time_1_time = forms.TimeField(
        widget=TimePickerInput, label="", input_formats=['%H:%M'])

    preferable_time_2_date = forms.DateField(
        widget=DatePickerInput, label="適合進行培導的時間(第二選擇)", input_formats=['%Y-%m-%d'], required=False)
    preferable_time_2_time = forms.TimeField(
        widget=TimePickerInput, label="", input_formats=['%H:%M'], required=False)

    preferable_time_3_date = forms.DateField(
        widget=DatePickerInput, label="適合進行培導的時間(第三選擇)", input_formats=['%Y-%m-%d'], required=False)
    preferable_time_3_time = forms.TimeField(
        widget=TimePickerInput, label="", input_formats=['%H:%M'], required=False)


class GoalForm(forms.Form):
    GOAL_TYPE = [
        ('interest', '興趣 - Interest'),
        ('academic', '學業 - Academic'),
        ('career', '事業 - Career'),
        ('wellbeing', '健康 - Wellbeing'),
    ]
    DIFFICULTY = [
        ('easy', '容易 - Easy'),
        ('moderate', '合適 - Moderate'),
        ('ambitious', '有挑戰性 - Ambitious')
    ]
    def __init__(self, goals, *args, **kwargs):
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['goal'] = forms.ChoiceField(
            choices=goals,
            label="所屬目標",
            widget=forms.Select() )
    name = forms.CharField(max_length=60, label="目標名稱")
    description = forms.CharField(required=False, label="描述", widget=forms.Textarea(
    attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    goal_type = forms.ChoiceField(choices=GOAL_TYPE, label="類別")
    difficulty = forms.ChoiceField(choices=DIFFICULTY, label="難度")
    predicted_end_time = forms.DateField(
        widget=DatePickerInput, label="預計結束時間",  input_formats=['%Y-%m-%d'])


class GoalEvaluationForm(forms.Form):
    STATUS = [
        ('on going', '進行中 - On Going'),
        ('finished', '完成 - Finished'),
        ('failed', '失敗 - Failed'),
    ]
    progress = forms.IntegerField(min_value=0, max_value=10, 
                label="進度 (0-10分, 0% - 100%)")
    status = forms.ChoiceField(choices=STATUS, label="目前狀態")
    effort = forms.IntegerField(min_value=0, max_value=5, 
                label="努力程度 (0分代表沒有努力，5分代表竭盡全力)")
    final_result = forms.IntegerField(min_value=0, max_value=5, 
                label="成果 (0分代表沒有開始，5分代表完全完成)(在完成/失敗後填寫)", required=False)
    comment = forms.CharField(required=False, label="評語/備注 (e.g. 失敗的原因)", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        final_result = cleaned_data.get("final_result")
        if status != 'on going' and final_result == None:
            raise forms.ValidationError('如目標已完成/失敗，請填寫成果分數。')
        elif status == 'on going' and final_result != None:
            raise forms.ValidationError('如目標仍在進行中，請不要填寫成果分數。')
        return cleaned_data


class TaskForm(forms.Form):
    def __init__(self, subjects, goals, methods, tasks, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.MultipleChoiceField(
            choices=subjects, label="科目", required=False, widget=forms.CheckboxSelectMultiple())

        self.fields['goal'] = forms.MultipleChoiceField(
            choices=goals, label="目標", required=False, widget=forms.CheckboxSelectMultiple())

        self.fields['method'] = forms.MultipleChoiceField(
            choices=methods, label="方法", required=False, widget=forms.CheckboxSelectMultiple())

        self.fields['task'] = forms.MultipleChoiceField(
            choices=tasks, label="任務", required=False, widget=forms.CheckboxSelectMultiple())

    name = forms.CharField(max_length=60, label="任務名稱")
    description = forms.CharField(required=False, label="描述", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    predicted_end_time = forms.DateField(
        widget=DatePickerInput, label="預計完成日期",  input_formats=['%Y-%m-%d'])
    priority = forms.IntegerField(
        min_value=1, max_value=5, label="優先度 (1分代表最次要，5分代表最優先)", required=True)


class TaskEvaluationForm(forms.Form):
    STATUS = [
        ('on going', '進行中 - On Going'),
        ('finished', '完結 - Finished'),
        ('failed', '失敗 - Failed'),
    ]
    status = forms.ChoiceField(choices=STATUS, label="目前狀態")
    priority = forms.IntegerField(
        min_value=1, max_value=5, label="如需更改優先度，請在此更改 (1分代表最次要，5分代表最優先)", required=True)
    completeness = forms.IntegerField(
        min_value=0, max_value=5, label="完成程度 (0分代表沒有開始，5分代表完成)", required=False)
    willingness = forms.IntegerField(
        min_value=0, max_value=5, label="投入程度 (0分代表非常厭惡，5分代表非常享受)", required=False)
    effort = forms.IntegerField(
        min_value=0, max_value=5, label="努力程度 (0分代表沒有沒有努力，5分代表竭盡全力)", required=False)
    time_spent = forms.IntegerField(
        min_value=0, label="用時 (分鐘)", required=False)
    effectiveness = forms.IntegerField(
        min_value=0, max_value=5, label="得著/成果 (0分代表低，5分代表高)", required=False)
    comment = forms.CharField(required=False, label="評語/備注 (e.g. 失敗的原因)", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        effort = cleaned_data.get('effort')
        willingness = cleaned_data.get('willingness')
        effectiveness = cleaned_data.get('effectiveness')
        completeness = cleaned_data.get('completeness')
        time_spent = cleaned_data.get('time_spent')
        if (status == 'finished' or status == 'failed') and (effort is None or willingness is None or effectiveness is None or completeness is None):
            raise forms.ValidationError(
                '如目標已完成/失敗，請填寫努力程度、投入程度、得著/成果和完成程度。')
        return cleaned_data


class CoachingReportForm(forms.ModelForm):
    class Meta:
        model = CoachingReportRecord
        exclude = ['student', 'coach', 'created_at','section']
    
    comment = forms.CharField(required=False, label="Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    duration = forms.IntegerField(
        min_value=0, label="Duration", required=True, help_text='in minutes')


class SAndCRecordForm(forms.ModelForm):

    class Meta:
        model = SAndCRecord
        exclude = ['coaching_report_record']

    critical_thinking_1 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                             label="展現智慧誠信、公正和開放的態度：教練應該觀察學生在做出判斷或決策時是否展現公正的態度，並且在進行思考時能夠正視自身的偏見。此外，教練應該評估學生是否對其思緒或行為的道德後果負責。")
    critical_thinking_2 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                             label="綜合思考和資訊以發現或擴展理解：教練應該觀察學生是否能夠整合相關的資訊和觀點，以支持其思緒、行為或信念。學生應該能夠基於所收集的資訊進行推論或預測，展示其綜合思考能力。")
    critical_thinking_3 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                             label="反思和評估思維、信念或行為背後的推理：教練應該評估學生能否解釋其思維、信念或行為的原因。學生應該能夠考慮到相關背景或納入不同的觀點來評估其思維或行為。")
    critical_thinking_4 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                             label="應用理性方法或相關準則來概念化、分析或做出判斷：教練應該觀察學生是否有效地運用準則來組織、分類或評估資訊。學生應該按照邏輯程序進行推理，以得出合理的結論。他們應該展示出應用理性方法和相關準則的能力。")
    critical_thinking_5 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                             label="質疑和分析證據、主張或假設：教練應該評估學生是否批判性地檢視主張或證據的可靠性、偏見或可信度。學生應該能夠評估證據的相關性、準確性和精確性，展示其質疑假設的分析能力。")
    critical_thinking_comment = forms.CharField(required=False, label="Critical Thinking Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    problem_solving_1 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                           label="以創造力、靈活性和決心應對挑戰：教練應該觀察學生如何適應變化的情況，調整解決問題的計劃，展示其靈活性。學生應該將挫折視為尋找更好解決方案的挑戰，並展示其在解決問題時的創造力。")
    problem_solving_2 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                           label="評估可能解決方案的影響，以執行最可行的選擇：教練應該評估學生如何評估所選解決方案對人際關係或生活品質的影響。學生應該權衡所提出解決方案對社會、政治、文化或環境背景的影響，以確定最可行的選擇。")
    problem_solving_3 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                           label="評估選項以生成行動方案：教練應該觀察學生是否為解決問題或挑戰制定計劃，展示他們評估不同選項的能力。學生還應該展示選擇獨立或合作解決問題的能力，展示其決策能力。")
    problem_solving_4 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                           label="利用相關資訊、資源或準則探索解決問題的策略：教練應該評估學生是否考慮到與問題相關的參數或可用資源。學生應該能夠制定評估解決方案的準則，利用相關資訊和資源探索不同的解決問題策略。")
    problem_solving_5 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                           label="確定問題的已知和所需以進行澄清：教練應該觀察學生是否能夠確定解決問題所需的需求或目標。學生應該展示出將複雜問題分解為較小或更簡單部分的能力，展示其澄清問題需求的技巧。")
    problem_solving_comment = forms.CharField(required=False, label="Problem Solving Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    managing_information_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="有效且符合倫理地使用、分享或儲存資訊：教練應評估學生是否評估資訊如何透過分享來增進體驗、表達或協作。學生應展現對於使用、分享或儲存資訊的正面和負面影響有所了解，同時遵守倫理準則。")
    managing_information_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="評估真實性、可靠性或有效性以適當地解釋或使用資訊：教練應觀察學生是否能夠識別資訊的作者或擁有者，展示他們評估真實性的能力。學生應展現系統性的研究能力，找到可能支持或相互矛盾的資訊來源，使他們能夠做出明智的解釋和決策。")
    managing_information_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="綜合或組織多條資訊以增強或澄清理解：教練應觀察學生是否能夠總結或用自己的話表達資訊中的主要或隱含觀點，展現他們有效綜合資訊的能力。此外，學生應展現組織和呈現資訊的能力，以增強和澄清理解。")
    managing_information_4 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="從各種數位或非數位來源中獲取資訊：教練應評估學生是否能夠從多種數位或非數位來源中搜尋和擷取資訊。學生應展現尋找其他來源以澄清或驗證資訊的能力，展示他們在獲取資訊方面的靈活性和資源利用能力。")
    managing_information_comment = forms.CharField(required=False, label="Managing Information Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    creativity_and_innovation_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="在將想法轉化為行動、產品或服務時展現主動性、足智多謀和毅力：教練應觀察學生是否展現在冒險和追求新想法時的主動性。學生應展現足智多謀和毅力，將想法轉化為行動、產品或服務，展現他們信心十足地實施創新想法的能力。")
    creativity_and_innovation_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="根據反饋或新情況評估和適應想法、材料或過程：教練應評估學生是否根據預期目標評估和調整想法、材料或過程。學生應展現根據不同目的適應想法或創新的能力，展示他們的靈活性和應變能力。")
    creativity_and_innovation_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="探索或玩弄想法、材料或過程以創造新事物：教練應觀察學生如何操作模型、原型或模擬來實驗新想法。學生應展現將材料或資源以獨特方式結合，通過探索和實驗創造新事物的能力，培養他們的創造力。")
    creativity_and_innovation_4 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="辨識機會和想像以新方式應用想法：教練應評估學生是否積極尋找改進想法、物體或情況的機會。學生應展現大膽構思並生成創新方式，創造或轉變物體或情況的能力，展現他們豐富的想像力。")
    creativity_and_innovation_comment = forms.CharField(required=False, label="Creativity and Innovation Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    communication_1 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="在與他人溝通時展現尊重和責任：教練應觀察學生是否支持或激勵那些不願分享知識或觀點的人。學生應承擔責任，以有益於他人的方式進行溝通，展現對不同觀點的尊重，促進建設性的對話。")
    communication_2 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="使用適當的語言、慣例或協議表達想法或概念：教練應評估學生在正式或非正式場合中是否遵守適當的協議。學生應選擇適當的風格、內容和格式來有效地表達訊息，以便在表達自己、提供指示、激勵、說服或分享想法時展現他們的溝通能力。")
    communication_3 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="解讀和詮釋以口語或非口語方式分享的想法或信息:教練應評估學生是否考慮到符號、手勢或詞語的多重含義，展現出準確解讀和詮釋信息的能力。學生應該展示出在解釋口語或非口語溝通時，對上下文和內容的重要性的理解。")
    communication_4 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="在追求共同理解時考慮不同觀點、情感和經歷:教練應評估學生是否從不同觀點、意見或經歷的人那裡獲取信息，豐富自己的理解。學生在表達自己的意見或想法時，應尊重他人的經歷或觀點，促進共情和包容。")
    communication_5 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="在與受眾、背景或文化相關時澄清信息的目的或意圖:教練應評估學生是否根據受眾來確保信息清晰。學生應該意識到他們對信息的解釋可能與其原意不一致，並在需要時主動尋求澄清，考慮到受眾、背景和文化的影響。")
    communication_comment = forms.CharField(required=False, label="Communication Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    collaboration_1 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="重視靈活性、妥協和他人的貢獻，培養良好的工作關係:教練應評估學生在面對變化或挑戰時是否展示出成長的心態。學生應該展示出尊重地表示不同意見、妥協或談判的能力，重視他人的多樣貢獻和觀點，培養良好的工作關係。")
    collaboration_2 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="在分享想法或角色時展示互惠和信任:教練應評估學生是否接受並貢獻想法，以實現共同利益。學生應通過履行自己的責任並贏得團隊的信任，展示出值得信賴的品質，促進基於互惠的合作環境。")
    collaboration_3 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="在與他人合作時對不同文化、受眾或背景保持敏感:教練應評估學生是否承認不同意見或貢獻，以建立包容性的團隊或關係。學生應該仔細傾聽、耐心理解不同文化、受眾或背景下他人的興趣、觀點或意見。")
    collaboration_4 = forms.IntegerField(min_value=1, max_value=6, required=False,
                                         label="共同分擔責任，支持他人實現共同目標:教練應評估學生是否鼓勵團隊成員貢獻他們的觀點、技能或知識。學生應通過共同領導、責任共擔或共同擁有，促進合作，支持他人實現共同目標。")
    collaboration_comment = forms.CharField(required=False, label="Collaboration Comment", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    cultural_and_global_citizenship_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="重視公平和多樣性，並相信能夠產生影響:教練應評估學生是否認識到自己是變革的推動者。學生應該理解在社區中平衡公平和多樣性的重要性，重視包容性，並相信自己能夠產生積極的影響。")
    cultural_and_global_citizenship_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="評估決策或行動對個人或社區的尊嚴和福祉的影響:教練應評估學生如何分析他們的選擇和行動對周圍世界的影響。學生應該能夠確定人類活動對個人和社區福祉的影響程度，展示出責任感和同理心。")
    cultural_and_global_citizenship_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="通過行動為健康和可持續的社區作出貢獻，展示負責任的公民意識:教練應觀察學生如何以模範領導或管理方式促進健康和可持續的社區。學生應願意自愿投入時間和努力，支持本地或全球倡議，積極為創建和維護健康和可持續的環境做出貢獻。")
    cultural_and_global_citizenship_4 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="在文化、環境、政治或經濟體系中分析決策的多種方式:教練應評估學生探索共同或多元利益如何影響決策過程。學生應該展示出納入不同觀點在決策過程中的重要性的理解，考慮到文化、環境、政治或經濟體系中的決策方式。")
    cultural_and_global_citizenship_5 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="在檢視文化、環境、政治或經濟體系與社區之間的互動時考慮多元觀點:教練應觀察學生如何分析價值觀如何影響社區，以及社區如何應對問題以確保納入不同社會和文化身份、角色或利益的能力。學生應展示出在檢視文化、環境、政治或經濟體系與社區之間的互動時考慮多元觀點的能力。")
    cultural_and_global_citizenship_comment = forms.CharField(
        required=False, label="Cultural and Global Citizenship Comment", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    personal_growth_and_wellbeing_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="適應新情況和轉變時展現樂觀、靈活或有韌性:教練應評估學生如何將變革或挑戰視為成長和改進的機會。學生應展示出在適應新情況和轉變時具有樂觀、靈活和韌性的能力，並保持積極的心態。")
    personal_growth_and_wellbeing_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="建立健康關係以支持自我和他人的成長和幸福：教練應觀察學生如何以關心和耐心的態度聆聽他人，展現出有效的溝通技巧。學生應該使用策略來培養情感意識和社交技巧，建立健康的關係，以支持自我和他人的成長和幸福。")
    personal_growth_and_wellbeing_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="做出選擇或採取行動，促進自我或他人的安全和幸福：教練應評估學生如何做出生活方式選擇，例如保持健康的飲食、定期鍛煉、優質睡眠和建立社交關係，對自身幸福有正面影響的能力。學生應該理解使用安全設備並遵守適當程序以確保自身和他人的安全的重要性。")
    personal_growth_and_wellbeing_4 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="探索、選擇或適應支持個人在生活、學校或職業生涯中成長的策略和資源：教練應觀察學生如何積極尋求支持他個人、學習或職業目標的人或機會。學生應展示出發展個人習慣以促進自身幸福和整體成功的能力，同時探索、選擇或適應支持個人在生活、學校或職業生涯各方面成長的策略和資源。")
    personal_growth_and_wellbeing_5 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="確定興趣、價值觀或技能，設定學習、生活或職業目標：教練應評估學生如何基於自我反思創建切實可行和相關的目標。學生應該展示出確定興趣、價值觀和技能的能力，並將其作為設定有意義的學習、生活或職業目標的基礎。此外，學生應積極探索在學習、社區或工作環境中實現個人成長的機會。")
    personal_growth_and_wellbeing_comment = forms.CharField(
        required=False, label="Personal Growth and Wellbeing Comment", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))

    def save(self,  coaching_report_record=None):

        instance = super().save(commit=False)
        if coaching_report_record:
            instance.coaching_report_record = coaching_report_record

        instance.save()

        return instance


class AcademicCoachingRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicCoachingRecord
        exclude = ['coaching_report_record']
    learning_strategy_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 理解自己的學習風格和偏好。")

    learning_strategy_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 為筆記、學習和考試制定有效的策略。")
    learning_strategy_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 定期反思學習策略並進行調整。")
    learning_strategy_comment = forms.CharField(required=False, label="學習策略 - Learning Strategy Comment",
                                                widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    goal_setting_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 設定具體、可衡量、可達成、相關且有時間限制（SMART）的目標。")
    goal_setting_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 將目標分解為較小的可行步驟。")
    goal_setting_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 定期監控目標進度並進行調整。")
    goal_setting_comment = forms.CharField(required=False, label="目標設定 - Goal Setting Comment",
                                           widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    organising_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 有效地定義和澄清任務/項目要求，並根據能力和偏好在團隊成員間分配任務。")
    organising_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 利用資源，如線上工具和連線，以支援任務完成。")
    organising_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 從各種來源中提取重要見解並有系統地管理信息。")
    organising_comment = forms.CharField(required=False, label="組織管理 - Organising Comment",
                                         widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    motivation_and_accountability_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 顯示自我激勵並對他們的學業進度負責。")
    motivation_and_accountability_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 為自己設定高標準並追求卓越。")
    motivation_and_accountability_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 需要時尋找並利用適當的支援系統，如教師或導師。")
    motivation_and_accountability_comment = forms.CharField(
        required=False, label="動機與責任 - Motivation and Accountability Comment", widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    time_management_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 對學術任務進行有效的優先排序和時間分配。")
    time_management_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 使用策略來減少拖延並最大化生產力。")
    time_management_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 管理時間承諾並與其他責任平衡學術工作量。")
    time_management_comment = forms.CharField(required=False, label="時間管理 - Time Management Comment",
                                              widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))
    life_balance_1 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="1. 在學術追求和個人健康之間保持健康的平衡。")
    life_balance_2 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="2. 參與對個人成長和幸福有貢獻的課外活動和/或愛好。")
    life_balance_3 = forms.IntegerField(
        min_value=1, max_value=6, required=False, label="3. 有效地認識和管理壓力。")
    ife_balance_comment = forms.CharField(required=False, label="生活平衡 - Life Balance Comment",
                                          widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))

    def save(self,  coaching_report_record=None):

        instance = super().save(commit=False)
        if coaching_report_record:
            instance.coaching_report_record = coaching_report_record

        instance.save()

        return instance


class FinalEvaluationForm(forms.ModelForm):
    class Meta:
        model = FinalEvaluation
        exclude = ['student', 'coach', 'created_at']

    q1 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="培導計畫對於你的整體學術表現和學習經驗帶來了多大的正面影響？")
    q2 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="請對培導計畫中所教授的學習策略和技巧進行評分。")
    q3 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="你對於繼續使用培導計畫中所教授的學習策略和技巧有多少可能性？")
    q4 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="培導計畫對於你實現長期學術目標的效果有多大？")
    q5 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="培導計畫對於你實現長期職業目標的效果有多大？")
    q6 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="培導計畫在你的壓力管理和心理健康支持方面提供了多少幫助？")
    q7 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="培導計畫所提供的反饋和指導對於你的進步和改善領域有多有用？")
    q8 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="你對於培導計畫整體的滿意度有多高？")
    q9 = forms.IntegerField(min_value=1, max_value=6,
                            required=True, label="你有多大可能向他人推薦這個培導計畫？")
    q10 = forms.CharField(required=False, label=" 你認爲培導計劃中能增加什麽内容/有什麽需要改善的地方？", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        label="請輸入舊密碼",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(
        required=True,
        label="請輸入新密碼",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(
        required=True,
        label="請確認新密碼",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))


class ECAForm(forms.Form):
    def __init__(self, eca, *args, **kwargs):
        super(ECAForm, self).__init__(*args, **kwargs)
        self.fields['eca'] = forms.ChoiceField(
            choices=eca, label="課外活動列表",
            widget=forms.Select())

    others = forms.CharField(
        required=False,
        label="新增其他課外活動",
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols': 40, 'style': 'resize:none;'}))

    def clean(self):
        cleaned_data = super().clean()
        selected_eca = cleaned_data.get("eca")
        others = cleaned_data.get("others")
        if selected_eca == "其他課外活動" and others == "":
            raise forms.ValidationError(
                "如你希望新增其他課外活動，請填寫其他課外活動欄位。")
        elif selected_eca != "其他課外活動" and others != "":
            raise forms.ValidationError(
                "請從課外活動列表中選擇希望新增的課外活動。")
        return cleaned_data
    

class QualificationForm(forms.Form):
    def __init__(self, qualification, *args, **kwargs):
        super(QualificationForm, self).__init__(*args, **kwargs)
        self.fields['qualification'] = forms.ChoiceField(
            choices=qualification, label = "資格列表", 
            widget=forms.Select())
    
    others = forms.CharField(
        required=False,
        label="新增其他資格",
        widget=forms.Textarea(
            attrs={'rows': 1, 'cols': 40, 'style': 'resize:none;'}))
    
    def clean(self):
        cleaned_data = super().clean()
        selected_qualification = cleaned_data.get("qualification")
        others = cleaned_data.get("others")
        if selected_qualification == "其他資格" and others == "":
            raise forms.ValidationError(
                "如你希望新增其他資格，請填寫其他資格欄位")
        elif selected_qualification != "其他資格" and others != "":
            raise forms.ValidationError(
                "請從資格列表中選擇希望新增的資格")
        return cleaned_data


class SubjectGradeForm(forms.Form):

    record_date = forms.DateField(required=False, widget=DatePickerInput, label="記錄日期",

                                  input_formats=['%Y-%m-%d'], initial=datetime.now())

    def __init__(self, subjects, *args, **kwargs):

        super(SubjectGradeForm, self).__init__(*args, **kwargs)

        for (subject_id, subject_name) in subjects:

            choices = [('N/A', 'N/A'), ('P', 'Pass'), ('F', 'Fail'), ('U', 'U'), ('1', '1'), ('2', '2'),

                       ('3', '3'), ('4', '4'), ('5', '5'), ('5*', '5*'), ('5**', '5**')]

            # Create a field for each subject with grade choices

            self.fields[subject_name] = forms.ChoiceField(

                required=False,

                label=subject_name,

                choices=choices,

                widget=forms.Select,

            )

    comment = forms.CharField(required=False, label="評語/備注 (e.g. 失敗的原因)", widget=forms.Textarea(
        attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}))


class UserRoleForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('coach', 'Coach'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(
        attrs={'class': 'form-control'}))

    def __init__(self, username, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        self.fields['role'].label = username

    class Meta:
        model = User
        fields = ['role']


class CoachStudentSelectForm(forms.Form):
    def __init__(self, students, coach, *args, **kwargs):
        super(CoachStudentSelectForm, self).__init__(*args, **kwargs)
        self.coach = coach
        self.students = students
        students_with_coaches = CoachStudentMapping.objects.filter(
            student_id__in=students).values_list('student_id', flat=True)
        choices = [
            (student.id,
             f"{student.name} {student.name_chinese} ({student.username})")
            for student in students if student.id not in students_with_coaches]
        self.fields['student'] = forms.ChoiceField(
            required=False,
            label="Available Students",
            choices=choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
        )


class StudentForm(forms.Form):
    def __init__(self, coach, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        students = User.objects.filter(role='student')
        coach.students = CoachStudentMapping.objects.filter(
            coach_id=coach.id).values_list('student_id', flat=True)
        choices = [
            (student.id,
             f"{student.name} {student.name_chinese} ({student.username})")
            for student in students if student.id in coach.students]
        self.fields['student'] = forms.ChoiceField(
            label="Please Select Student",
            choices=choices,
            widget=forms.Select(attrs={'class': 'form-control'}),
        )


class StudyMethodFilterForm(forms.Form):
    social_style_choices = [(4,'任何風格'), (0,'分析型'),(1,'友善型'),(2,'推動型'),(3,'表達型')]
    social_style = forms.ChoiceField(
        label="請選擇你的社交風格",
        choices=social_style_choices, 
        widget=forms.Select())
    time_consumption_choices = [('All','任何時間'), ('Low','低'),('Middle','中'),('High','高')]
    time_consumption = forms.ChoiceField(
        label="請選擇你的溫習時長",
        choices=time_consumption_choices,
        widget=forms.Select())
    def __init__(self, subjects, focuses, *args, **kwargs):
        super(StudyMethodFilterForm, self).__init__(*args, **kwargs)
        self.fields['subject'] = forms.ChoiceField(
            label="請選擇你的科目",
            choices=subjects,
            widget=forms.Select())
        self.fields['study_focus'] = forms.ChoiceField(
            label="請選擇你的學習重點",
            choices=focuses,
            widget=forms.Select())


class StudyMethodAddForm(forms.Form):
    def __init__(self, subjects, goals, *args, **kwargs):
        super(StudyMethodAddForm, self).__init__(*args, **kwargs)
        self.fields['goal'] = forms.ChoiceField(
            label="請選擇方法有助的目標",
            choices=goals,
            widget=forms.Select(),
            required=False)
        self.fields['subject'] = forms.MultipleChoiceField(
            label="請選擇方法有助的科目",
            choices= subjects,
            widget=forms.CheckboxSelectMultiple(),
            required=False)
    personalization = forms.CharField(
        label="請輸入你的個人化學習方法",
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}),
        required=False)
    

class StudyMethodEvaluationForm(forms.Form):
    personalization = forms.CharField(
        label="你的個人化學習方法",
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}),
        required=False)
    suitable = forms.IntegerField(
        label="請輸入你認為此方法對你的適合度 (0分代表非常不適合, 5分代表非常適合)",
        min_value=0,
        max_value=5)
    willingness = forms.IntegerField(
        label="請輸入你認為此方法對你的投入程度 (0分代表非常不投入, 5分代表非常投入)",
        min_value=0,
        max_value=5)
    comment = forms.CharField(
        label="評語/備注 (e.g. 失敗的原因)",
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40, 'style': 'resize:none;'}),
        required=False)
    status = forms.ChoiceField(
        label="請選擇如果處理此方法",
        choices=[('0','延續'),('1','完結'),('2','放棄')],
        widget=forms.Select())


def generate_schema(form_class):
  schema = {
    "type": "object",
    "properties": {}    
  }
  required = []
  for name, field in form_class.base_fields.items():
    schema["properties"][name] = {}

    if isinstance(field, forms.ChoiceField):
      schema["properties"][name]["type"] = "string"
      schema["properties"][name]["enum"] = [k for k,v in field.choices]

    elif isinstance(field, forms.MultipleChoiceField):
      schema["properties"][name]["type"] = "array"
      schema["properties"][name]["items"] = {"type": "string"}

    elif isinstance(field, forms.IntegerField):
      schema["properties"][name]["type"] = "integer"
      if field.min_value:
        schema["properties"][name]["minimum"] = field.min_value  
      if field.max_value:  
        schema["properties"][name]["maximum"] = field.max_value

    elif isinstance(field, forms.CharField):
      schema["properties"][name]["type"] = "string"
      if field.max_length:
        schema["properties"][name]["maxLength"] = field.max_length

    elif isinstance(field, forms.EmailField):
      schema["properties"][name]["type"] = "string"
      schema["properties"][name]["format"] = "email"

    elif isinstance(field, forms.DateField):
      schema["properties"][name]["type"] = "string"
      schema["properties"][name]["format"] = "date"

    elif isinstance(field, forms.TimeField):
      schema["properties"][name]["type"] = "string"
      schema["properties"][name]["format"] = "time"
      
  if field.required:
        required.append(name)



      

  if required:
    schema["required"] = required

#   # Get initial data
#   initial = form_class.initial  
#   if form_class.instance:
#     initial = forms.model_to_dict(form_class.instance)

#   # Populate default values  
#   for name, value in initial.items():
#     if name in schema['properties']:
#       schema['properties'][name]['default'] = value

  return schema