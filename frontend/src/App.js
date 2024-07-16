import {Routes, Route} from "react-router-dom";
import TaskPage from "./Task/TaskPage";
import {RequireToken} from "./LoginPage/Auth";
import Hello from "./LoginPage/Hello";
import {UserContextProvider} from "./Context";


export default function App() {
    return (
        <UserContextProvider>
            <div className="App">
                <Routes>
                    <Route path="/" element={<Hello/>}></Route>
                    <Route path="/my_tasks" element={
                        // <TaskPage/>
                        <RequireToken>
                            <TaskPage/>
                        </RequireToken>
                    }/>
                </Routes>
            </div>
        </UserContextProvider>

    )
}