/**
 * Tasks.tsx
 * 
 * Renders the tasks section.
 * 
 * Displays task name, subjects, due date. 
 * Expandable details section.
 * Implements Task generator column.
 *  
 * @key Shows tasks info
 * @key Expandable details 
 * @key Task generator
*/

import React from 'react';
import { useState } from 'react';
import { Separator, BlockTitle } from './Utils';

import 'react-circular-progressbar/dist/styles.css';
import { MDBCol, MDBContainer, MDBRow } from 'mdb-react-ui-kit';
import moment from 'moment';
import { Task } from '../Interface';
import styles from '../styles/styles.module.css';
import { getSize } from './Responsive';
import { Generator, IElement } from './Column';
import { camelCase, filter } from 'lodash';
import { nanoid } from 'nanoid';
import { TaskEvaluation } from './HandleEvaluation';
import { handleDelete } from '../API';


interface TaskButtonProps {
    task_id: number;
  }


export default function taskContent({ tasks, dndData, setDndData }: { tasks: Task[], dndData: IElement[], setDndData: React.Dispatch<React.SetStateAction<IElement[]>> }) {
    const [expanded, setExpanded] = useState<number[]>([]);

    function isExpanded(task: Task) {
        return expanded.includes(task.id);
    }

    function toggleExpanded(task: Task) {
        if (isExpanded(task)) {
            setExpanded(expanded.filter((id) => id !== task.id));
        } else {
            setExpanded([...expanded, task.id]);
        }
    }

    const handleGeneratorMount = (name: string, col: string) => {
        if (dndData.some(elm => elm.content === name && elm.column === col && elm.shouldCopy === true)) {
            // console.log(`${name} in ${col} already exists`)
            return;
        }


        const newElement = {
            id: nanoid(),
            content: name,
            column: col,
            shouldCopy: true,
            color: '#c4f5c3',
        };
        setDndData(prevData => [...prevData, newElement]);
    };

    const DeleteButton: React.FC<TaskButtonProps> = ({ task_id }) => {
        const handleDeleteButtonClick = () => {
          const confirmDelete = window.confirm('確定要刪除嗎？');
          if (confirmDelete) {
            handleDelete(task_id.toString(), 'task')
              .then(() => {
                window.location.reload();
              })
              .catch((error) => {
                console.error('Error deleting item:', error);
              });
          }
        };
      
        return (
          <button className="secondary-button" onClick={handleDeleteButtonClick}>
            刪除
          </button>
        );
      };

        
    const EvaluateButton: React.FC<TaskButtonProps> = ({task_id}) => {
        const [showEvaluation, setShowEvaluation] = useState(false);
      
        const handleEvaluateClick = () => {
          setShowEvaluation(!showEvaluation);
        };
      
        return (
          <div className={`button-row ${showEvaluation ? 'column' : ''}`}>
            <button className="primary-button" onClick={handleEvaluateClick}>
              {showEvaluation ? '取消' : '評估任務'}
            </button>
            <div>
            {showEvaluation && <TaskEvaluation id={task_id}/>}
            </div>
            <div>
                <DeleteButton task_id={task_id}></DeleteButton>
            </div>
          </div>
          
        );
      };


    return (
        <MDBContainer>
            <BlockTitle titles={['', '相關科目', 'Due Date']} />
            <Separator thickness={4} />

            <MDBContainer>
                {tasks.map((task, index) => {
                    return (<div key={nanoid()}>
                        <MDBRow
                            onClick={() => toggleExpanded(task)}
                            style={{ cursor: 'pointer', }}
                        >
                            {index !== 0 && <Separator thickness={2} />}
                            <MDBCol className={`section-content ${getSize()}`}>
                                <Generator
                                    key={`task-column-${task.name}${index}`}

                                    heading={`task-column-${task.name}${index}`}
                                    elements={filter(dndData, (elm) =>
                                        elm.column === camelCase(`task-column-${task.name}${index}`)
                                    )}
                                    title={task.name}
                                    col={camelCase(`task-column-${task.name}${index}`)}
                                    onMount={handleGeneratorMount}
                                />
                            </MDBCol>
                            <MDBCol className={`section-content ${getSize()}`}>
                                {task.subject.map((subject) => {
                                    return (
                                        <div key={nanoid()}>
                                            {subject.name_abbr}
                                        </div>
                                    )
                                })}
                            </MDBCol>
                            <MDBCol className={`section-content ${getSize()}`}>
                                {moment(task.predicted_end_time).format('D/M')}
                            </MDBCol>
                        </MDBRow>
                        {isExpanded(task) &&
                            <MDBRow>
                                <MDBContainer>
                                    描述：{task.description}
                                </MDBContainer>
                                <br />
                                <MDBContainer>
                                    優先度：{task.priority}
                                </MDBContainer>
                                <br />
                                <MDBRow className={styles.tagRow}>
                                    {task.goals.map((goal) => {
                                        return (
                                            <MDBContainer className={styles.goalTag}>

                                                {goal.name}
                                                <br />
                                            </MDBContainer>
                                        )
                                    })}
                                    {task.tasks.map((task) => {
                                        return (
                                            <MDBContainer className={styles.taskTag}>
                                                {task.name}
                                                <br />
                                            </MDBContainer>)

                                    })}

                                </MDBRow>
                                <div className="button-row">
                                        <EvaluateButton task_id={task.id} />
                                        
                                </div>
                            </MDBRow>}
                    </div>
                    )
                })
                }
            </MDBContainer>
        </MDBContainer>
    )

}