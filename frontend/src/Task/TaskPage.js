import {useEffect, useState} from "react";
import TaskList from "./TaskList";
import TaskForm from "./CreateComponent/TaskForm";
import CompletedOrOverdueTasks from "./CompletedOrOverdueTasks";
import WarningDialog from "../Components/WarningDialog";
import {useCurrentUser} from "../Context";

export default function TaskPage() {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [inProcessTasks, setInProcessTasks] = useState([]);
    const [completedOrOverdueTasks, setCompletedOrOverdueTasks] = useState([])
    const [showWarning, setShowWarning] = useState(false);
    const [warningTaskNum, setWarningTaskNum] = useState(0)
    const {currentUser} = useCurrentUser()

    async function fetcheInprocessTasks() {
        try {
            const resp = await fetch(`${BASE_URL}/api/tasks/in_process/${currentUser.id}`)
            const result = await resp.json();
            if (resp.status === 200) {
                const tasks = result["tasks"];
                setInProcessTasks(() => ([...tasks]));
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function fetcheCompletedOrOverdueTasks() {
        try {
            const resp = await fetch(`${BASE_URL}/api/tasks/completed_or_overdue/${currentUser.id}`)
            const result = await resp.json();
            if (resp.status === 200) {
                const tasks = result["tasks"];
                setCompletedOrOverdueTasks(() => ([...tasks]));
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    async function fetchWarningTaskNum() {
        try {
                const resp = await fetch(`${BASE_URL}/api/tasks/warning/${currentUser.id}`);
                const result = await resp.json();

                if (resp.status === 200 && result["warning_task_num"] > 0) {
                    setShowWarning(true);
                    setWarningTaskNum(result["warning_task_num"]);
                }

            } catch (error) {
                console.error(error)
            }
    }

    //render warning message if user's tasks' remaining time is less than 24 hours
    useEffect(() => {
        (async () => {
            await fetcheInprocessTasks();
            await fetcheCompletedOrOverdueTasks();
            await fetchWarningTaskNum();
        })();
    }, [currentUser])


    return (
        <div className="task-page-container">
            <WarningDialog showWarning={showWarning} setShowWarning={setShowWarning}
                           message={`There are ${warningTaskNum} tasks overdue today! Hurry up!!`}/>
            <TaskForm fetchTasks={fetcheInprocessTasks}/>
            <TaskList tasks={inProcessTasks} fetcheInprocessTasks={fetcheInprocessTasks}
                      fetcheCompletedOrOverdueTasks={fetcheCompletedOrOverdueTasks}/>
            <CompletedOrOverdueTasks tasks={completedOrOverdueTasks} fetcheInprocessTasks={fetcheInprocessTasks}
                                     fetcheCompletedOrOverdueTasks={fetcheCompletedOrOverdueTasks}/>
        </div>
    );
}
