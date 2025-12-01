import './Message.css';

export function Message({ message, sessionId, onConfirmationResponse }) {
  const isUser = message.author === 'user';
  const isSystem = message.author === 'system';
  
  const renderFile = (file, index) => {
    if (file.data) {
      // Inline data - show preview if image
      if (file.mimeType?.startsWith('image/')) {
        return (
          <div key={index} className="message-file">
            <img
              src={`data:${file.mimeType};base64,${file.data}`}
              alt={file.name}
              className="file-preview-image"
            />
            <div className="file-name">{file.name}</div>
          </div>
        );
      }
    }
    
    // File URI or regular file
    return (
      <div key={index} className="message-file">
        <div className="file-icon">📄</div>
        <div className="file-info">
          <div className="file-name">{file.name}</div>
          {file.mimeType && (
            <div className="file-type">{file.mimeType}</div>
          )}
        </div>
        {file.uri && (
          <a href={file.uri} target="_blank" rel="noopener noreferrer" className="file-link">
            Open
          </a>
        )}
      </div>
    );
  };
  
  const handleConfirmation = async (confirmed) => {
    if (message.toolConfirmation && onConfirmationResponse) {
      await onConfirmationResponse(
        message.toolConfirmation.id,
        message.toolConfirmation.name,
        confirmed
      );
    }
  };

  // Don't render if no text, no files, and no pending confirmation
  const hasContent = (message.text && message.text.trim()) ||
                    (message.files && message.files.length > 0) ||
                    (message.toolConfirmation && !message.toolConfirmation.confirmed);
  
  if (!hasContent) {
    return null;
  }

  return (
    <div className={`message ${isUser ? 'user' : isSystem ? 'system' : 'assistant'}`}>
      <div className="message-author">{isUser ? 'You' : isSystem ? 'System' : 'Agent'}</div>
      {message.text && <div className="message-text">{message.text}</div>}
      {message.files && message.files.length > 0 && (
        <div className="message-files">
          {message.files.map((file, index) => renderFile(file, index))}
        </div>
      )}
      {message.toolConfirmation && !message.toolConfirmation.confirmed && (
        <div className="tool-confirmation">
          <div className="confirmation-hint">
            {message.toolConfirmation.hint || 'Please approve or reject this tool call.'}
          </div>
          {message.toolConfirmation.originalFunctionCall && (
            <div className="confirmation-details">
              <div className="confirmation-function">
                <strong>Function:</strong> {message.toolConfirmation.originalFunctionCall.name}()
              </div>
              {message.toolConfirmation.originalFunctionCall.args && (
                <div className="confirmation-args">
                  <strong>Arguments:</strong>
                    <pre>
                      {JSON.stringify(
                        Object.fromEntries(
                          Object.entries(message.toolConfirmation.originalFunctionCall.args)
                            .filter(([key]) => key !== 'body')
                        ),
                        null,
                        2
                      )}
                    </pre>
                </div>
              )}
            </div>
          )}
          <div className="confirmation-buttons">
            <button
              className="confirm-btn approve"
              onClick={() => handleConfirmation(true)}
              disabled={!onConfirmationResponse}
            >
              ✓ Approve
            </button>
            <button
              className="confirm-btn reject"
              onClick={() => handleConfirmation(false)}
              disabled={!onConfirmationResponse}
            >
              ✗ Reject
            </button>
          </div>
        </div>
      )}
      {message.timestamp && (
        <div className="message-time">
          {new Date(message.timestamp).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
}

