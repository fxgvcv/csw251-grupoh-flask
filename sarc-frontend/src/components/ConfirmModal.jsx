import React, { useRef, useEffect } from 'react';

function ConfirmModal({ isOpen, title, message, onConfirm, onCancel }) {
  const dialogRef = useRef(null);

  useEffect(() => {
    if (dialogRef.current) {
      if (isOpen) {
        dialogRef.current.showModal();
      } else {
        // Check if the dialog is open before trying to close it
        // This check might not be strictly necessary with showModal if managed correctly,
        // but good for robustness if dialog could be closed by other means (e.g. ESC key)
        if (dialogRef.current.hasAttribute('open')) {
            dialogRef.current.close();
        }
      }
    }
  }, [isOpen]);

  // Handle closing via ESC key
  useEffect(() => {
    const dialogNode = dialogRef.current;
    const handleDialogCancel = (event) => {
        // This event fires when ESC is pressed.
        // We call onCancel to ensure the parent state (controlling isOpen) is updated.
        onCancel();
    };

    if (dialogNode) {
        dialogNode.addEventListener('cancel', handleDialogCancel);
    }

    return () => {
        if (dialogNode) {
            dialogNode.removeEventListener('cancel', handleDialogCancel);
        }
    };
  }, [onCancel]);


  if (!isOpen) {
    return null; // Don't render if not open, though dialog.showModal() handles visibility
  }

  return (
    <dialog ref={dialogRef}>
      <article>
        <header>
          <h5>{title || 'Confirm Action'}</h5>
        </header>
        <p>{message || 'Are you sure?'}</p>
        <footer>
          <button className="secondary" onClick={onCancel} style={{ marginRight: '1rem' }}>
            Cancel
          </button>
          <button onClick={onConfirm}>
            Confirm
          </button>
        </footer>
      </article>
    </dialog>
  );
}

export default ConfirmModal;
