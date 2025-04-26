/**
 * Goals.tsx
 * 
 * Renders the goals section.
 * 
 * Displays goal name, days remaining, and progress.
 * Can expand goal to show details.
 * Implements Goal generator column.
 * 
 * @key Displays goal info  
 * @key Expandable details
 * @key Goal generator column
*/

import React from 'react';
import { useState } from 'react';
import { BlockTitle, Separator } from './Utils';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { MDBCol, MDBContainer, MDBRow } from 'mdb-react-ui-kit';
import moment, { now } from 'moment';
import { Goal } from '../Interface';
import { GoalEvaluation } from './HandleEvaluation';
//import styles from '../styles/styles.module.css';
import '../styles/styles.css'
import { Phone, getSize } from './Responsive';
import { Column, IElement, Generator } from './Column';
import { filter, camelCase } from "lodash";
import { nanoid } from 'nanoid';
import { handleDelete } from '../API';

interface GoalButtonProps {
    goal_id: number;
  }


const GoalProgress = ({ goal }: { goal: Goal }) => {
    let progress_num = goal.progress * 10
    return (
        <div style={{
            width: 100,
            height: 100,
            margin: 'auto',
        }}>
            <CircularProgressbar
                value={progress_num}
                text={`${progress_num}%`}
            />
        </div>

    )
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


export default function GoalContent({ goals, dndData, setDndData }: { goals: Goal[], dndData: IElement[], setDndData: React.Dispatch<React.SetStateAction<IElement[]>> }) {
    const [expanded, setExpanded] = useState<number[]>([]);
    const [showEvaluation, setShowEvaluation] = useState<boolean>(false);

    function isExpanded(goal: Goal) {
        return expanded.includes(goal.id);
    }

    function toggleExpanded(goal: Goal) {
        if (isExpanded(goal)) {
            setExpanded(expanded.filter((id) => id !== goal.id));
        } else {
            setExpanded([...expanded, goal.id]);
        }
    }

    const handleGeneratorMount = (name: string, col: string) => {
        if (dndData.some(elm => elm.content === name && elm.column === col && elm.shouldCopy === true)) {
            // console.log(`goal ${name} already exists`)
            return;
        }


        const newElement = {
            id: nanoid(),
            content: name,
            column: col,
            shouldCopy: true,
            color : '#f5c3c3',
        };
        setDndData(prevData => [...prevData, newElement]);
    };

    const DeleteButton: React.FC<GoalButtonProps> = ({goal_id}) => {
        const handleDeleteButtonClick = () => {
            const confirmDelete = window.confirm('確定要刪除嗎？');
            if (confirmDelete) {
              handleDelete(goal_id.toString(), 'goal')
                .then(() => {
                  window.location.reload();
                })
                .catch((error) => {
                  console.error('Error deleting item:', error);
                });
            }
          };
        return (
            <button className="secondary-button" onClick={handleDeleteButtonClick}
            >刪除</button>
        )
    }
        
    const EvaluateButton: React.FC<GoalButtonProps> = ({goal_id}) => {
        const [showEvaluation, setShowEvaluation] = useState(false);
      
        const handleEvaluateClick = () => {
          setShowEvaluation(!showEvaluation);
        };
      
        return (
          <div className={`button-row ${showEvaluation ? 'column' : ''}`}>
            <button className="primary-button" onClick={handleEvaluateClick}>
              {showEvaluation ? '取消' : '評估目標'}
            </button>
            <div>
            {showEvaluation && <GoalEvaluation id={goal_id}/>}
            </div>
            <div>
                <DeleteButton goal_id={goal_id}></DeleteButton>
            </div>
          </div>
          
        );
      };




    return (
        <MDBContainer style={{
            overflow: 'show',
        }}>
            <BlockTitle titles={['', '剩餘日子', '進度']} />
            <Separator thickness={4} />
            {goals.map(
                (goal, index) => {
                    return (
                        <div key={nanoid()}>
                            <MDBRow
                                onClick={() => toggleExpanded(goal)}
                                style={{ cursor: 'pointer', }}
                            >
                                {index !== 0 && <Separator thickness={2} />}

                                <MDBCol className={`section-content ${getSize()}`}>

                                    <Generator
                                        key={`goal-column-${goal.name}${index}`}

                                        heading={`goal-column-${goal.name}${index}`}
                                        elements={filter(dndData, (elm) =>
                                            elm.column === camelCase(`goal-column-${goal.name}${index}`)
                                        )}
                                        title={goal.name}
                                        col={camelCase(`goal-column-${goal.name}${index}`)}
                                        onMount={handleGeneratorMount}
                                    />
                                </MDBCol>
                                <MDBCol className={`section-content ${getSize()}`}>
                                    {getDaysRemainingText(goal)}
                                </MDBCol>
                                <MDBCol className={`section-content ${getSize()}`}>
                                    {goal.progress * 10}%
                                    {/* <GoalProgress goal={goal} /> */}
                                </MDBCol>
                            </MDBRow>

                            {
                                isExpanded(goal) &&
                                <MDBRow>
                                    {goal.parent !== null &&
                                        <span>
                                            所屬目標: {goal.parent.name}
                                        </span>
                                    }
                                    <span>
                                        描述: {goal.description}
                                        
                                    </span>
                                    <span>
                                        目標種類: {goal.display_goal_type}
                                    </span>
                                    <span>
                                        難度: {goal.display_difficulty}
                                    </span>
                                    <div className="button-row">
                                        <EvaluateButton goal_id={goal.id} />
                                        
                                    </div>

                                </MDBRow>
                            }
                        </div>
                    )
                })
            }
        </MDBContainer>
    )

}

