import { useLocation,Navigate } from "react-router-dom"
import {useCurrentUser} from "../Context";
import {useEffect} from "react";

export const setToken = (token)=>{
    localStorage.setItem('token', token)
}

export const fetchToken = (token)=>{
    return localStorage.getItem('token')
}

export function RequireToken({children}){
    const {fetchCurrentUser} = useCurrentUser();
    const location = useLocation()
    useEffect(() => {
        fetchCurrentUser();
    }, []);
    if(!fetchToken()){
        console.log("get back to login")
        return <Navigate to='/' state ={{from : location}}/>;
    }

    return children;
}
