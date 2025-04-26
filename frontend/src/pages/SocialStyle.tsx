import '../styles/styles.css';
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import { Social_Style } from '../Interface';
import {getSocialStyle} from '../API';
import { MDBCol, MDBContainer, MDBRow } from 'mdb-react-ui-kit';
import { BlockTitle, Separator } from '../components/Utils';
import moment from 'moment';
import {SocialStyleScoreModal} from '../components/HandleAdding';


function SocialStyle() {
    const [socialStyle, setSocialStyle] = useState<Social_Style[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [showScoreInput, setShowScoreInput] = useState<boolean>(false);
    const [showQuestionnaire, setShowQuestionnaire] = useState<boolean>(false);

    const AddScoreRecord = () => {
        if (showQuestionnaire) {
            setShowQuestionnaire(false);
        }
        if (showScoreInput) {
            setShowScoreInput(false);
        }
        else{
            setShowScoreInput(true);        
        }
    }

    const AddQuestionRecord = () => {
        if (showScoreInput) {
            setShowScoreInput(false);
        }
        if (showQuestionnaire) {
            setShowQuestionnaire(false);
        }
        else{
            setShowQuestionnaire(true);        
        }
    }


    useEffect(() => {
        (async () => {
            getSocialStyle()
                .then((data) => {
                    setSocialStyle(data);
                })
                .catch((e) => {
                    setError(e);
                });
        })();
    }, []);

    return (
        <>
            <Header />
            <h3 style={{fontWeight: 'bold', marginLeft:'4%'}}> 待人處事風格 </h3>
            <MDBContainer className="dashboard-component-background">

                <BlockTitle titles={["提交日期", "分析型", "友善型", "表達型", "推動型"]}/>
                <Separator thickness={4}/>
                {socialStyle && socialStyle.map((style, index) => (
                    <div key={index} className="social-style-container">
                            <MDBRow className="scrollbar">
                                <MDBCol >
                                    {moment(style.created_at).format('DD/MM/YYYY')}
                                </MDBCol>
                                <MDBCol>
                                    {style.analytical}
                                </MDBCol>
                                <MDBCol>
                                    {style.amiable}
                                </MDBCol>
                                <MDBCol>
                                    {style.expressive}
                                </MDBCol>
                                <MDBCol>
                                    {style.driver}
                                </MDBCol>
                            </MDBRow>
                    </div>
                ))}
            </MDBContainer>
            <div style={{  display: 'flex',
                justifyContent: 'center', /* Center align the buttons */
                marginTop: '20px'}}>
                    <button className='modalButton' onClick={AddScoreRecord}>
                        新增記錄
                    </button>
                    <div style={{ width: '3%' }} /> {/* Spacer */}
                    {/* <button className='modalButton' onClick={AddQuestionRecord}>
                        完成問卷
                    </button> */}
            </div>
            {showScoreInput && <SocialStyleScoreModal />}

        </>
    )
}

export default SocialStyle;
