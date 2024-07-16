import {useState} from "react";
import "./task_form.css";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faMinus, faPlus} from '@fortawesome/free-solid-svg-icons';
import {useCurrentUser} from "../../Context";

export default function TaskForm({fetchTasks}) {
    const BASE_URL = process.env.REACT_APP_BASE_URL;
    const [showFrom, setShowForm] = useState(false);
    //allowSubmit is used to control the opacity of the submit button
    const [submitDisabled, setSubmitDisabled] = useState(false);
    const {currentUser} = useCurrentUser()
    //task is used to store the data of the form
    const [task, setTask] = useState({
        title: "",
        content: "",
    });
    const allowSubmit = task.title.trim() === "" || task.content.trim() === "" || submitDisabled;

    function openForm() {
        setShowForm(true);
        setTask({
            user_id: currentUser.id,
            title: "",
            content: "",
        });
    }

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setTask((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleSubmit = async (e) => {
        // prevent the default form submission
        if (submitDisabled) {
            return;
        }
        e.preventDefault();
        // disable the submit button to prevent multiple submissions
        setSubmitDisabled(true);

        const url = `${BASE_URL}/api/tasks/create_task`;
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(task),
        };
        try {
            const response = await fetch(url, options);
            const result = await response.json();
            if (response.status === 201) {
                fetchTasks();
                setShowForm(false);
                setTask({
                    user_id: currentUser.id,
                    title: "",
                    content: "",
                });
                alert("Create Successfully!");
            }else if (response.status === 400) {
                alert("Create Failed!");
            }
        } catch (error) {
            console.log(error);
        } finally {
            setSubmitDisabled(false);
            // console.log(`submit finished: ${submitDisabled}`);
        }
    };

    return (
        <div>
            {!showFrom && <button onClick={() => {
                openForm();
            }} id="add-button">
                <FontAwesomeIcon icon={faPlus}/>
            </button>}
            {showFrom && (
                <form onSubmit={handleSubmit} className="form-container">
                    <button onClick={() => setShowForm(false)} id="cancel-button">
                        <FontAwesomeIcon icon={faMinus}/>
                    </button>
                    <input
                        name="title"
                        value={task.title}
                        onChange={handleInputChange}
                        placeholder="Title(Required)"
                    />
                    <textarea
                        name="content"
                        value={task.content}
                        onChange={handleInputChange}
                        placeholder="Content(Required)"
                    />
                    <input
                        name="brief"
                        value={task.brief}
                        onChange={handleInputChange}
                        placeholder="Brief"
                    />
                    <input
                        type="date"
                        name="deadline"
                        value={task["deadline"]}
                        onChange={handleInputChange}
                        placeholder="Deadline"
                    />
                    <button
                        type="submit"
                        disabled={allowSubmit}
                        className={`submit-button ${allowSubmit ? "disabled" : ""}`}
                        style={{opacity: allowSubmit ? 0.5 : 1}}
                    >
                        submit
                    </button>
                </form>
            )}
        </div>
    );
}
