import React, { useState, useEffect } from 'react';
import { addGoal, addTask, addSessionReport, editSessionReport, getSessionReport, addSocialStyle, editFinalReport, addSubjectComment, editSubjectComment} from '../API';
import {GOAL_TYPE, DIFFICULTY, PRIORITY, GoalModalForm, TaskModalForm, ReportModalForm, SocialStyleScoreForm, SOCIAL_STYLE_OPTIONS} from '../Constants';
import {GoalModalProps, TaskModalProps, ReportModalProps, FinalSocialStyleProps, Subject, SubjectComment} from '../Interface';
import {Modal, } from '../styles/style.const'
import moment from 'moment';


// Goal Modal component
export const GoalModal: React.FC<GoalModalProps> = ({goal, isEdit, GOAL_OPTIONS}) => {
    const [formData, setFormData] = useState(GoalModalForm);
    const [errors, setErrors] = useState([] as any[]);
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (localStorage.getItem('student_id') === null){
            newErrors.push({message: '請先選擇學生'});
            hasError = true;
        }
        else if(formData.name === "") {
            newErrors.push( {message: '請輸入目標名稱'});
            hasError = true;
            }
        else if (formData.predicted_end_time === "") {
            newErrors.push({message: '請輸入預計結束時間'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        addGoal(formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }
    return (
    <Modal>
        <form onSubmit={handleSubmit}>
        <label className='label'>目標名稱: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}  
        />
        <br></br>
        <label className='label'>描述: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}  

        />
        <br></br>
        <label className='label'>所屬目標: </label>
        <select
            className='modalSelect'
            value={formData.goal_id}
            onChange={(e) => setFormData({...formData, goal_id: e.target.value})}  
        >
            {GOAL_OPTIONS.map(option => (
                <option key={option.value} value={option.value}>
                {option.label}  
                </option>
            ))}
        </select>
        <br></br>
        <label className='label'>目標種類: </label>
        <select
            className='modalSelect'
            value={formData.goal_type}
            onChange={(e) => setFormData({...formData, goal_type: e.target.value})}  
        >
        {GOAL_TYPE.map(option => (
            <option key={option.value} value={option.value}>
            {option.label}  
            </option>
        ))}
        </select>
        <br></br>
        <label className='label'>難度: </label>
        <select
            className='modalSelect'
            value={formData.difficulty}
            onChange={(e) => setFormData({...formData, difficulty: e.target.value})}  
        >
            {DIFFICULTY.map(option => (
                <option key={option.value} value={option.value}>
                {option.label}  
                </option>
            ))}
        </select>
        <br></br>
        <label className='label'>預計結束時間: </label>
        <input
            type="date"
            className="modalTextInput-single"
            value={formData.predicted_end_time}
            onChange={(e) => 
                setFormData({
                    ...formData,  
                    predicted_end_time: e.target.value
                })
            }
        />
        <br></br>
        <button
            type="submit"
            className="modalButton" 
        >
        新增目標
        </button>
        <br></br>
        {errors.map(error => (
        <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
        ))}
        </form>
    </Modal>
    )
}


// Task Modal component
export const TaskModal: React.FC<TaskModalProps> = ({task, isEdit, GOAL_OPTIONS, TASK_OPTIONS, SUBJECT_OPTIONS, METHOD_OPTIONS}) => {
    const [formData, setFormData] = useState(TaskModalForm);
    const [errors, setErrors] = useState([] as any[]);
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        // console.log(formData);
        let hasError = false;
        const newErrors = [];
        if (localStorage.getItem('student_id') === null){
            newErrors.push({message: '請先選擇學生'});
            hasError = true;
        }
        else if(formData.name === "") {
            newErrors.push( {message: '請輸入任務名稱'});
            hasError = true;
            }
        else if (formData.predicted_end_time === "") {
            newErrors.push({message: '請輸入預計結束時間'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        addTask(formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }
    return (
    <Modal>
        <form onSubmit={handleSubmit}>
        <label className='label'>任務名稱: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.name}
            onChange={(e) => setFormData({...formData, name: e.target.value})}  
        />
        <br></br>
        <label className='label'>描述: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.description}
            onChange={(e) => setFormData({...formData, description: e.target.value})}  

        />
        <br></br>
        <label className='label'>預計結束時間: </label>
        <input
            type="date"
            className="modalTextInput-single"
            value={formData.predicted_end_time}
            onChange={(e) => 
                setFormData({
                    ...formData,  
                    predicted_end_time: e.target.value
                })
            }
        />
        <br></br>
        <label className='label'>優先度: </label>
        <select
            className='modalSelect'
            value={formData.priority}
            onChange={(e) => setFormData({...formData, priority: parseInt(e.target.value)})}
        >
        {PRIORITY.map(option => (
            <option key={option.value} value={option.value}>
                {option.label}  
            </option>
        ))}
        </select>
        <br></br>
        <label className='label'>科目: </label>
        <select
            className='modalSelect'
            value={formData.subject_id}
            onChange={(e) => setFormData({...formData, subject_id: e.target.value})}
        >
        {SUBJECT_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
                {option.label}  
            </option>
        ))}
        </select>
        <br></br>
        <label className='label'>目標: </label>
        <select
            className='modalSelect'
            value={formData.goal_id}
            onChange={(e) => setFormData({...formData, goal_id: e.target.value})}
        >
        {GOAL_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
                {option.label}  
            </option>
        ))}
        </select>
        <br></br>
        {/* <label className='label'>方法: </label>
        <select
            className='modalSelect'
            value={formData.method_id}
            onChange={(e) => setFormData({...formData, method_id: e.target.value})}
        >
        {METHOD_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
                {option.label}  
            </option>
        ))}
        </select>
        <br></br> */}
        <label className='label'>任務: </label>
        <select
            className='modalSelect'
            value={formData.task_id}
            onChange={(e) => setFormData({...formData, task_id: e.target.value})}
        >
        {TASK_OPTIONS.map(option => (
            <option key={option.value} value={option.value}>
                {option.label}  
            </option>
        ))}
        </select>


        <button
            type="submit"
            className="modalButton" 
        >
        新增任務
        </button>
        <br></br>
        {errors.map(error => (
        <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
        ))}
        </form>
    </Modal>
    )
}


// Session Report Modal component
export const ReportModal: React.FC<ReportModalProps> = ({report, isEdit, sessionNum}) => {
    const [formData, setFormData] = useState(ReportModalForm);
    const [errors, setErrors] = useState([] as any[]);
    const button_test = isEdit ?'儲存變更' : '提交報告'
    useEffect(() => {
        if (isEdit && report) {
            setFormData({
                ...formData,
                section: report.section,
                coaching_date: new Date(report.coaching_date).toISOString().split('T')[0],
                comment: report.comment !== null ? report.comment : '',
                duration: report.duration !== null? report.duration: 0,
            });
        } else {
            setFormData({
                ...formData,
                section: sessionNum,
                coaching_date: new Date().toISOString().split('T')[0]
            });
        }
    }, [isEdit, report, sessionNum]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (localStorage.getItem('student_id') === null){
            newErrors.push({message: '請先選擇學生'});
            hasError = true;
        }
        else if (formData.section <=0 || formData.section > 15) {
            newErrors.push({message: '請輸入有效節數 (1-15)'});
            hasError = true;
        }
        else if(formData.duration <=0) {
            newErrors.push( {message: '請輸入有效時長'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        if (isEdit && report){
            editSessionReport(report.id, formData)
                .then(() => {     
                sessionStorage.removeItem(`session-report-${report.id}`);
                getSessionReport(report.id.toString())
                    .then((data) => 
                    {
                        sessionStorage.setItem(`session-report-${report.id}`, JSON.stringify(data));
                    }
                )
            })
        }
        else{
            addSessionReport(formData).then(
                ()=>{
                    window.location.reload();
                }
            );
        }
    }
    return (
        <Modal>
            <form onSubmit={handleSubmit}>
            <label className='label'>培導節數: </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.section}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        section: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <label className='label'>培導日期: </label>
            <input
                type="date"
                className="modalTextInput-single"
                value={formData.coaching_date}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        coaching_date: e.target.value
                    })
                }
            />
            <br></br>
            <label className='label'>時長 (分鐘): </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.duration}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        duration: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <label className='label'>評語: </label>
            <textarea
                className="modalTextInput"
                value={formData.comment}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        comment: e.target.value
                    })
                }
            />
            <br></br>
            <button
                type="submit"
                className="modalButton"
            >
            {button_test}
            </button>
            <br></br>
            {errors.map(error => (
            <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
            ))}
            </form>
        </Modal>
    )
}


export const SubjectCommentModal: React.FC<{subjects: Subject[], subject_comments: SubjectComment[], report_id: number, general_comment: string}> = ({subjects, subject_comments, report_id, general_comment}) => {
    const [formData, setFormData] = useState({subject: -1, comment: '', subject_display_name: ''});
    const [errors, setErrors] = useState([] as any[]);
    const [isEdit, setIsEdit] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (formData.subject === -1){
            newErrors.push({message: '請選擇科目'});
            hasError = true;
        }
        else if (formData.comment === ''){
            newErrors.push({message: '請輸入科目評語'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        if (isEdit){
            // Edit subject comment
            editSubjectComment(report_id, formData).then(
                ()=>{window.location.reload();}
            );
        }
        else {
            // Add subject comment
            addSubjectComment(report_id, formData).then(
                ()=>{window.location.reload();}
            );
        }
    }

    // Update comment when subject changes
    useEffect(() => {
        // Find the subject comment for the selected subject
        const matchingComment = subject_comments.find(comment => comment.subject === formData.subject);
        // Update the comment in the form data
        if (matchingComment || formData.subject === 0) {
            setIsEdit(true);
            if (matchingComment){
                setFormData(prevFormData => ({
                    ...prevFormData,
                    comment: matchingComment.subject_comment
                }));
            }
            else {
                if (general_comment !== null){
                setFormData(prevFormData => ({
                    ...prevFormData,
                    comment: general_comment
                }));
                }
                else{
                    setFormData(prevFormData => ({
                        ...prevFormData,
                        comment: ''
                    }));
                }
            }
        }
        else {
            setIsEdit(false);
            setFormData(prevFormData => ({
                ...prevFormData,
                comment: ''
            }));
        }
        console.log(subject_comments)
    }, [formData.subject, subject_comments]);

    return (
        <Modal>
            <form onSubmit={handleSubmit}>
                <label className='label'>科目: </label>
                <select
                    className='modalSelect'
                    value={formData.subject}
                    onChange={(e) => setFormData({...formData, subject: parseInt(e.target.value)})}
                >
                    <option key="-1" value="-1">請選擇科目</option>
                    <option key="0" value="0">整體評語</option>
                    {subjects.map(option => (
                        <option key={option.id} value={option.id}>
                            {option.display_name}
                        </option>
                    ))}
                </select>
                <br />
                <label className='label'>科目評語: </label>
                <textarea
                    className="modalTextInput"
                    value={formData.comment}
                    onChange={(e) => setFormData({...formData, comment: e.target.value})}
                />
                <br />
                <button
                    type="submit"
                    className="modalButton"
                >
                    提交科目評語
                </button>
                <br />
                {errors.map(error => (
                    <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
                ))}
            </form>
        </Modal>
    );
};



export const SocialStyleModal: React.FC<FinalSocialStyleProps> = ({finalSocialStyle, social_styles}) => {
    const [formData, setFormData] = useState(finalSocialStyle);
    const [errors, setErrors] = useState([] as any[]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (localStorage.getItem('student_id') === null){
            newErrors.push({message: '請先選擇學生'});
            hasError = true;
        }
        else if (formData.after_social_style === -1){
            newErrors.push({message: '請選擇待人處事風格'});
            hasError = true;
        }
        else if (formData.social_style_type === ""){
            newErrors.push({message: '請輸入待人處事風格'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        editFinalReport('social_style', formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }

    return (
        <Modal>
            <form onSubmit={handleSubmit}>
                {social_styles.length > 0 && (
                    <>
                    <label className='label'>請選擇記錄: </label>
                    <select
                        className='modalSelect'
                        value={formData.after_social_style}
                        onChange={(e) => setFormData({...formData, after_social_style: parseInt(e.target.value)})}
                    >
                    <option key="-1" value="-1">請選擇待人處事風格</option>
                    {social_styles.map(option => (
                        <option key={option.id} value={option.id}>
                            {moment(option.created_at).format('DD/MM/YYYY')}  -  {option.analytical}/{option.amiable}/{option.expressive}/{option.driver} (分析型/友善型/表達型/推動型)
                        </option>
                    ))}
                    </select>
                    <br/>
                    <label className='label'>待人處事風格(e.g. 友善推動型(高度友善，低度推動)): </label>
                    <input 
                        type="text"
                        className="modalTextInput-single"  
                        value={formData.social_style_type}
                        onChange={(e) => setFormData({...formData, social_style_type: e.target.value})}
                    />
                    <label className='label'>評語: </label>
                    <textarea 
                        className="modalTextInput"
                        value={formData.social_style_comment}
                        onChange={(e) => 
                            setFormData({
                                ...formData,  
                                social_style_comment: e.target.value
                            })
                        }
                    />
                    <br></br>
                    <button
                        type="submit"
                        className="modalButton"
                    >
                    儲存待人處事風格
                    </button>
                    <br></br>
                    {errors.map(error => (
                    <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
                    ))}
                    </>
                )}
            </form>

        </Modal>
    )

}


// Social Style Score Modal Component 
export const SocialStyleScoreModal = () => {
    const [formData, setFormData] = useState(SocialStyleScoreForm);
    const [errors, setErrors] = useState([] as any[]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (localStorage.getItem('student_id') === null){
            newErrors.push({message: '請先選擇學生'});
            hasError = true;
        }
        else if (formData.analytical + formData.amiable + formData.expressive + formData.driver !== 100){
            newErrors.push({message: '請確保四種分數總和為100'});
            hasError = true;
            }
        else if (formData.analytical % 5 !== 0 || formData.amiable % 5 !== 0 || formData.expressive % 5 !== 0 || formData.driver % 5 !== 0){
            newErrors.push({message: '請確保四種分數為5的倍數'});
            hasError = true;
            }    
        if (hasError){
            setErrors(newErrors);
            return;
        }
        addSocialStyle(formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }


    return (
        <Modal>
            <form onSubmit={handleSubmit}>
            <label className='label'>分析型: </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.analytical}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        analytical: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <label className='label'>友善型: </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.amiable}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        amiable: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <label className='label'>表達型: </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.expressive}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        expressive: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <label className='label'>推動型: </label>
            <input
                type="number"
                className="modalTextInput-single"
                value={formData.driver}
                onChange={(e) => 
                    setFormData({
                        ...formData,  
                        driver: parseInt(e.target.value)
                    })
                }
            />
            <br></br>
            <button
                type="submit"
                className="modalButton"
            >
            提交記錄
            </button>
            {errors.map(error => (
            <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
            ))}
            </form>
        </Modal>
    )
}


// export const SocialStyleQuestionModal = () => {
//     const [formData, setFormData] = useState(SocialStyleQuestionForm);
//     const [errors, setErrors] = useState([] as any[]);

//     const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
//         e.preventDefault(); 
//         let hasError = false;
//         const newErrors = [];
//         if (localStorage.getItem('student_id') === null){
//             newErrors.push({message: '請先選擇學生'});
//             hasError = true;
//         }
 
//         if (hasError){
//             setErrors(newErrors);
//             return;
//         }
//         addSocialStyle(formData).then(
//             ()=>{
//                 window.location.reload();
//             }
//         );
//     }

//     const handleOptionChange = (index, option) => {
//         const updatedFormData = [...formData];
//         updatedFormData[index].selectedOption = option;
//         setFormData(updatedFormData);
//       };


//     return (
//         <Modal>
//             <form onSubmit={handleSubmit}>
//             {formData.map((question, index) => (
//                 <div key={index}>
//                 <h3>Question {index + 1}</h3>
//                 <p>Please choose the best option:</p>
//                 <select
//                     className="modalSelect"
//                     value={question.selectedOption}
//                     onChange={(e) => handleOptionChange(index, e.target.value)}
//                 >
//                     <option value="">Select an option</option>
//                     {SocialStyleQuestionForm[index].options.map(option => (
//                     <option key={option.value} value={option.value}>
//                         {option.label}
//                     </option>
//                     ))}
//                 </select>
//                 </div>
//             ))}
//             </form>
//         </Modal>
//     )
// }