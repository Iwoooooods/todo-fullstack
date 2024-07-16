
export default function WarningDialog({showWarning, setShowWarning, message}) {
    if (!showWarning){
        return null
    }else {
        return (
            <div className="warningContainer">
                <div className="overlay"></div>
                <div className="warning dialog">
                    <div>{message}</div>
                    <button className="okButton" onClick={() => setShowWarning(false)}>ok</button>
                </div>
            </div>)
    }
}