import { IElement } from './components/Column';
import {idProps} from './Interface';

const API_URL = "https://star-planner-coaching-api.azurewebsites.net";
// const API_URL = "http://127.0.0.1:8000"


export async function getStudentList() {
    const response = await fetch(`${API_URL}/api/get_student_list`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: 'include',
    }).then(
        response => {
            return response.json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
};


// get all the goals, tasks, methods for the selected student
export async function getProfile(isFinal: boolean) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, isFinal: isFinal } : {};
    const response = await fetch(`${API_URL}/api/student_dashboard_api/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
};


export async function getSessionReport(id:string) {
    const body_data = id ? { report_id: id } : {};
    const response = await fetch(`${API_URL}/api/get_session_report/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
}


export async function getSessionReports() {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id } : {};
    const response = await fetch(`${API_URL}/api/get_session_reports/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
}


export async function getCommentList() {
    const student_id = localStorage.getItem('student_id');
    const body_data = { student_id: student_id};
    const response = await fetch(`${API_URL}/api/get_comment_list/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: 'include',
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
}


export async function getFinalReport(){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { student_id: student_id, coach_id: coach_id };
    const response = await fetch(`${API_URL}/api/get_final_report/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
}


export async function getSocialStyle(){
    const student_id = localStorage.getItem('student_id');
    const body_data = { student_id: student_id };
    const response = await fetch(`${API_URL}/api/get_social_style/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;
}


export async function getSubjectComments(){
    const student_id = localStorage.getItem('student_id');
    const body_data = { student_id: student_id };
    const response = await fetch(`${API_URL}/api/get_subject_comments/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: 'include',
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;

}


export async function getPreACRecord(){
    const student_id = localStorage.getItem('student_id');
    const body_data = { student_id: student_id };
    const response = await fetch(`${API_URL}/api/get_pre_ac_record/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: 'include',
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.json();
        }
    )
        .catch(
            error => {
            console.log(error);
        }
    )
    return response;

}


export async function addPreACRecord(formData:any){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { student_id: student_id, coach_id: coach_id, record: formData };
    const response = await fetch(`${API_URL}/api/add_edit_pre_ac_record/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(body_data)
    })
}


// get the calendar info for the selected student
export async function getDndData() {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id } : {};
    const response = await fetch(`${API_URL}/api/get_calendar_data/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;

}


// update the calendar info for the selected student
export async function postDndData(data: IElement[]) {
    const student_id = localStorage.getItem('student_id');
    data = data.filter(elm => elm.shouldCopy === false && elm.column !== 'bin');
    const body_data = student_id ? { student_id: student_id, calendar_data: data } : {};
    const response = await fetch(`${API_URL}/api/save_calendar_data/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data),
    }).catch(
        error => {
            console.log(error);
        }
    )
    return response;
}


export async function addGoal(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, goal: formData } : {};
    const response = await fetch(`${API_URL}/api/add_goal/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function addTask(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, task: formData } : {};
    const response = await fetch(`${API_URL}/api/add_task/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function addSessionReport(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { coach_id: coach_id, student_id: student_id, report: formData };
    const response = await fetch(`${API_URL}/api/add_session_report/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function addSocialStyle(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, social_style: formData } : {};
    const response = await fetch(`${API_URL}/api/add_social_style/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: 'include',
        body: JSON.stringify(body_data)
    })
}


export async function addSubjectComment(report_id:number, formData:any) {
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    const body_data = { report_id: report_id, student_id: student_id, coach_id: coach_id, subject: formData };
    const response = await fetch(`${API_URL}/api/add_subject_comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(body_data)
    })
}


export async function editSessionReport(id:number, formData:any){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { report_id: id, report: formData };
    const response = await fetch(`${API_URL}/api/edit_session_report/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function editFinalReport(part:string, formData:any){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { student_id: student_id, coach_id: coach_id, part: part, report: formData };
    const response = await fetch(`${API_URL}/api/edit_final_report/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function editACRecord(id:number, formData:any){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    if (!coach_id|| !student_id) {
        return;
    }
    const body_data = { report_id: id, record: formData };
    const response = await fetch(`${API_URL}/api/edit_ac_record/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function editSubjectComment(id:number, formData:any){
    const student_id = localStorage.getItem('student_id');
    const coach_id = localStorage.getItem('coach_id');
    const body_data = { report_id: id, student_id: student_id, coach_id: coach_id, subject: formData };
    const response = await fetch(`${API_URL}/api/edit_subject_comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(body_data)
    })
}


export async function evaluateGoal(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, evaluation: formData } : {};
    const response = await fetch(`${API_URL}/api/evaluate_goal/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function evaluateTask(formData:any) {
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, evaluation: formData } : {};
    const response = await fetch(`${API_URL}/api/evaluate_task/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}


export async function signin(signInData:any){
    const response = await fetch(`${API_URL}/api/api-token-auth/`, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': 'application/json',
        }),
        body: JSON.stringify(signInData)
    })
    return response;
}


export async function signout(){
    const response = await fetch(`${API_URL}/api/signout/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': 'csrftoken',
        },
        credentials: "include",
    })

    return response;
}


export async function getGPTComment(section: string, modelType: string, selectedComments: string[], personalizedComments: string){
    const model_type = modelType === "" ? "social_style" : modelType;
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, section: section, model_area: model_type ,selected_comments: selectedComments, personalized_comments: personalizedComments } : {};
    const response = await fetch(`${API_URL}/api/get_gpt_comment/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    }).then(
        response => {
            return response.clone().json();
        }
    )
        .catch(
            error => {
                console.log(error);
            }
        )
    return response;


}


export async function handleDelete(id: string, section: string){
    const student_id = localStorage.getItem('student_id');
    const body_data = student_id ? { student_id: student_id, id: id, section: section } : {};
    const response = await fetch(`${API_URL}/api/handle_delete/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        credentials: "include",
        body: JSON.stringify(body_data)
    })
}