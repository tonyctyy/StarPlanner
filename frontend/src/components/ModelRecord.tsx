import '../styles/styles.css';
import React, { useEffect, useState } from 'react';
import {ACRecord, SCRecord, ACProps, SCProps} from '../Interface';
import {MDBCol, MDBContainer, MDBRow} from 'mdb-react-ui-kit';
import { Modal } from '../styles/style.const';
import {Tabs, Tab} from 'react-bootstrap';
import { FivePointScale, ACRecordForm, SCRecordForm, ACDescription, SCDescription} from '../Constants';
import {editACRecord, editFinalReport, getSessionReport} from '../API';
import {Separator} from './Utils';


export const ACModal: React.FC<ACProps> = ({ACRecord, isFinal}) => {
    const [ACformData, setACFormData] = useState<ACRecord | null> (null)
    function handleACRecord(record: ACRecord){
        const updatedACFormData: ACRecord = ACRecordForm;
        Object.entries(record).forEach(([key, value]) => {
            if (value === null) {
                if (key.endsWith('comment')){
                    updatedACFormData[key] = '';
                }
                else{
                    updatedACFormData[key] = -1;
                }
            }
            else {
                if (key==='id' || key.endsWith('comment')){
                    updatedACFormData[key] = value;
                }
                else {
                    updatedACFormData[key] = value -1;
                }
            }
        });
        setACFormData(updatedACFormData)
    }
    
    useEffect(() => {
        if (ACRecord) {
            handleACRecord(ACRecord);
        }
    }, [ACRecord]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (ACformData){
            if(isFinal){
                editFinalReport('ac', ACformData)
                .then(() => {
                    window.location.reload()
                }
                )
            }
            else{
                editACRecord(ACformData.id, ACformData)
                .then(() => {     
                    sessionStorage.removeItem(`session-report-${ACformData.coaching_report_record}`);
                    getSessionReport(ACformData.coaching_report_record.toString())
                        .then((data) => 
                        {
                            sessionStorage.setItem(`session-report-${ACformData.coaching_report_record}`, JSON.stringify(data));
                        }
                    )
                })
            }
        }
    }    

    return(
    <MDBContainer style={{overflow: 'show'}}>
        {ACformData && (
        <form onSubmit={handleSubmit}>
            <Tabs defaultActiveKey="l_s" id="ac-modal" className="mb-3">
                <Tab eventKey="l_s" title={ACDescription.learning_strategy}>
                        <label className='label'>{ACDescription.learning_strategy_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.learning_strategy_1}
                            onChange={(e) => setACFormData({...ACformData, learning_strategy_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.learning_strategy_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.learning_strategy_2}
                            onChange={(e) => setACFormData({...ACformData, learning_strategy_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.learning_strategy_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.learning_strategy_3}
                            onChange={(e) => setACFormData({...ACformData, learning_strategy_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.learning_strategy_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.learning_strategy_comment}
                            onChange={(e) => setACFormData({...ACformData, learning_strategy_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="g_s" title={ACDescription.goal_setting}>
                <label className='label'>{ACDescription.goal_setting_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.goal_setting_1}
                            onChange={(e) => setACFormData({...ACformData, goal_setting_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.goal_setting_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.goal_setting_2}
                            onChange={(e) => setACFormData({...ACformData, goal_setting_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.goal_setting_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.goal_setting_3}
                            onChange={(e) => setACFormData({...ACformData, goal_setting_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.goal_setting_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.goal_setting_comment}
                            onChange={(e) => setACFormData({...ACformData, goal_setting_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="org" title={ACDescription.organising}>
                <label className='label'>{ACDescription.organising_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.organising_1}
                            onChange={(e) => setACFormData({...ACformData, organising_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.organising_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.organising_2}
                            onChange={(e) => setACFormData({...ACformData, organising_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.organising_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.organising_3}
                            onChange={(e) => setACFormData({...ACformData, organising_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.organising_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.organising_comment}
                            onChange={(e) => setACFormData({...ACformData, organising_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="mot" title={ACDescription.motivation_and_accountability}>
                <label className='label'>{ACDescription.motivation_and_accountability_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.motivation_and_accountability_1}
                            onChange={(e) => setACFormData({...ACformData, motivation_and_accountability_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.motivation_and_accountability_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.motivation_and_accountability_2}
                            onChange={(e) => setACFormData({...ACformData, motivation_and_accountability_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.motivation_and_accountability_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.motivation_and_accountability_3}
                            onChange={(e) => setACFormData({...ACformData, motivation_and_accountability_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.motivation_and_accountability_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.motivation_and_accountability_comment}
                            onChange={(e) => setACFormData({...ACformData, motivation_and_accountability_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="t_m" title={ACDescription.time_management}>
                <label className='label'>{ACDescription.time_management_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.time_management_1}
                            onChange={(e) => setACFormData({...ACformData, time_management_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.time_management_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.time_management_2}
                            onChange={(e) => setACFormData({...ACformData, time_management_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.time_management_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.time_management_3}
                            onChange={(e) => setACFormData({...ACformData, time_management_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.time_management_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.time_management_comment}
                            onChange={(e) => setACFormData({...ACformData, time_management_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="l_b" title={ACDescription.life_balance}>
                <label className='label'>{ACDescription.life_balance_1}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.life_balance_1}
                            onChange={(e) => setACFormData({...ACformData, life_balance_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.life_balance_2}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.life_balance_2}
                            onChange={(e) => setACFormData({...ACformData, life_balance_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.life_balance_3}</label>
                        <select
                            className='modalSelect'
                            value={ACformData.life_balance_3}
                            onChange={(e) => setACFormData({...ACformData, life_balance_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{ACDescription.life_balance_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={ACformData.life_balance_comment}
                            onChange={(e) => setACFormData({...ACformData, life_balance_comment: e.target.value})}
                        />
                </Tab>
            </Tabs>
            <br></br>
            <Separator thickness={4} />
            <br></br>
            { !isFinal && (
                <div>
            <label className='label'>整體評語: </label>
            <textarea 
                className="modalTextInput"
                value={ACformData.comment}
                onChange={(e) => 
                    setACFormData({
                        ...ACformData,  
                        comment: e.target.value
                    })
                }
            />    
            <br></br>
            </div>
            )}
                <button
                        type="submit"
                        className="modalButton"
                    >
                        儲存AC Focus
                </button>

        </form>
        )}
    </MDBContainer>
    )

}

export const SCModal: React.FC<SCProps> = ({SCRecord}) => {
    const [SCformData, setSCFormData] = useState<SCRecord | null> (null)
    function handleSCRecord(record: SCRecord){
        const updatedSCFormData: SCRecord = SCRecordForm;
        Object.entries(record).forEach(([key, value]) => {
            if (value === null) {
                if (key.endsWith('comment')){
                    updatedSCFormData[key] = '';
                }
                else{
                    updatedSCFormData[key] = -1;
                }
            }
            else {
                if (key==='id' || key.endsWith('comment')){
                    updatedSCFormData[key] = value;
                }
                else {
                    updatedSCFormData[key] = value -1;
                }
            }
        }
        );
        setSCFormData(updatedSCFormData)
    }

    useEffect(() => {
        if (SCRecord) {
            handleSCRecord(SCRecord);
        }
    }, [SCRecord]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (SCformData){
            editFinalReport('s_and_c', SCformData)
            .then(() => {
                window.location.reload()
            }
            )
        }
    }


    return(
    <MDBContainer style={{overflow: 'show'}}>
        {SCformData && (
        <form onSubmit={handleSubmit}>
            <Tabs defaultActiveKey="c_t" id="sc-modal" className="mb-3">
                <Tab eventKey="c_t" title={SCDescription.critical_thinking}>
                        <label className='label'>{SCDescription.critical_thinking_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.critical_thinking_1}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.critical_thinking_2}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.critical_thinking_2}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.critical_thinking_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.critical_thinking_3}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.critical_thinking_4}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.critical_thinking_4}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.critical_thinking_5} </label>
                        <select
                            className='modalSelect'
                            value={SCformData.critical_thinking_5}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_5: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.critical_thinking_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.critical_thinking_comment}
                            onChange={(e) => setSCFormData({...SCformData, critical_thinking_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="p_s" title={SCDescription.problem_solving}>
                        <label className='label'>{SCDescription.problem_solving_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.problem_solving_1}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.problem_solving_2}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.problem_solving_2}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.problem_solving_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.problem_solving_3}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.problem_solving_4}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.problem_solving_4}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.problem_solving_5} </label>
                        <select
                            className='modalSelect'
                            value={SCformData.problem_solving_5}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_5: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.problem_solving_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.problem_solving_comment}
                            onChange={(e) => setSCFormData({...SCformData, problem_solving_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="m_i" title={SCDescription.managing_information}>
                        <label className='label'>{SCDescription.managing_information_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.managing_information_1}
                            onChange={(e) => setSCFormData({...SCformData, managing_information_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.managing_information_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.managing_information_2}
                            onChange={(e) => setSCFormData({...SCformData, managing_information_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.managing_information_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.managing_information_3}
                            onChange={(e) => setSCFormData({...SCformData, managing_information_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.managing_information_4}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.managing_information_4}
                            onChange={(e) => setSCFormData({...SCformData, managing_information_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.managing_information_comment} </label>
                        <textarea
                            className="modalTextInput"
                            value={SCformData.managing_information_comment}
                            onChange={(e) => setSCFormData({...SCformData, managing_information_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="c_i" title={SCDescription.creativity_and_innovation}>
                        <label className='label'>{SCDescription.creativity_and_innovation_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.creativity_and_innovation_1}
                            onChange={(e) => setSCFormData({...SCformData, creativity_and_innovation_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.creativity_and_innovation_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.creativity_and_innovation_2}
                            onChange={(e) => setSCFormData({...SCformData, creativity_and_innovation_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.creativity_and_innovation_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.creativity_and_innovation_3}
                            onChange={(e) => setSCFormData({...SCformData, creativity_and_innovation_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.creativity_and_innovation_4}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.creativity_and_innovation_4}
                            onChange={(e) => setSCFormData({...SCformData, creativity_and_innovation_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.creativity_and_innovation_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.creativity_and_innovation_comment}
                            onChange={(e) => setSCFormData({...SCformData, creativity_and_innovation_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="com" title={SCDescription.communication}>
                        <label className='label'>{SCDescription.communication_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.communication_1}
                            onChange={(e) => setSCFormData({...SCformData, communication_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.communication_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.communication_2}
                            onChange={(e) => setSCFormData({...SCformData, communication_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.communication_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.communication_3}
                            onChange={(e) => setSCFormData({...SCformData, communication_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.communication_4}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.communication_4}
                            onChange={(e) => setSCFormData({...SCformData, communication_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.communication_5} </label>
                        <select
                            className='modalSelect' 
                            value={SCformData.communication_5}
                            onChange={(e) => setSCFormData({...SCformData, communication_5: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.communication_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.communication_comment}
                            onChange={(e) => setSCFormData({...SCformData, communication_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="col" title={SCDescription.collaboration}>
                        <label className='label'>{SCDescription.collaboration_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.collaboration_1}
                            onChange={(e) => setSCFormData({...SCformData, collaboration_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.collaboration_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.collaboration_2}
                            onChange={(e) => setSCFormData({...SCformData, collaboration_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.collaboration_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.collaboration_3}
                            onChange={(e) => setSCFormData({...SCformData, collaboration_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.collaboration_4}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.collaboration_4}
                            onChange={(e) => setSCFormData({...SCformData, collaboration_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.collaboration_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.collaboration_comment}
                            onChange={(e) => setSCFormData({...SCformData, collaboration_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="c_g_c" title={SCDescription.cultural_and_global_citizenship}>
                        <label className='label'>{SCDescription.cultural_and_global_citizenship_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.cultural_and_global_citizenship_1}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.cultural_and_global_citizenship_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.cultural_and_global_citizenship_2}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.cultural_and_global_citizenship_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.cultural_and_global_citizenship_3}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.cultural_and_global_citizenship_4}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.cultural_and_global_citizenship_4}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.cultural_and_global_citizenship_5} </label>
                        <select
                            className='modalSelect' 
                            value={SCformData.cultural_and_global_citizenship_5}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_5: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.cultural_and_global_citizenship_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.cultural_and_global_citizenship_comment}
                            onChange={(e) => setSCFormData({...SCformData, cultural_and_global_citizenship_comment: e.target.value})}
                        />
                </Tab>
                <Tab eventKey="p_g_w" title={SCDescription.personal_growth_and_wellbeing}>
                        <label className='label'>{SCDescription.personal_growth_and_wellbeing_1}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.personal_growth_and_wellbeing_1}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_1: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.personal_growth_and_wellbeing_2}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.personal_growth_and_wellbeing_2}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_2: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label'>{SCDescription.personal_growth_and_wellbeing_3}</label>
                        <select
                            className='modalSelect'
                            value={SCformData.personal_growth_and_wellbeing_3}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_3: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.personal_growth_and_wellbeing_4}</label>
                        <select
                            className='modalSelect' 
                            value={SCformData.personal_growth_and_wellbeing_4}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_4: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.personal_growth_and_wellbeing_5} </label>
                        <select
                            className='modalSelect' 
                            value={SCformData.personal_growth_and_wellbeing_5}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_5: parseInt(e.target.value)})}
                        >
                        {FivePointScale.map(option => (
                            <option key={option.value} value={option.value}>
                                {option.label}  
                            </option>
                        ))}
                        </select>
                        <br/>
                        <label className='label '>{SCDescription.personal_growth_and_wellbeing_comment} </label>
                        <textarea
                            className="modalTextInput"  
                            value={SCformData.personal_growth_and_wellbeing_comment}
                            onChange={(e) => setSCFormData({...SCformData, personal_growth_and_wellbeing_comment: e.target.value})}
                        />
                </Tab>
            </Tabs>
            <br></br>
            <Separator thickness={4} />
            <br></br>
            <button
                        type="submit"
                        className="modalButton"
                    >
                        儲存S&C Model
                </button>

        </form>
        )}
    </MDBContainer>
    )
}