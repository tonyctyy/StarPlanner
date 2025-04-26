export interface Options {
    value: string;
    label: string;
}

export interface User {
    id: number;
    username: string;
    email: string;
    name: string;
    name_chinese: string;
    role: string;
    phase: number;
}

export interface Profile {
    tasks: Task[]
    goals: Goal[]
    methods: Method[]
    subjects: Subject[]
}

interface GoalEvaluate {
    comment: string;
    effort: number;
    goal: number;
    id: number;
    progress: number;
}

export interface Goal {
    predicted_end_time: string;
    id: number,
    name: string,
    progress: number,
    description: string | null,
    difficulty: string,
    goal_status: string,
    goal_type: string,
    end_at: string,
    parent: Goal | null,
    display_difficulty: string,
    display_goal_type: string,
    final_result: number | null,
    goal_evaluate: GoalEvaluate | null,
    
}

export interface Method {
    id: number,
    name: string,
    subject: Subject[],
    description: string,
}

export interface Task {
    id: number,
    name: string,
    description: string,
    priority: number,
    subject: Subject[],
    predicted_end_time: string,
    end_at: string,
    goals: Goal[],
    methods: Method[],
    tasks: Task[],
    status: string,
    willingness: number | null,
    completeness: number | null,
    effort: number | null,
    effectiveness: number | null,
    comment: string | null,
    time_spent: number | null,

}

export interface Social_Style{
    id: number,
    user: number,
    driver: number,
    amiable: number,
    analytical: number,
    expressive: number,
    created_at: string,
}

export interface Subject {
    id: number,
    name: string,
    name_chin: string,
    name_abbr: string,
    display_name: string,
}

export interface Session_Report {
    id: number,
    student: number,
    coach: number,
    comment: string,
    phase: number,
    section: number,
    duration: number,
    coaching_date: string,
    created_at: string,
    ACRecord: ACRecord,
    SAndCRecord: SCRecord,
}

export interface ACRecord {
    [key: string]: any;
    id: number,
    coaching_report_record: number;
    learning_strategy_1: number;
    learning_strategy_2: number;
    learning_strategy_3: number;
    learning_strategy_comment: string;
    goal_setting_1: number;
    goal_setting_2: number;
    goal_setting_3: number;
    goal_setting_comment: string;
    organising_1: number;
    organising_2: number;
    organising_3: number;
    organising_comment: string;
    motivation_and_accountability_1: number;
    motivation_and_accountability_2: number;
    motivation_and_accountability_3: number;
    motivation_and_accountability_comment: string;
    time_management_1: number;
    time_management_2: number;
    time_management_3: number;
    time_management_comment: string;
    life_balance_1: number;
    life_balance_2: number;
    life_balance_3: number;
    life_balance_comment: string;
    comment: string;
}

export interface SCRecord {
    [key: string]: any;
    id: number;
    coaching_report_record: number;
    critical_thinking_1: number;
    critical_thinking_2: number;
    critical_thinking_3: number;
    critical_thinking_4: number;
    critical_thinking_5: number;
    critical_thinking_comment: string;
    
    problem_solving_1: number;
    problem_solving_2: number;
    problem_solving_3: number;
    problem_solving_4: number;
    problem_solving_5: number;
    problem_solving_comment: string;
    
    managing_information_1: number;
    managing_information_2: number;
    managing_information_3: number;
    managing_information_4: number;
    managing_information_comment: string;
    
    creativity_and_innovation_1: number;
    creativity_and_innovation_2: number;
    creativity_and_innovation_3: number;
    creativity_and_innovation_4: number;
    creativity_and_innovation_comment: string;
    
    communication_1: number;
    communication_2: number;
    communication_3: number;
    communication_4: number;
    communication_5: number;
    communication_comment: string;
    
    collaboration_1: number;
    collaboration_2: number;
    collaboration_3: number;
    collaboration_4: number;
    collaboration_comment: string;
    
    cultural_and_global_citizenship_1: number;
    cultural_and_global_citizenship_2: number;
    cultural_and_global_citizenship_3: number;
    cultural_and_global_citizenship_4: number;
    cultural_and_global_citizenship_5: number;
    cultural_and_global_citizenship_comment: string;
    
    personal_growth_and_wellbeing_1: number;
    personal_growth_and_wellbeing_2: number;
    personal_growth_and_wellbeing_3: number;
    personal_growth_and_wellbeing_4: number;
    personal_growth_and_wellbeing_5: number;
    personal_growth_and_wellbeing_comment: string;

    comment: string;
}

export interface Final_Report_Modal{
    model: string,
    model_chinese: string,
    score: number,
    comment: string,
}

export interface SAndCModelScores{
    critical_thinking: string[],
    problem_solving: string[],
    managing_information: string[],
    creativity_and_innovation: string[],
    communication: string[],
    collaboration: string[],
    cultural_and_global_citizenship: string[],
    personal_growth_and_wellbeing: string[],
}

export interface ACModelScores{
    goal_setting: string[],
    learning_strategy: string[],
    life_balance: string[],
    motivation_and_accountability: string[],
    organising: string[],
    time_management: string[],
}

export interface Final_Report_Comment{
    comment_list: Final_Report_Modal[],
}

export interface Final_Report{
    [key: string]: any;
    id: number,
    phase: number,
    student: User,
    coach: User,
    s_and_c_list: Final_Report_Modal[],
    s_and_c_scores: SAndCModelScores,
    ac_list: Final_Report_Modal[],
    ac_scores: ACModelScores,
    // subject_list: 
    before_social_style: Social_Style,
    after_social_style: Social_Style,
    social_style_type: string,
    social_style_comment: string,
    critical_thinking_score: number,
    critical_thinking_comment: string,
    problem_solving_score: number,
    problem_solving_comment: string,
    managing_information_score: number,
    managing_information_comment: string,
    creativity_and_innovation_score: number,
    creativity_and_innovation_comment: string,
    communication_score: number,
    communication_comment: string,
    collaboration_score: number,
    collaboration_comment: string,
    cultural_and_global_citizenship_score: number,
    cultural_and_global_citizenship_comment: string,
    personal_growth_and_wellbeing_score: number,
    personal_growth_and_wellbeing_comment: string,

    critical_thinking_1: number,
    critical_thinking_2: number,
    critical_thinking_3: number,
    critical_thinking_4: number,
    critical_thinking_5: number,
    
    problem_solving_1: number,
    problem_solving_2: number,
    problem_solving_3: number,
    problem_solving_4: number,
    problem_solving_5: number,
    
    managing_information_1: number,
    managing_information_2: number,
    managing_information_3: number,
    managing_information_4: number,
    
    creativity_and_innovation_1: number,
    creativity_and_innovation_2: number,
    creativity_and_innovation_3: number,
    creativity_and_innovation_4: number,
    
    communication_1: number,
    communication_2: number,
    communication_3: number,
    communication_4: number,
    communication_5: number,
    
    collaboration_1: number,
    collaboration_2: number,
    collaboration_3: number,
    collaboration_4: number,
    
    cultural_and_global_citizenship_1: number,
    cultural_and_global_citizenship_2: number,
    cultural_and_global_citizenship_3: number,
    cultural_and_global_citizenship_4: number,
    cultural_and_global_citizenship_5: number,
    
    personal_growth_and_wellbeing_1: number,
    personal_growth_and_wellbeing_2: number,
    personal_growth_and_wellbeing_3: number,
    personal_growth_and_wellbeing_4: number,
    personal_growth_and_wellbeing_5: number,
    
    learning_strategy_score: number,
    learning_strategy_comment: string,
    goal_setting_score: number,
    goal_setting_comment: string,
    organising_score: number,
    organising_comment: string,
    motivation_and_accountability_score: number,
    motivation_and_accountability_comment: string,
    time_management_score: number,
    time_management_comment: string,
    life_balance_score: number,
    life_balance_comment: string,

    learning_strategy_1: number,
    learning_strategy_2: number,
    learning_strategy_3: number,

    goal_setting_1: number,
    goal_setting_2: number,
    goal_setting_3: number,

    organising_1: number,
    organising_2: number,
    organising_3: number,
   
    motivation_and_accountability_1: number,
    motivation_and_accountability_2: number,
    motivation_and_accountability_3: number,

    time_management_1: number,
    time_management_2: number,
    time_management_3: number,
    
    life_balance_1: number,
    life_balance_2: number,
    life_balance_3: number,

    subject_comment: string,
}

export interface GoalModalProps {
    goal: Goal | null;
    isEdit: boolean;
    GOAL_OPTIONS: Options[];
}

export interface TaskModalProps {
    task: Task | null;
    isEdit: boolean;
    GOAL_OPTIONS: Options[];
    TASK_OPTIONS: Options[];
    SUBJECT_OPTIONS: Options[];
    METHOD_OPTIONS: Options[];
}

export interface ReportModalProps {
    report: Session_Report | null;
    isEdit: boolean;
    sessionNum: number;
}
 
export interface FinalSocialStyle {
    id: number,
    before_social_style: number,
    after_social_style: number,
    social_style_type: string,
    social_style_comment: string,
}

export interface FinalSocialStyleProps {
    finalSocialStyle: FinalSocialStyle;
    social_styles: Social_Style[];
}

export interface ACProps {
    ACRecord: ACRecord;
    isFinal: boolean;
}

export interface SCProps {
    SCRecord: SCRecord;
}

export interface idProps {
    id: number;
}

export interface RadarChartData {
    labels: string[];
    pre_values: number[];
    post_values: number[];
}

export interface CommentSelectData{
    [key: string]: { [key: string]: string[] };
    ac: {
        learning_strategy_comment: string[],
        goal_setting_comment: string[],
        organising_comment: string[],
        motivation_and_accountability_comment: string[],
        time_management_comment: string[],
        life_balance_comment: string[],
    };
    sc: {
        critical_thinking_comment: string[],
        problem_solving_comment: string[],
        managing_information_comment: string[],
        creativity_and_innovation_comment: string[],
        communication_comment: string[],
        collaboration_comment: string[],
        cultural_and_global_citizenship_comment: string[],
        personal_growth_and_wellbeing_comment: string[],
    };
    report: {
        comment: string[],
    };
}

export interface SubjectComment{
    id: number,
    subject_comment: string,
    report_dashboard: number,
    subject: number,
    subject_display_name: string,
}

export interface Pre_ACRecord{
    id: number,
    coach: number,
    student: number,
    phase: number,
    learning_strategy: number,
    goal_setting: number,
    organising: number,
    motivation_and_accountability: number,
    time_management: number,
    life_balance: number,
}