/**
 * Header.tsx
 * 
 * Renders the header navigation bar.
 * 
 * Has logo, nav links, and sign out button.
 * Uses React Bootstrap for layout.
 * 
 * @key Renders navbar
 * @key Has logo, links, profile
 * @key Sign out button
*/


import React, { useState, useEffect } from 'react';
import { Navbar, Nav, NavDropdown, Container } from 'react-bootstrap';
import {getStudentList, signout} from '../API';
import '@fortawesome/fontawesome-free/css/all.min.css'
import logo from '../assets/brand_logo/Logo_Rect.png'
import {Separator} from './Utils';
import { Route, useNavigate } from 'react-router-dom';
import { set } from 'lodash';


const styles = {
    navItemText: {
        fontFamily: 'Montserrat',
        fontStyle: 'normal',
        fontWeight: 'bold' as const,
        fontSize: '20px',
        lineHeight: '20px',
        alignItems: 'center',
        textTransform: 'uppercase' as const,
        color: '#0A4072',
    }
}

interface Profile {
    id: string;
    name: string;
}


export default function Header() {
    const [selectedProfile, setSelectedProfile] = useState<string | null>(localStorage.getItem('student_id'));
    const [profiles, setProfiles] = useState<Profile[]>([]);
    const [role, setRole] = useState<string | null>('student');
    const [userName, setUserName] = useState<string | null>('');
    const [coachID, setCoachID] = useState<string | null>(localStorage.getItem('coach_id'));

    useEffect(() => {
        const fetchStudentList = async () => {
            try {
                const student_list = await getStudentList();
                setRole(student_list.role);
                setProfiles(student_list.profiles); // Set the fetched profiles in the state
                setUserName(student_list.user_name);
                if (coachID !== student_list.coach.id){
                    setCoachID(student_list.coach.id);
                    localStorage.setItem('coach_id', student_list.coach.id);
                }
            } catch (error) {
                // Handle error if necessary
                console.error("Error fetching student list:", error);
            }
        };
        fetchStudentList();
    }, []);


    const navigate = useNavigate();

    const handleSelectedProfile = (eventKey: string | null) => {
            if (eventKey as string !== selectedProfile) {
                setSelectedProfile(eventKey as string);
                sessionStorage.clear();
                localStorage.setItem('student_id', eventKey as string);
                window.location.reload();
            }
        }

    const handleSignOut = async ()=> {
        const response = signout();
        if((await response).status){
            localStorage.clear();
            sessionStorage.clear();
            navigate('/')
        }
    }

    return (
        <>
            <Navbar expand="lg" className='navbar navbar-expand-lg navbar-light'>
                <Container>

                    <Navbar.Brand href="/dashboard">
                        <img
                            src={logo}
                            alt='logo'
                            height="80"
                            className="d-inline-block align-top"

                        />
                    </Navbar.Brand>

                    <Navbar.Toggle aria-controls="basic-navbar-nav" />

                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="me-auto">
                            <Nav>
                                {role === "coach" && (
                                <NavDropdown
                                    style={styles.navItemText}
                                    title={selectedProfile ? (profiles.find(function (profile) {
                                        return Number(profile.id) ===  Number(selectedProfile);
                                    }) || {}).name || 'Select a Profile' : 'Select a Profile'}
                                    id="profile-dropdown"
                                    onSelect={handleSelectedProfile}
                                >
                                    {profiles && profiles.map((profile) => (
                                        <NavDropdown.Item key={profile.id} eventKey={profile.id}
                                        active={selectedProfile === profile.id.toString()} // Check if the profile is selected
                                        >
                                            {profile.name}
                                        </NavDropdown.Item>
                                    ))}
                                </NavDropdown>
                                )}
                                {role === "student" && (
                                    <Nav.Link
                                    style={styles.navItemText}
                                    href="">
                                    {userName}
                                    </Nav.Link>
                                )}
                            </Nav>

                            {/* <NavDropdown
                                style={styles.navItemText}
                                title="Past Record" id="basic-nav-dropdown">
                                <NavDropdown.Item href="/goals">Goal</NavDropdown.Item>
                                <NavDropdown.Item href="/tasks">Task</NavDropdown.Item>
                                <NavDropdown.Item href="/methods">Method</NavDropdown.Item>
                            </NavDropdown> */}
 
                            {role=="coach" && (
                                    // <Nav.Link
                                    // style={styles.navItemText}
                                    // href="">
                                    // Coaching Report
                                    // </Nav.Link>
                            <NavDropdown
                                style={styles.navItemText}
                                title="Coaching Report" id="report-dropdown">
                                <NavDropdown.Item href="/session_report">Session Report</NavDropdown.Item>
                                <NavDropdown.Item href="/final_report">Final Report</NavDropdown.Item>
                                <NavDropdown.Item href="/pre_ac_record">Pre Academic Focus</NavDropdown.Item>
                                {/* <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item> */}
                            </NavDropdown>
                            
                            )}
                            {role=="coach" && (
                            <NavDropdown
                            style={styles.navItemText}
                            title="Other"
                            id="other-dropdown"
                            >
                            <NavDropdown.Item href="/social_style">Social Style</NavDropdown.Item>

                            </NavDropdown>    
                            )}

                        </Nav>
                        
                       <Nav.Link
                            style={styles.navItemText}
                            onClick={handleSignOut}
                            >signout
                        </Nav.Link>

                        <Nav>
                            {/* <Nav.Link href="#profile">

                            </Nav.Link> */}
                        </Nav>

                    </Navbar.Collapse>
                </Container>
            </Navbar>
            {/* <Separator thickness={4} margin={0}/> */}
        </>
    );
}