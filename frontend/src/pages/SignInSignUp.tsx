import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Tabs,
    Tab,
    Button,
    Form,
    FormControl,
    FormGroup,
    FormLabel
} from 'react-bootstrap';
import {signin} from '../API';
import logo from '../assets/brand_logo/Logo_Rect.png'


interface SignInFormData {
    username: string;
    password: string;
}

interface LogoProps {
    src: string;
    alt: string;
    style: React.CSSProperties;
}

const Logo: React.FC<LogoProps> = ({ src, alt, style }) => (
    <div className=" text-center">
      <img
        src={src}
        alt={alt}
        style={style}
        className="d-inline-block align-top"
      />
    </div>
  );


function SignInSignUp() {

    const navigate = useNavigate();

    const [key, setKey] = useState<string>('login');

    const [signInData, setSignInData] = useState<SignInFormData>({
        username: '',
        password: ''
    });

    const logoStyle = {
        height: '30vh', // 15% of the viewport height
        margin: 'auto', // Center horizontally
        display: 'block', // Center horizontally
      };

    const handleSignInChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setSignInData(prev => ({
            ...prev,
            [name]: value
        }));
    }


    const handleSignInSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        signin(signInData)
        .then(res => res.json())
        .then(data => {
            if(data.token){
                localStorage.setItem('token', data.token)
                navigate(`/dashboard`, {replace: true})
            }
            else{
                console.log(data.error)
            }})
    }

    useEffect(() => {
        const isAuthenticated = localStorage.getItem('token') !== null;
        if (isAuthenticated) {        
            navigate('/dashboard', { replace: true });
        }else{   
        setSignInData({
            username: '',
            password: ''
        })}

    }, [])

    return (
        <div>
        <Logo src={logo} alt="logo" style={logoStyle} />
        
        <Container className="w-50 ">

            {/* <Tabs
                activeKey={key}
                onSelect={(k) => {
                    if (k === null) return;
                    setKey(k)
                }}
                className="mb-3"
            >

                <Tab eventKey="login" title="Login"> */}

                    <Form onSubmit={handleSignInSubmit}>

                        <FormGroup controlId="username">
                            <FormLabel>Username</FormLabel>
                            <FormControl
                                type="text"
                                name="username"
                                value={signInData.username}
                                onChange={handleSignInChange}
                            />
                        </FormGroup>

                        <FormGroup controlId="password">
                            <FormLabel>Password</FormLabel>
                            <FormControl
                                type="password"
                                name="password"
                                value={signInData.password}
                                onChange={handleSignInChange}
                            />
                        </FormGroup>

                        <Button variant="primary" type="submit" className="mt-3 float-right">
                        Sign In
                        </Button>

                    </Form>

                {/* </Tab> */}

                {/* <Tab eventKey="register" title="Register"> */}

                    {/* Register form */}

                {/* </Tab> */}

            {/* </Tabs> */}
        </Container>
        </div>

    );
}

export default SignInSignUp;