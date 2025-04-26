import '../styles/styles.css';
import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import {Session_Report, ACRecord } from '../Interface';
import {getSessionReport, getSessionReports} from '../API';
import {MDBCol, MDBContainer, MDBRow} from 'mdb-react-ui-kit';
import {Separator } from '../components/Utils';
import {ReportModal} from '../components/HandleAdding';
import {Tabs, Tab } from 'react-bootstrap';
import {ACModal} from '../components/ModelRecord'





function SessionReport() {
    const [sessionReports, setSessionReports] = useState<Session_Report[]>([])
    const [currReport, setCurrReport] = useState<Session_Report | null> (null)
    const [ACRecord, setACRecord] = useState<ACRecord | null> (null)
    // useState<Session_Report[]>([]);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        (async () => {
            getSessionReports()
                .then((data) => {
                    setSessionReports(data);
                    data.map((report:Session_Report) => {
                        const reportContent = sessionStorage.getItem(`session-report-${report.id}`)
                        if (reportContent === "undefined" || reportContent === null){
                            getSessionReport(report.id.toString())
                            .then((data) => {
                                const session_report: Session_Report = data;
                                sessionStorage.setItem(`session-report-${report.id}`, JSON.stringify(session_report))
                            })
                        }
                    })
                })
                .catch((e) => {
                    setError(e);
                });
        })();
    }, [currReport]);

    const handleTabSelect  = (eventKey: string | null) => {
        if (!eventKey)
            return;
        if (eventKey==='add'){
            setCurrReport(null);
            setACRecord(null);
            return
        }
        const storedReport = sessionStorage.getItem(`session-report-${eventKey}`)
        if (storedReport!="undefined" && storedReport!=null){
            const report: Session_Report = JSON.parse(storedReport) as Session_Report;
            setCurrReport(report);
            if (report){
                setACRecord(report.ACRecord as ACRecord)
            }
        }
        else{
            setCurrReport(null);
            setACRecord(null);
            getSessionReport(eventKey)
                .then((data) => {
                    const report: Session_Report = data;
                    sessionStorage.setItem(`session-report-${eventKey}`, JSON.stringify(report));
                    setCurrReport(report)
                    if (report){
                        setACRecord(report.ACRecord as ACRecord)
                    }
                });
        }
    };

    return (
        <>
        <Header />
        <MDBContainer className="dashboard-component-background">
        <h3 style={{fontWeight: 'bold', marginLeft:'2%'}}> 培導報告 </h3>
        <Separator thickness={2}/>
            <Tabs defaultActiveKey="add" id="session-report" onSelect={handleTabSelect}>
                {sessionReports.map(
                    (report) => (
                        <Tab eventKey={report.id.toString()} title={report.section}>
                        </Tab>
                    )
                )}
                <Tab eventKey="add" title="+">
                    <ReportModal report={null} isEdit={false} sessionNum={sessionReports.length+1}/>
                </Tab>
            </Tabs>
            {currReport && (    
                <MDBContainer>
                <MDBRow>
                <MDBCol size="6" className="text-center">
                    
                    <MDBRow >
                        <ReportModal report={currReport} isEdit={true} sessionNum={currReport.section}/>
                    </MDBRow>
                    
                </MDBCol>
                <MDBCol size="6">
                    {/* Right Section: Display Tab Pages */}
                    {/* <Tabs defaultActiveKey="acModal" id="coachingTabs"> */}
                    {/* <Tab eventKey="acModal" title="AC Modal"> */}
                        {/* {<ACModal ACRecord={currReport.ACRecord}/>} */}
                        {currReport && ACRecord && <ACModal ACRecord={ACRecord} isFinal={false}/>}        

                    
                    {/* </Tab> */}
                    {/* <Tab eventKey="sandcModal" title="S&C Modal"> */}
                    {/* </Tab> */}
                    {/* </Tabs> */}
                </MDBCol>
                </MDBRow>
            </MDBContainer>
        )}
        </MDBContainer>
        </>
    )
}


export default SessionReport;