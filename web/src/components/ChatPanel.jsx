import { useState, useEffect, useRef } from 'react';
import { apiClient } from '../api/client';
import { Message } from './Message';
import './ChatPanel.css';

export function ChatPanel({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    if (sessionId) {
      loadSession();
    } else {
      setMessages([]);
    }
  }, [sessionId]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadSession = async () => {
    try {
      setLoading(true);
      const session = await apiClient.getSession(sessionId);
      // Extract messages from events
      const extractedMessages = extractMessages(session.events || []);
      setMessages(extractedMessages);
    } catch (error) {
      console.error('Failed to load session:', error);
    } finally {
      setLoading(false);
    }
  };

  const extractMessages = (events) => {
    return events
      .filter(event => event.content?.parts || event.parts)
      .map(event => {
        const parts = event.content?.parts || event.parts || [];
        const text = parts
          .map(part => part.text)
          .filter(Boolean)
          .join('\n');
        
        // Extract files from parts
        const files = parts
          .filter(part => part.fileData || part.inlineData)
          .map(part => ({
            name: part.fileData?.displayName || part.inlineData?.displayName || 'file',
            uri: part.fileData?.fileUri,
            mimeType: part.fileData?.mimeType || part.inlineData?.mimeType,
            data: part.inlineData?.data
          }));
        
        // Check for function call with tool confirmation
        const functionCall = parts.find(part => part.functionCall);
        let toolConfirmation = null;
        if (functionCall?.functionCall) {
          const fc = functionCall.functionCall;
          if (fc.args?.toolConfirmation) {
            toolConfirmation = {
              id: fc.id,
              name: fc.name,
              hint: fc.args.toolConfirmation.hint,
              originalFunctionCall: fc.args.originalFunctionCall,
              confirmed: fc.args.toolConfirmation.confirmed
            };
          }
        }
        
        return {
          id: event.id || Math.random().toString(),
          author: event.author || 'assistant',
          text: text,
          files: files.length > 0 ? files : undefined,
          toolConfirmation: toolConfirmation,
          timestamp: event.timestamp
        };
      })
      .filter(message => {
        // Only show messages with text, files, or pending tool confirmation
        return (message.text && message.text.trim()) || 
               (message.files && message.files.length > 0) ||
               (message.toolConfirmation && !message.toolConfirmation.confirmed);
      });
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(prev => [...prev, ...files]);
    // Reset input so same file can be selected again
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleConfirmationResponse = async (functionCallId, functionName, confirmed) => {
    if (!sessionId || sending) return;
    
    // Add user message showing "Approve" or "Reject"
    const confirmationText = confirmed ? 'Approve' : 'Reject';
    const userMessage = {
      id: Date.now().toString(),
      author: 'user',
      text: confirmationText,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, userMessage]);
    
    setSending(true);
    
    try {
      // Only send the function response (not the text message)
      await apiClient.sendFunctionResponse(
        sessionId,
        functionCallId,
        functionName,
        confirmed
      );
      
      // Reload session to get updated messages
      await loadSession();
    } catch (error) {
      console.error('Failed to send confirmation:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString() + '_error',
        author: 'system',
        text: 'Failed to send confirmation. Please try again.',
        timestamp: Date.now()
      }]);
    } finally {
      setSending(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if ((!inputText.trim() && selectedFiles.length === 0) || !sessionId || sending) return;

    const userMessage = {
      id: Date.now().toString(),
      author: 'user',
      text: inputText || undefined,
      files: selectedFiles.map(f => ({ name: f.name, type: f.type })),
      timestamp: Date.now()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageToSend = inputText;
    const filesToSend = [...selectedFiles];
    setInputText('');
    setSelectedFiles([]);
    setSending(true);

    try {
      const response = await apiClient.sendMessage(sessionId, messageToSend, filesToSend);
      
      // Extract response message
      if (response.parts) {
        const text = response.parts
          .map(part => part.text)
          .filter(Boolean)
          .join('\n');
        
        const files = response.parts
          .filter(part => part.fileData || part.inlineData)
          .map(part => ({
            name: part.fileData?.displayName || part.inlineData?.displayName || 'file',
            uri: part.fileData?.fileUri,
            mimeType: part.fileData?.mimeType || part.inlineData?.mimeType,
            data: part.inlineData?.data
          }));
        
        // Check for function call with tool confirmation
        const functionCall = response.parts.find(part => part.functionCall);
        let toolConfirmation = null;
        if (functionCall?.functionCall) {
          const fc = functionCall.functionCall;
          if (fc.args?.toolConfirmation) {
            toolConfirmation = {
              id: fc.id,
              name: fc.name,
              hint: fc.args.toolConfirmation.hint,
              originalFunctionCall: fc.args.originalFunctionCall,
              confirmed: fc.args.toolConfirmation.confirmed
            };
          }
        }
        
        // Only add message if it has text, files, or pending tool confirmation
        const hasContent = (text && text.trim()) || 
                          (files.length > 0) ||
                          (toolConfirmation && !toolConfirmation.confirmed);
        
        if (hasContent) {
          const assistantMessage = {
            id: Date.now().toString() + '_response',
            author: 'assistant',
            text: text || undefined,
            files: files.length > 0 ? files : undefined,
            toolConfirmation: toolConfirmation,
            timestamp: Date.now()
          };
          
          setMessages(prev => [...prev, assistantMessage]);
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString() + '_error',
        author: 'system',
        text: 'Failed to send message. Please try again.',
        timestamp: Date.now()
      }]);
    } finally {
      setSending(false);
    }
  };

  if (!sessionId) {
    return (
      <div className="chat-panel empty">
        <div className="empty-state">
          <p>Select a session from the left panel to start chatting</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-panel">
      <div className="chat-messages">
        {loading ? (
          <div className="loading">Loading messages...</div>
        ) : (
          <>
            {messages.length === 0 ? (
              <div className="empty-chat">
                <p>No messages yet. Start the conversation!</p>
              </div>
            ) : (
              messages.map((message) => (
                <Message
                  key={message.id}
                  message={message}
                  sessionId={sessionId}
                  onConfirmationResponse={handleConfirmationResponse}
                />
              ))
            )}
            {sending && (
              <div className="typing-indicator">
                <div className="message assistant">
                  <div className="message-author">Agent</div>
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
      <form className="chat-input-form" onSubmit={handleSend}>
        {selectedFiles.length > 0 && (
          <div className="selected-files">
            {selectedFiles.map((file, index) => (
              <div key={index} className="file-tag">
                <span className="file-name">{file.name}</span>
                <button
                  type="button"
                  className="file-remove"
                  onClick={() => removeFile(index)}
                  disabled={sending}
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        )}
        <div className="input-row">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            className="file-input"
            multiple
            disabled={sending}
            style={{ display: 'none' }}
          />
          <button
            type="button"
            className="file-button"
            onClick={() => fileInputRef.current?.click()}
            disabled={sending}
            title="Attach file"
          >
            📎
          </button>
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Type your message..."
            disabled={sending}
            className="text-input"
          />
          <button
            type="submit"
            disabled={sending || (!inputText.trim() && selectedFiles.length === 0)}
          >
            {sending ? 'Sending...' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}

