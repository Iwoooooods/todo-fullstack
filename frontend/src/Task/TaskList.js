import Task from "./Task";
import {useState} from "react";
import ConfirmDialog from "../Components/ConfirmDialog";
import {useCurrentUser} from "../Context";

export default function TaskList({fetcheInprocessTasks, fetcheCompletedOrOverdueTasks, tasks}) {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [currentTask, setCurrentTask] = useState({});
    const [showConfirm, setShowConfirm] = useState(false);
    const {currentUser} = useCurrentUser();

    const handleDelete = async () => {
        try {
            const resp = await fetch(`${BASE_URL}/api/tasks/delete_task?task_id=${currentTask.id}&user_id=${currentUser.id}`,
                {method: 'DELETE',}
            );
            console.log("Delete successfully:", resp);
            if (resp.status === 200) {
                const result = await resp.json();
                alert(result.msg);
                fetcheInprocessTasks();
            }
        } catch (error) {
            console.log(error.message);
        } finally {
            setShowConfirm(false);
        }
    }

    return (
        <div>
            <ConfirmDialog onCancel={() => setShowConfirm(false)} onConfirm={handleDelete} isOpen={showConfirm}>
                <p>Are you sure you want to delete this task?</p>
            </ConfirmDialog>
            {tasks.map((task) => (
                <Task
                    key={task.id}
                    task={task}
                    setShowConfirm={setShowConfirm}
                    deleteCurrentTask={setCurrentTask}
                    fetcheInprocessTasks={fetcheInprocessTasks}
                    fetcheCompletedOrOverdueTasks={fetcheCompletedOrOverdueTasks}
                />
            ))}
        </div>
    );
}
