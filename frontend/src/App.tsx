import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import SignInSignUp from './pages/SignInSignUp';
import Dashboard from './pages/Dashboard';
import SessionReport from './pages/SessionReport';
import FinalReport from './pages/FinalReport';
import SocialStyle from './pages/SocialStyle';
import PreACRecord from './pages/PreACRecord';
import 'bootstrap/dist/css/bootstrap.min.css';


const styles = {
  background: {
    background: '#d6e7ef',
    minHeight: '100vh',
    margin: 0,
    padding: 20,
    boxSizing: 'border-box' as const,

    fontFamily: "'Noto Sans TC', sans-serif" as const,

  }
}

const AuthenticatedRoute = ({ element }: { element: React.ReactNode }) => {
  // Add your authentication logic here
  const isAuthenticated = localStorage.getItem('token') !== null;

  return isAuthenticated ? element : <Navigate to="/" />;
};

function App() {
  return (
    <>

      <div style={styles.background}>
        <BrowserRouter>
          <Routes>
            {/* Use the AuthenticatedRoute for the dashboard */}
            <Route path="/dashboard" element={<AuthenticatedRoute element={<Dashboard />} />} />
            <Route path="/session_report" element={<AuthenticatedRoute element={<SessionReport />} />} />
            <Route path="/final_report" element={<AuthenticatedRoute element={<FinalReport />} />} />
            <Route path="/social_style" element={<AuthenticatedRoute element={<SocialStyle />} />} />
            <Route path="/pre_ac_record" element={<AuthenticatedRoute element={<PreACRecord />} />} />
            {/* Non-authenticated users will see the sign-in/sign-up page */}
            <Route path="/" element={<SignInSignUp />} />
          </Routes>
        </BrowserRouter>
      </div>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap');
      </style>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@900&family=Noto+Sans+TC:wght@500&display=swap');
      </style>
    </>
  )
}

export default App;
