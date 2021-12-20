import React, {useEffect, useState} from 'react';
import Navbar from "./Navbar";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Registration from "./Registration";
import Login from "./Login";
import {getCurrentUser} from "../utils/user";
import StatsEmployee from './StatsEmployee';
import StatsPatient from './StatsPatient';
import Financing from './Financing';
import Reviews from './Reviews';
import LoginButton from './LoginButton';

function App() {
    const [currentUser, setCurrentUser] = useState(null);

    useEffect(() => {
        const user = getCurrentUser();
        if (user) setCurrentUser(user);
    }, []);


    return (
        <BrowserRouter>
                <Navbar/>
                {!currentUser && 
                    <Switch>
                        <Route path="/registration" component={Registration}/>
                        <Route path="/login" component={Login}/>
                        <Route path="/loginet" component={LoginButton}/>
                    </Switch>
                }
                {currentUser && 
                    <Switch>
                        <Route path="/employee_stats" component={StatsEmployee}/>
                        <Route path="/patient_stats" component={StatsPatient}/>
                        <Route path="/financing" component={Financing}/>
                        <Route path="/reviews" component={Reviews}/>
                    </Switch>
                }
        </BrowserRouter>
    );
}

export default App;
