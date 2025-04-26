import React, { useState } from 'react';
import { evaluateGoal, evaluateTask} from '../API';
import {STATUS, FivePointScale, TenPointScale, GoalEvaluationForm, TaskEvaluationForm} from '../Constants';
import {Modal, } from '../styles/style.const'
import { idProps } from '../Interface';



export const GoalEvaluation: React.FC<idProps> = ({id}) => {
    const [formData, setFormData] = useState(GoalEvaluationForm);
    const [errors, setErrors] = useState([] as any[]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if(formData.progress === -1) {
            newErrors.push( {message: '請選擇進度'});
            hasError = true;
            }
        else if (formData.effort === -1) {
            newErrors.push({message: '請選擇努力程度'});
            hasError = true;
        }
        else if (formData.status != 'on going' && formData.final_result === -1) {
            newErrors.push({message: '請選擇成果'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        formData.goal_id = id;
        evaluateGoal(formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }
return (
    <Modal>
        <form onSubmit={handleSubmit}>
        <label className='label'>進度 (0-10分, 0% - 100%): </label>
        <select 
            value={formData.progress}
            onChange={(e) => setFormData({...formData, progress: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {TenPointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>目前狀態: </label>
        <select 
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value})}
            className="modalSelect"
        >
            {STATUS.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>努力程度 (0分代表沒有努力，5分代表竭盡全力): </label>
        <select 
            value={formData.effort}
            onChange={(e) => setFormData({...formData, effort: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>成果 (0分代表沒有開始，5分代表完全完成)(在完成/失敗後填寫):</label>
        <select 
            value={formData.final_result}
            onChange={(e) => setFormData({...formData, final_result: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>評語: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.comment}
            onChange={(e) => setFormData({...formData, comment: e.target.value})}
        />
        <button 
            type="submit" 
            className="modalButton">
        提交評估
        </button>
        <br></br>
        {errors.map(error => (
        <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
        ))}
        </form>
    </Modal>
    )
}


export const TaskEvaluation: React.FC<idProps> = ({id}) => {
    const [formData, setFormData] = useState(TaskEvaluationForm);
    const [errors, setErrors] = useState([] as any[]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault(); 
        let hasError = false;
        const newErrors = [];
        if (formData.status != 'on going' && ((formData.effort === -1) || (formData.willingness === -1) || (formData.effectiveness === -1) || (formData.completeness === -1))) {
            newErrors.push({message: '如目標已完成/失敗，請填寫努力程度、投入程度、得著/成果和完成程度。'});
            hasError = true;
        }
        if (hasError){
            setErrors(newErrors);
            return;
        }
        formData.task_id = id;
        evaluateTask(formData).then(
            ()=>{
                window.location.reload();
            }
        );
    }
    return(
        <Modal>
        <form onSubmit={handleSubmit}>
        <label className='label'>目前狀態: </label>
        <select 
            value={formData.status}
            onChange={(e) => setFormData({...formData, status: e.target.value})}
            className="modalSelect"
        >
            {STATUS.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>完成程度 (0分代表沒有開始，5分代表完成): </label>
        <select 
            value={formData.completeness}
            onChange={(e) => setFormData({...formData, completeness: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>投入程度 (0分代表非常厭惡，5分代表非常享受):</label>
        <select 
            value={formData.willingness}
            onChange={(e) => setFormData({...formData, willingness: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>努力程度 (0分代表沒有努力，5分代表竭盡全力): </label>
        <select 
            value={formData.effort}
            onChange={(e) => setFormData({...formData, effort: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>用時 (分鐘): </label>
        <input 
            type="number"
            className="modalTextInput-single"  
            value={formData.time_spent}
            onChange={(e) => setFormData({...formData, time_spent: parseInt(e.target.value, 10) || 0})}
        />
        <br></br>
        <label className='label'>得著/成果 (0分代表低，5分代表高): </label>
        <select 
            value={formData.effectiveness}
            onChange={(e) => setFormData({...formData, effectiveness: parseInt(e.target.value)})}
            className="modalSelect"
        >
            {FivePointScale.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
            ))}
        </select>
        <br></br>
        <label className='label'>評語: </label>
        <input 
            type="text"
            className="modalTextInput-single"  
            value={formData.comment}
            onChange={(e) => setFormData({...formData, comment: e.target.value})}
        />
        <button 
            type="submit" 
            className="modalButton">
        提交評估
        </button>
        <br></br>
        {errors.map(error => (
        <p key={error.message} style={{color: 'red'}}>*{error.message}</p>  
        ))}
        </form>
    </Modal>
    )
}


