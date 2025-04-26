import '../styles/styles.css';
import React, {  useEffect, useState } from 'react';
import Header from '../components/Header';
import {getPreACRecord, addPreACRecord} from '../API';
import {PreACRecordForm, ACDescription, FivePointScale} from '../Constants';
import {Pre_ACRecord} from '../Interface';
import {Modal} from '../styles/style.const';


function PreACRecord() {
    const [preACRecord, setPreACRecord] = useState<Pre_ACRecord>(PreACRecordForm);
    const [error, setError] = useState<string | null>(null);
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        addPreACRecord(preACRecord)
    }

    const handleNull = (value: any) => {
        if (value === null || value === undefined){
            return -1
        }
        return value
    }

    useEffect(() => {
        (async () => {
            getPreACRecord()
                .then((data) => {
                    if(data === undefined){
                        setPreACRecord(PreACRecordForm);
                    }
                    else{
                        for (let key in data){
                            data[key] = handleNull(data[key]);
                        }
                        setPreACRecord(data);
                    }
                })
                .catch((e) => {
                    setError(e);
                });
        })();
    }, []);


    return (
        <>
            <Header />
            <h3 style={{fontWeight: 'bold', marginLeft:'4%'}}> Pre-AC Focus </h3>
            <Modal>
                <form onSubmit={handleSubmit}>
                <label className='label'>{ACDescription.learning_strategy}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.learning_strategy}
                    onChange={(e) => setPreACRecord({...preACRecord, learning_strategy: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <label className='label'>{ACDescription.goal_setting}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.goal_setting}
                    onChange={(e) => setPreACRecord({...preACRecord, goal_setting: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <label className='label'>{ACDescription.organising}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.organising}
                    onChange={(e) => setPreACRecord({...preACRecord, organising: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <label className='label'>{ACDescription.motivation_and_accountability}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.motivation_and_accountability}
                    onChange={(e) => setPreACRecord({...preACRecord, motivation_and_accountability: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <label className='label'>{ACDescription.time_management}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.time_management}
                    onChange={(e) => setPreACRecord({...preACRecord, time_management: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <label className='label'>{ACDescription.life_balance}: </label>
                <select
                    className='modalSelect'
                    value={preACRecord.life_balance}
                    onChange={(e) => setPreACRecord({...preACRecord, life_balance: parseInt(e.target.value)})}
                >
                {FivePointScale.map((option, index) => (
                    <option key={index} value={index}>{option.label}</option>
                ))}
                </select>
                <br></br>
                <button type="submit" className="modalButton">儲存AC</button>   
                </form>
            </Modal>
        </>
    );
}

export default PreACRecord;