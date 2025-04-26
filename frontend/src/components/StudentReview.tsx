import '../styles/styles.css';
import React, { useState, useEffect } from 'react';
import moment from 'moment';
import {Profile, Task, Goal, SAndCModelScores, ACModelScores} from '../Interface';
import {MDBCol, MDBContainer, MDBRow} from 'mdb-react-ui-kit';
import {Tabs, Tab} from 'react-bootstrap';
import { BlockTitle, Separator } from './Utils';
import {areaTitles} from '../Constants';


const TaskReview: React.FC<{tasks: Task[]}> = ({tasks}) => {
    const [expanded, setExpanded] = useState<number[]>([]);

    function isExpanded(comment_id: number) {
        return expanded.includes(comment_id);
    }

    function toggleExpanded(comment_id: number) {
        if (isExpanded(comment_id)) {
            setExpanded(expanded.filter((id) => id !== comment_id));
        } else {
            setExpanded([...expanded, comment_id]);
        }
    }

    return (
        <MDBContainer>
        <MDBRow>
            <div style={{marginTop:"3%"}}/>

            <BlockTitle titles={["任務", "完成日期", "完成程度"]}/>
            <Separator thickness={4}/>
            <MDBCol className="scrollable" style={{height: '30vh', overflowY: 'scroll'}}>            
            {tasks.map((task) => (
                <div key = {task.id} className='dashboard-component-background'>
                <MDBRow onClick={() => toggleExpanded(task.id)} style={{ cursor: 'pointer', }}>
                    <MDBCol size="4">
                    {task.name}
                    </MDBCol>
                    <MDBCol size="4">
                    {task.status === "on going" ? 
                        "進行中" : 
                        task.status === "failed"? 
                        "失敗" :
                        moment(task.end_at).format('DD/MM/YYYY')
                    }
                    </MDBCol>
                    <MDBCol size="4">
                    {task.completeness === 0? "失敗":
                     task.completeness? task.completeness + "/5" : "未完成"}                    
                    </MDBCol>
                </MDBRow>
                {isExpanded(task.id) && (
                <>
                    <Separator thickness={2} />
                    <MDBContainer style={{textAlign: 'left'}}>
                        <span>
                            描述: {task.description}
                        </span>
                        {task.status !== "on going" && (
                        <>
                        <br/>
                        <span>
                            用時: {task.time_spent} 分鐘
                        </span>
                        <br/>
                        <span>
                            投入程度: {task.willingness}
                        </span>
                        <br/>
                        <span>
                            努力程度: {task.effort}
                        </span>
                        <br/>
                        <span>
                            得著/成果: {task.effectiveness}
                        </span>
                        <br/>
                        <span>
                            評語: {task.comment===""? "N/A": task.comment}
                        </span>
                        </>
                        )}

                    </MDBContainer>
                </>
                )}
                </div>
            ))}
            </MDBCol>
        </MDBRow>
        </MDBContainer>
    );
}


const GoalReview: React.FC<{goals: Goal[]}> = ({goals}) => {
    const [expanded, setExpanded] = useState<number[]>([]);

    function isExpanded(comment_id: number) {
        return expanded.includes(comment_id);
    }

    function toggleExpanded(comment_id: number) {
        if (isExpanded(comment_id)) {
            setExpanded(expanded.filter((id) => id !== comment_id));
        } else {
            setExpanded([...expanded, comment_id]);
        }
    }

    function getDaysRemainingText(goal: Goal): JSX.Element {
        const now = moment();
        const deadline = moment(goal.predicted_end_time);
    
        const days = deadline.diff(now, 'days');
        const color = days < 10 ? 'red' : 'black';
    
        return (
            <span style={{ color }}>
                {days}日
            </span>
        );
    }

    return (
        <MDBContainer>
        <MDBRow>
            <div style={{marginTop:"3%"}}/>
            <BlockTitle titles={["目標", "完成日期", "進度"]}/>
            <Separator thickness={4}/>
            <MDBCol className="scrollable" style={{height: '30vh', overflowY: 'scroll'}}>            
            {goals.map((goal) => (
                <div key = {goal.id} className='dashboard-component-background'>
                <MDBRow onClick={() => toggleExpanded(goal.id)} style={{ cursor: 'pointer', }}>
                    <MDBCol size="4">
                    {goal.name}
                    </MDBCol>
                    <MDBCol size="4">
                    {goal.goal_status === "on going" ? 
                        getDaysRemainingText(goal) : 
                        goal.goal_status === "failed"?
                        "失敗" :
                        moment(goal.end_at).format('DD/MM/YYYY')
                    }
                    </MDBCol>
                    <MDBCol size="4">
                    {goal.final_result === 0? 
                        "失敗":
                        goal.final_result? 
                        goal.final_result + "/5":
                        goal.progress*10 + "%"
                    }                    
                    </MDBCol>
                </MDBRow>
                {isExpanded(goal.id) && (
                <>
                    <Separator thickness={2} />
                    <MDBContainer style={{textAlign: 'left'}}>
                        {goal.parent && (
                        <>
                        <span>
                            所屬目標: {goal.parent.name}
                        </span>
                        <br/>
                        </>
                        )}    
                        <span>
                            描述: {goal.description}
                        </span>
                        <br/>
                        <span>
                            目標種類: {goal.display_goal_type}
                        </span>
                        <br/>
                        <span>
                            難度: {goal.display_difficulty}
                        </span>
                        {goal.goal_evaluate && (
                        <>
                        <br/>
                        <span>
                            努力程度: {goal.goal_evaluate.effort}
                        </span>
                        <br/>
                        <span>
                            評語: {goal.goal_evaluate.comment}
                        </span>
                        </>
                        )}
                    </MDBContainer>
                </>
                )}
                </div>
            ))}
            </MDBCol>
        </MDBRow>
        </MDBContainer>
    );
}


const ScoreReview: React.FC<{scores: SAndCModelScores | ACModelScores}> = ({scores}) => {
    const [expanded, setExpanded] = useState<string[]>([]);

    function isExpanded(comment_id: string) {
        return expanded.includes(comment_id);
    }

    function toggleExpanded(comment_id: string) {
        if (isExpanded(comment_id)) {
            setExpanded(expanded.filter((id) => id !== comment_id));
        } else {
            setExpanded([...expanded, comment_id]);
        }
    }

    return (
        <MDBContainer>
            <MDBRow>
                <div style={{marginTop:"3%"}}/>
                <MDBCol className="scrollable" style={{height: '30vh', overflowY: 'scroll'}}>      
                    {scores && Object.entries(scores).map(([area, score]) => (
                        <div key={area} className='dashboard-component-background'>
                        <MDBRow onClick={() => toggleExpanded(area)} style={{ cursor: 'pointer', }}>
                            <MDBCol>
                                {areaTitles[area]}
                            </MDBCol>
                        </MDBRow>
                        {isExpanded(area) && (
                            <div>
                            {score.map( (item: String, key:number) => (
                                <MDBRow key={key}>
                                    範疇{key+1}:    {item}
                                </MDBRow>
                                
                            ))}
                            </div>
                        )}
                        </div>
                    ))}
                </MDBCol>
            </MDBRow>
        </MDBContainer>
    );
}



const StudentReview: React.FC<{profile: Profile, sc_scores:SAndCModelScores, ac_scores: ACModelScores}> = ({profile, sc_scores, ac_scores}) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [activeTab, setActiveTab] = useState('tasks');



  useEffect(() => {
    const sortedTasks = profile.tasks.sort((a, b) => {
        if (a.status === "on going" && b.status !== "on going") {
            return -1;
        } else if (a.status !== "on going" && b.status === "on going") {
            return 1;
        } else {
            return -moment(a.end_at).diff(moment(b.end_at));
        }
    });
    const sortedGoals = profile.goals.sort((a, b) => {
        if (a.goal_status === "on going" && b.goal_status !== "on going") {
            return -1;
        }
        else if (a.goal_status !== "on going" && b.goal_status === "on going") {
            return 1;
        }
        else {
            return -moment(a.end_at).diff(moment(b.end_at));
        }
    });

    setTasks(sortedTasks);
    setGoals(sortedGoals);
  }, [profile]);

  return (
    <MDBContainer>
      <MDBRow>
        <Tabs activeKey={activeTab} onSelect={(tab) => (tab && setActiveTab(tab))}>
            <Tab eventKey="tasks" title="任務">
                <TaskReview tasks={tasks}/>
            </Tab>
            <Tab eventKey="goals" title="目標">
                <GoalReview goals={goals}/>
            </Tab>
            <Tab eventKey="scores" title="過往分數">
                <ScoreReview scores={ac_scores}/>
            </Tab>
        </Tabs>
      </MDBRow>
    </MDBContainer>
  );
}

export default StudentReview;
