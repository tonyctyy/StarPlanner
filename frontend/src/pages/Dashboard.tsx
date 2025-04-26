/**
 * Dashboard.tsx
 * 
 * This is the main dashboard component that fetches user profile data and calendar/task data from the API.
 * 
 * It displays goals, tasks, and methods sections using other components.
 * It also implements drag and drop functionality for the calendar tasks using react-dnd.
 * 
 * @key Fetches data from API  
 * @key Renders GoalContent, TaskContent, MethodContent
 * @key Implements drag and drop calendar
 */

import '../styles/styles.css';
import React, { FC, useCallback, useEffect, useState, useRef } from 'react';
import GoalContent from '../components/Goals';
import TaskContent from '../components/Tasks';
// import MethodContent from '../components/Method';
import {GoalModal, TaskModal} from '../components/HandleAdding'
import {MainWrapper, DnDWrapper} from '../styles/style.const'
import moment from 'moment';
import {MDBContainer, MDBTabsLink, MDBCol, MDBRow} from 'mdb-react-ui-kit';
import 'react-circular-progressbar/dist/styles.css';
import { Profile, Options } from '../Interface';
import Header from '../components/Header';
import { getSize } from '../components/Responsive';
import { Phone, Tablet, Desktop } from '../components/Responsive';
import { Column, IElement } from '../components/Column';
import { nanoid } from 'nanoid';
import { DndContext, DragEndEvent, DragOverEvent } from '@dnd-kit/core';
import _, { camelCase, filter} from 'lodash';
import "@fontsource/anek-telugu";
import { Droppable } from "../primitives/Droppable";
import { FaTrashAlt, FaPlusCircle } from "react-icons/fa"
import { closestCenter } from '@dnd-kit/core';
import { snapCenterToCursor } from '@dnd-kit/modifiers';
import {getProfile, getDndData, postDndData} from '../API';
import {BlockTitle, Separator } from '../components/Utils';
import {AC_Element} from '../components/ACElement';

// the container setting for goals, tasks, and methods
const Section = ({ title, children }: { title: string, children: React.ReactNode }) => (
    <>
        <MDBContainer
            className="dashboard-component-background"
        >

            {title &&
                <MDBTabsLink>
                    <MDBCol>
                        <Desktop>
                            <h3 className="dashboard-component-title">{title}</h3>
                        </Desktop>
                        <Tablet>
                            <h5 className="dashboard-component-title">{title}</h5>
                        </Tablet>
                        <Phone>
                            <h6 className="dashboard-component-title">{title}</h6>
                        </Phone>
                    </MDBCol>
                </MDBTabsLink>
            }
            {children}
        </MDBContainer>
    </>
)


// const for setting the calendar drag area
const today = moment();

const dates = [];

for (let i = 0; i < 7; i++) {
    const date = moment().add(i, 'days');
    dates.push(date.format("D/M (ddd)"));
}

const COLUMNS = ["Overdue", ...dates];

const DEFAULT_DATA_STATE: IElement[] = [
    {
        id: nanoid(),
        content: "Initial Draggable 1",
        column: "24/8 (Thu)",
        shouldCopy: false,
    }

];


// main dashboard 
function Dashboard() {
    const [data, setData] = useState<Profile | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [expanded, setExpanded] = useState<number[]>([]);
    const [isDragging, setIsDragging] = useState(false);
    const rowRef = useRef<HTMLDivElement>(null);
    const [rowTop, setRowTop] = useState(0);
    const [overCol, setOverCol] = useState<string | null>(null);
    const [showGoalModal, setShowGoalModal] = useState(false);
    const [showTaskModal, setShowTaskModal] = useState(false);
    const [showSuccess, setShowSuccess] = useState(false);
    const [dndData, setDndData] = useState<IElement[]>(DEFAULT_DATA_STATE);

    // convert the calendar info to the displayed calendar
    function calendarDataConverter(data: IElement[]) {
        data = data.filter(elm => elm.column !== 'bin')
        data.map(elm => {
            if (elm.column !== 'overdue' && moment(elm.column, "D/M (ddd)").isBefore(today.startOf('day'))) {
                elm.column = 'overdue';
            }
        })
        setDndData(data)
        return;
    }

    useEffect(() => {
        (async () => {
            getProfile(false)
                .then((data) => {
                    setData(data);

                }).catch((e) => {
                    setError(e);
                });
        })();

        (async () => {
            getDndData()
                .then((data) => {
                    calendarDataConverter(data.calendar_data);
                }).catch((e) => {
                    setError(e);
                }
                )
        })();
    }, []);


    // handle the dragging event (drag item into the calendar)
    const handleResize = () => {
        if (rowRef.current) {
            const rect = rowRef.current.getBoundingClientRect();
            setRowTop(rect.top);
        }
    }

    const handleOnDragStart = useCallback(
        () => {
            handleResize()
            setIsDragging(true);
        }, []
    )

    const handleOnDragOver = useCallback(
        ({ active, over }: DragOverEvent) => {
            setOverCol(over && String(over.id));
        }, []
    )

    const handleOnDragEnd = useCallback(
        ({ active, over }: DragEndEvent) => {
            const elementId = active.id;
            const deepCopy = [...dndData];


            const draggedElementIndex = deepCopy.findIndex((elm) => elm.id === elementId);
            if (draggedElementIndex === -1) return;

            const draggedElement = deepCopy[draggedElementIndex];
            setOverCol(over && String(over.id));
            const column = over !== null ? String(over.id) : draggedElement.column;

            // Assuming we copy all elements for demonstration purposes.
            // You can adjust this condition to specify which elements should be copied.
            if (draggedElement.column === 'bin') {
                deepCopy.splice(draggedElementIndex, 1);
            }
            else if (draggedElement.shouldCopy) {
                const newElement = { ...draggedElement, id: nanoid(), column, shouldCopy: false };
                deepCopy.push(newElement);
            } else {
                draggedElement.column = column;
            }

            

            setDndData(deepCopy.filter(elm => elm.column !== 'bin'));
            setIsDragging(false);
            setOverCol(null);
            postDndData(deepCopy);
            console.log(deepCopy.filter(elm => elm.column !== 'bin'))
        },
        [dndData, setDndData]
    );  


   // the style of the section for goals, tasks and methods
   const contentStyle = {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'nowrap',
    overflowX: 'auto',
    justifyContent: getSize() === 'desktop' ? 'center' : 'flex-start',
    gap: 'calc(0.5%)',
    width: getSize() === 'desktop' ? '98vw' : '95vw',
    top: 0,
    position: isDragging ? 'absolute' : 'relative',
    paddingTop: isDragging ? rowTop : 0,
} as const

    // the list of goals the selected student is having
    const GOAL_OPTIONS: Options[] = [{value: '0', label: '沒有所屬目標'}];
    if (data && data.goals.length) {
        GOAL_OPTIONS.push(...data.goals.map(goal => ({
          value: String(goal.id),
          label: goal.name
        })));
      }
      
    const TASK_OPTIONS: Options[] = [{value: '0', label: '沒有所屬任務'}];
    if (data && data.tasks.length) {
        TASK_OPTIONS.push(...data.tasks.map(task => ({
        value: String(task.id),
        label: task.name
        })));
    }

    const SUBJECT_OPTIONS: Options[] = [{value: '0', label: '沒有所屬科目'}];
    if (data && data.subjects.length) {
        SUBJECT_OPTIONS.push(...data.subjects.map(subject => ({
        value: String(subject.id),
        label: subject.display_name
        })));
    }
    
    const METHOD_OPTIONS: Options[] = [{value: '0', label: '沒有所屬方法'}];
    // if (data && data.methods.length) {
    //     METHOD_OPTIONS.push(...data.methods.map(method => ({
    //     value: String(method.id),
    //     label: method.name
    //     })));
    // }

    // Update Goal AddIcon
    const AddGoalIcon = () => {
        return (
        <FaPlusCircle onClick={() => {
            if (showGoalModal) {setShowGoalModal(false)}
            else{setShowGoalModal(true)}
        }
            } /> 
        )
    }
      
    // Update Task AddIcon
    const AddTaskIcon = () => {
        return (
        <FaPlusCircle onClick={() => {
            if (showTaskModal) {setShowTaskModal(false)}
            else{setShowTaskModal(true)}
        }
            } /> 
        )
    }

    
    return (
        <>
            <Header />
            <DndContext
                onDragEnd={handleOnDragEnd}
                onDragStart={handleOnDragStart}
                onDragOver={handleOnDragOver}
                collisionDetection={closestCenter}
                modifiers={[snapCenterToCursor]}
            >
            <div style={{display: "flex",
                 justifyContent: "center",
                 height: "100%"}}>
                <MainWrapper>
                    <DnDWrapper>
                        {COLUMNS.map((column, columnIndex) => (
                            <Column
                                key={`column-${columnIndex}`}
                                heading={column}
                                elements={filter(dndData, (elm) =>
                                    elm.column === camelCase(column)
                                )}
                                overCol={overCol}

                            />
                        ))}

                    </DnDWrapper>
                    
                    {<MDBContainer style={{
                            position: "relative",
                            width: 0,
                            height: 'auto',
                            padding: 0,
                        }}>
                            <div style={{
                                width: 20,
                                height: 20,
                                position: "absolute",
                                bottom: 20,
                                right: 20,
                            }}>
                                <Droppable id='bin'>
                                    <FaTrashAlt style={{
                                        fontSize: 20,
                                        color: "red",
                                        
                                    }} />
                                </Droppable>
                            </div>
                    </MDBContainer> }
                </MainWrapper>
            </div>
                <MDBRow
                    style={contentStyle}
                    className='hide-scrollbar'
                    ref={rowRef}
                >
                    
                    <MDBCol md="4" className="dashboard-component-col">
                        <Section title="" >
                        <div className="dashboard-component-titleContainer">
                            <div className="dashboard-component-title">
                                Goals
                            </div>
                            <div>
                                <AddGoalIcon />
                            </div>
                        </div>
                        {showGoalModal && <GoalModal goal={null} isEdit={false} GOAL_OPTIONS={GOAL_OPTIONS}/>}
                            
                        {data &&
                            <GoalContent
                                goals={data.goals} 
                                dndData={dndData} 
                                setDndData={setDndData} />
                        }
                        </Section>
                    </MDBCol>
                
                    <MDBCol md="4" className="dashboard-component-col">
                        <Section title="">
                        <div className="dashboard-component-titleContainer">
                            <div className="dashboard-component-title">
                                Tasks
                            </div>
                            <div>
                                <AddTaskIcon />
                            </div>
                        </div>
                        {showTaskModal && <TaskModal task={null} isEdit={false}GOAL_OPTIONS={GOAL_OPTIONS} TASK_OPTIONS={TASK_OPTIONS} SUBJECT_OPTIONS={SUBJECT_OPTIONS} METHOD_OPTIONS={METHOD_OPTIONS}/>}
                        {data &&
                            <TaskContent
                                tasks={data.tasks}
                                dndData={dndData}
                                setDndData={setDndData}/>
                        }
                        </Section>
                    </MDBCol>

                    <MDBCol md="2" className="dashboard-component-col">
                        <Section title="">
                        <MDBRow className="dashboard-component-titleContainer">
                            <BlockTitle titles={['AC Focus']}/>
                            {/* <div style={{marginBottom:"5%"}}></div> */}
                        </MDBRow>
                        <Separator thickness={4}/>

                            <AC_Element />
                        </Section>
                    </MDBCol>

                </MDBRow>



            </DndContext >
        </>
    )
}

export default Dashboard;