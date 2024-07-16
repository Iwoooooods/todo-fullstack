import Task from "./Task";
import {useState} from "react";
import ConfirmDialog from "../Components/ConfirmDialog";
import './completed_or_overdue.css'

export default function CompletedOrOverdueTasks({ fetcheInprocessTasks, fetcheCompletedOrOverdueTasks, tasks }) {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [currentTask, setCurrentTask] = useState({});
    const [showConfirm, setShowConfirm] = useState(false);

  const handleDelete = async ()=>{
    try{
        const resp = await fetch(`${BASE_URL}/api/tasks/delete_task/${currentTask.id}`,
            {method: 'DELETE',}
        );
        const result = await resp.json();
        if (resp.status === 200){
            console.log("Delete successfully:", result);
            fetcheCompletedOrOverdueTasks();
        }
    }catch (error){
        console.error('Error:',error);
    }finally{
        setShowConfirm(false);
    }
  }

  return (
    <div className="completed-or-overdue-tasks">
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
