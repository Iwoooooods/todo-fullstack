import './dialog.css'

export default function ConfirmDialog({ onConfirm, onCancel, isOpen, children }) {
  if (!isOpen) {
    return null;
  } else {
    return (
      <>
        <div className="overlay"></div>
        <div className="confirm dialog">
          <div>{children}</div>
          <button onClick={onConfirm}>Confirm</button>
          <button onClick={onCancel}>Cancel</button>
        </div>
      </>);
  }
}

