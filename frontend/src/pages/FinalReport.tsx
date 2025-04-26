import '../styles/styles.css';
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import {Profile, Final_Report, Final_Report_Modal, ACRecord, SCRecord, CommentSelectData, Final_Report_Comment, Social_Style, FinalSocialStyle, SAndCModelScores, ACModelScores, SubjectComment} from '../Interface';
import {SCDescription, ACDescription} from '../Constants';
import {getProfile, getFinalReport, getCommentList, getSocialStyle, getSubjectComments, getPreACRecord} from '../API';
import {MDBCol, MDBContainer, MDBRow} from 'mdb-react-ui-kit';
import { BlockTitle, Separator } from '../components/Utils';
import { FaEdit, FaTimes, FaPlusCircle } from "react-icons/fa"
import {SocialStyleModal, SubjectCommentModal} from '../components/HandleAdding';
import {Tabs, Tab } from 'react-bootstrap';
import {ACModal, SCModal} from '../components/ModelRecord';
import {SocialStyleChart, ModelChart} from '../components/RadarChart';
import GPT from '../components/GPT';
import StudentReview from '../components/StudentReview';


const FinalReportComment: React.FC<Final_Report_Comment> = (comment_list)   => {
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
        <MDBCol className='scrollable' style={{height: '50vh', overflowY: 'scroll'}}>
            {comment_list.comment_list.map((comment, index) => (
                <div key={index} className = 'dashboard-component-background'>
                    <MDBRow onClick={() => toggleExpanded(index)}
                            style={{ cursor: 'pointer', }}>
                            <h5>
                                {comment.model_chinese} : {comment.score}
                            </h5>
                    </MDBRow>
                    {isExpanded(index) && (
                        <MDBContainer className='section-content'>
                            評語: {comment.comment}
                        </MDBContainer>
                    )}
                </div>
            ))}
        </MDBCol>
    )
}


function FinalReport() {
    const [profile, setProfile] = useState<Profile | null>(null)
    const [finalReport, setFinalReport] = useState<Final_Report |null>(null)
    const [error, setError] = useState<string | null>(null)
    const [ACScores, setACScores] = useState<number[]>([])
    const [preACScores, setPreACScores] = useState<number[]>([])
    const [SCScores, setSCScores] = useState<number[]>([])
    const [SSScores, setSSScores] = useState<number[]>([])
    const [SSRecord, setSSRecord] = useState <FinalSocialStyle | null> (null)
    const [acRecord, setACRecord] = useState<ACRecord | null> (null)
    const [scRecord, setSCRecord] = useState<SCRecord | null> (null)
    const [showSSModal, setShowSSModal] = useState(false)
    const [showACModal, setShowACModal] = useState(false)
    const [showSCModal, setShowSCModal] = useState(false)
    const [showSubComModal, setShowSubComModal] = useState(false)
    const [commentList, setCommentList] = useState<CommentSelectData | null>(null)
    const [allAC, setAllAC] = useState<boolean>(true)
    const [allPreAC, setAllPreAC] = useState<boolean>(true)
    const [allSC, setAllSC] = useState<boolean>(true)
    const [hasSS, setHasSS] = useState<boolean>(true)
    const [SocialStyles, setSocialStyles] = useState<Social_Style []>([])
    const [SubjectComments, setSubjectComments] = useState<SubjectComment[]>([])

  
    const EditSTIcon = () => {
        const iconSize = '2vw'; // You can adjust the size as needed
        return (
            <>
                {showSSModal ? (
                    <FaTimes 
                        onClick={() => setShowSSModal(false)} 
                        style={{ fontSize: iconSize }} 
                    />
                ) : (
                    <FaEdit 
                        onClick={() => setShowSSModal(true)} 
                        style={{ fontSize: iconSize }} 
                    />
                )}
            </>
        );
    };

    const EditSCIcon = () => {
        const iconSize = '2vw'; // You can adjust the size as needed
        return (
            <>
                {showSCModal ? (
                    <FaTimes 
                        onClick={() => setShowSCModal(false)} 
                        style={{ fontSize: iconSize }} 
                    />
                ) : (
                    <FaEdit 
                        onClick={() => setShowSCModal(true)} 
                        style={{ fontSize: iconSize }} 
                    />
                )}
            </>
        );
    };

    const EditACIcon = () => {
        const iconSize = '2vw'; // You can adjust the size as needed
        return (
            <>
                {showACModal ? (
                    <FaTimes 
                        onClick={() => setShowACModal(false)} 
                        style={{ fontSize: iconSize }} 
                    />
                ) : (
                    <FaEdit 
                        onClick={() => setShowACModal(true)} 
                        style={{ fontSize: iconSize }} 
                    />
                )}
            </>
        );
    };

    const EditSubComIcon = () => {
        const iconSize = '2vw'; 
        return (
            <>
                {showSubComModal ? (
                    <FaTimes 
                        onClick={() => setShowSubComModal(false)} 
                        style={{ fontSize: iconSize }} 
                    />
                ) : (
                    <FaEdit 
                        onClick={() => setShowSubComModal(true)} 
                        style={{ fontSize: iconSize }} 
                    />
                )}
            </>
        );
    }

    useEffect(() => {
        (async () => {
            getFinalReport()
                .then((data) => {
                    // console.log(data)
                    setFinalReport(data)
                    setACScores([])
                    setSCScores([])
                    setSSScores([])
                    {(data.ac_list as Final_Report_Modal[]).map((ac) => {
                        setACScores((prevACScores) => [...prevACScores, ac.score ])
                    })}
                    {(data.s_and_c_list as Final_Report_Modal[]).map((sc) => {
                        setSCScores((prevSCScores) => [...prevSCScores, sc.score ])
                    })}
                    if (data.after_social_style){
                        setSSScores([data.after_social_style.analytical, data.after_social_style.amiable , data.after_social_style.expressive, data.after_social_style.driver])
                    }
                    else {
                        setHasSS(false)
                    }
                    setACRecord(data as ACRecord)
                    setSCRecord(data as SCRecord)
                })
                .catch((e) => {
                    setError(e);
                }
                );
        })();
        (async () => {
            getCommentList()
                .then((data) => {
                    setCommentList(data)
                })
                .catch((e) => {
                    setError(e);
                }
                );
        })();
        (async () => {
            getSocialStyle()
                .then((data) => {
                    // console.log(data)
                    setSocialStyles(data);
                })
                .catch((e) => {
                    setError(e);
                });
        })();
        (async () => {
            getSubjectComments()
                .then((data) => {
                    setSubjectComments(data);
                })
                .catch((e) => {
                    setError(e);
                });
        })();
        (async () => {
            getProfile(true )
                .then((data) => {
                    setProfile(data);
                })
                .catch((e) => {
                    setError(e);
                });
        })();
        (async () => {
            getPreACRecord()
                .then((data) => {
                    if (data != undefined){
                        setPreACScores([data.learning_strategy, data.goal_setting, data.organising, data.motivation_and_accountability, data.time_management, data.life_balance])
                    }
                })
                .catch((e) => {
                    setError(e);
                });
        })();
    }
    , []);

    useEffect(() => {
        ACScores.map((score) => {
            if (score <= 0){
                setAllAC(false)
            }   
        })
    }
    , [ACScores]);

    useEffect(() => {
        preACScores.map((score) => {
            if (score <= 0){
                setAllPreAC(false)
            }   
        })
    }, [preACScores])

    useEffect(() => {
        SCScores.map((score) => {
            if (score <= 0){
                setAllSC(false)
            }
        })
    }
    , [SCScores]);

    useEffect(() => {
        if (finalReport && SocialStyles.length>0){
            const SSRecord = {
                    id: finalReport.id,
                    before_social_style: finalReport.before_social_style? finalReport.before_social_style.id : -1,
                    after_social_style: finalReport.after_social_style? finalReport.after_social_style.id : -1,
                    social_style_type: finalReport.social_style_type? finalReport.social_style_type : "",
                    social_style_comment: finalReport.social_style_comment? finalReport.social_style_comment : "",
                }
            setSSRecord(SSRecord)
        }
    }
    , [finalReport, SocialStyles]);


    const SocialStyleChartData = {
        labels: ['分析型', '友善型', '表達型', '推動型'],
        pre_values: [],
        post_values: SSScores,
    }

    const SCradarChartData = {
        labels: [ SCDescription.critical_thinking, SCDescription.problem_solving, SCDescription.managing_information, SCDescription.creativity_and_innovation, SCDescription.communication, SCDescription.collaboration, SCDescription.cultural_and_global_citizenship, SCDescription.personal_growth_and_wellbeing],
        pre_values: [],
        post_values: SCScores,
    }

    const ACradarChartData = {
        labels: [ ACDescription.learning_strategy, ACDescription.goal_setting, ACDescription.organising, ACDescription.motivation_and_accountability, ACDescription.time_management, ACDescription.life_balance,],
        pre_values: allPreAC? preACScores : [],
        post_values: ACScores,
    };



    return (
        <>
        <Header />
            <MDBContainer>
                <div className='final-dashboard-title-div'>
                        <h3 className='final-dashboard-title'> 1. 待人處事風格 </h3>
                        <EditSTIcon/>
                </div>
                <div className='final-dashboard-container'>  
                    {!showSSModal && (
                        <MDBRow>
                            <MDBCol size="8" className="text-center">
                            { hasSS && <SocialStyleChart data=  {SocialStyleChartData} />} 
                            {!hasSS && (
                                <div className='final-dashboard-missing'>
                                    <h4>請先選擇待人處事風格</h4>
                                </div>
                            )}
                            </MDBCol>
                            <MDBCol size="4" className="text-center">
                                {finalReport && SSRecord && (
                                    <div className='dashboard-component-background'>
                                        <MDBRow>
                                            <h5>{SSRecord.social_style_type}</h5>
                                        </MDBRow>
                                        <Separator/>                                        
                                        <MDBRow>
                                            <h5>{SSRecord.social_style_comment}</h5>
                                        </MDBRow>
                                    </div>
                                )}
                            </MDBCol>
                        </MDBRow>
                    )}
                    {showSSModal && finalReport && SSRecord && SocialStyles.length>0 && (
                        <MDBRow>      
                            <MDBCol size="6" className="text-center"> 
                            <Tabs defaultActiveKey="gpt" id="social-style-gpt">
                                <Tab eventKey="student" title="學生檔案">
                                {finalReport && profile && <StudentReview profile={profile} sc_scores={finalReport.s_and_c_scores as SAndCModelScores} ac_scores={finalReport.ac_scores as ACModelScores}/> }

                                </Tab>
                                <Tab eventKey="gpt" title="GPT評語">
                                {commentList && <GPT comments={commentList} section = "social_style"/>}
                                </Tab>
                            </Tabs>
                            </MDBCol>
                            <MDBCol size="6" className="test-center">
                                <SocialStyleModal finalSocialStyle={SSRecord} social_styles={SocialStyles}/>
                            </MDBCol>
                        </MDBRow> 
                    )}     
                </div>


                <div className='final-dashboard-title-div'>
                        <h3 className='final-dashboard-title'> 2. 綜合學生能力</h3>
                        <EditSCIcon/>
                </div>
                <div className='final-dashboard-container'>  
                    {!showSCModal && (
                        <MDBRow>
                            <MDBCol size="8" className="text-center">
                                {allSC && <ModelChart data={SCradarChartData} />}
                                {!allSC && (
                                    <div className='final-dashboard-missing'>
                                        <h4>請先完成所有項目評分</h4>
                                    </div>
                                )}
                            </MDBCol>
                            <MDBCol size="4" className="text-center">
                                {finalReport && <FinalReportComment comment_list = {finalReport.s_and_c_list as Final_Report_Modal[]}/>}
                            </MDBCol>
                        </MDBRow>
                    )}
                    {showSCModal && scRecord && (
                        <MDBRow>      
                            <MDBCol size="6" className="text-center"> 
                            <Tabs defaultActiveKey="gpt" id="sc-gpt">
                                <Tab eventKey="student" title="學生檔案">
                                {finalReport && profile && <StudentReview profile={profile} sc_scores={finalReport.s_and_c_scores as SAndCModelScores} ac_scores={finalReport.ac_scores as ACModelScores}/> }

                                </Tab>
                                <Tab eventKey="gpt" title="GPT評語">
                                {commentList && <GPT comments={commentList} section = "s_and_c"/>}
                                </Tab>
                            </Tabs>
                            </MDBCol>
                            <MDBCol size="6" className="test-center">
                                <SCModal SCRecord={scRecord}/>
                            </MDBCol>
                        </MDBRow> 
                    )}     
                </div>


                <div className='final-dashboard-title-div'>
                    <h3 className='final-dashboard-title'> 3.學業培導能力</h3>
                    <EditACIcon/>   
                </div>
                <div className='final-dashboard-container'>  
                    {!showACModal && (
                        <MDBRow>
                            <MDBCol size="8" className="text-center">
                                {allAC && <ModelChart data={ACradarChartData} />}
                                {!allAC && (
                                    <div className='final-dashboard-missing'>
                                        <h4>請先完成所有項目評分</h4>
                                    </div>
                                )}
                            </MDBCol>
                            <MDBCol size="4" className="text-center">
                                {finalReport && <FinalReportComment comment_list = {finalReport.ac_list as Final_Report_Modal[]}/>}
                            </MDBCol>
                        </MDBRow>
                    )}
                    {showACModal && acRecord && (
                        <MDBRow>      
                            <MDBCol size="6" className="text-center"> 
                            <Tabs defaultActiveKey="gpt" id="ac-gpt">
                                <Tab eventKey="student" title="學生檔案">
                                {finalReport && profile && <StudentReview profile={profile} sc_scores={finalReport.s_and_c_scores as SAndCModelScores} ac_scores={finalReport.ac_scores as ACModelScores}/> }
                                </Tab>
                                <Tab eventKey="gpt" title="GPT評語">
                                    {commentList && <GPT comments={ commentList} section = "ac"/>}
                                </Tab>
                            </Tabs>
                            </MDBCol>
                            <MDBCol size="6" className="test-center">
                                <ACModal ACRecord={acRecord} isFinal={true}/>
                            </MDBCol>
                        </MDBRow> 
                    )}     
                </div>


                <div className='final-dashboard-title-div'>
                        <h3 className='final-dashboard-title'> 4.個人表現及成績 </h3>
                        <EditSubComIcon/>
                </div>
                <div className='final-dashboard-container'>  
                    { !showSubComModal && profile && (
                        <MDBCol className='scrollable' style={{height: '40vh', overflowY: 'scroll'}}>
                        {profile.subjects.map((subject) => (
                            <div className = 'dashboard-component-background'>
                                <MDBRow>
                                    <MDBCol>
                                        <h5>
                                            {subject.display_name} : 
                                        </h5>
                                            {SubjectComments.map((comment) => {
                                                if (comment.subject === subject.id){
                                                    return (
                                                        <h6>
                                                            {comment.subject_comment}
                                                        </h6>
                                                    )
                                                }
                                            })}
                                    </MDBCol>
                                </MDBRow>
                            </div>
                        ))}
                        <div className = 'dashboard-component-background'>
                            <MDBRow>
                                <MDBCol>
                                    <h5>
                                        整體評語 : 
                                    </h5>
                                    <h6>
                                        {finalReport && finalReport.subject_comment}
                                    </h6>
                                </MDBCol>
                            </MDBRow>
                        </div>
                        </MDBCol>
                    )
                    }
                    { showSubComModal && profile && finalReport && (
                        <MDBRow>      
                        <MDBCol size="6" className="text-center"> 
                        <Tabs defaultActiveKey="gpt" id="ac-gpt">
                            <Tab eventKey="student" title="學生檔案">
                            {finalReport && profile && <StudentReview profile={profile} sc_scores={finalReport.s_and_c_scores as SAndCModelScores} ac_scores={finalReport.ac_scores as ACModelScores}/> }
                            </Tab>
                            <Tab eventKey="gpt" title="GPT評語">
                                {commentList && <GPT comments={ commentList} section = "subject"/>}
                            </Tab>
                        </Tabs>
                        </MDBCol>
                        <MDBCol size="6" className="test-center">
                            <SubjectCommentModal report_id={finalReport.id}subjects={profile.subjects} subject_comments={SubjectComments} general_comment={finalReport.subject_comment}/>
                        </MDBCol>
                    </MDBRow> 

                    )   
                    }    

                    
                </div>
                
                


            </MDBContainer>

        </>
    )
}


export default FinalReport;