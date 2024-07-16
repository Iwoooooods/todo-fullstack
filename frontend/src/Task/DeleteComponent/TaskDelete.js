import './delete_task.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes } from '@fortawesome/free-solid-svg-icons';

export default function TaskDeleteButton({task, setCurrentTask, setShowConfirm}) {
    
    const confirmDelete = ()=>{
        setCurrentTask(task);
        setShowConfirm(true);
    }

    return (
    <div>
        <button onClick={()=>confirmDelete()} className="delete-button">
            <FontAwesomeIcon icon={faTimes} style={{width:'40px', height:'40px'}} />
        </button>
    </div>
    )
}