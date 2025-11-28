import { useState, useRef } from 'react';
import { SessionsPanel } from './components/SessionsPanel';
import { ChatPanel } from './components/ChatPanel';
import { apiClient } from './api/client';
import './styles/App.css';

function App() {
  const [selectedSessionId, setSelectedSessionId] = useState(null);
  const sessionsPanelRef = useRef(null);

  const handleCreateSession = async () => {
    try {
      const newSession = await apiClient.createSession();
      setSelectedSessionId(newSession.id);
      // Refresh the sessions list
      if (sessionsPanelRef.current) {
        sessionsPanelRef.current.refresh();
      }
    } catch (error) {
      console.error('Failed to create session:', error);
      alert('Failed to create session. Please try again.');
    }
  };

  return (
    <div className="app">
      <SessionsPanel
        ref={sessionsPanelRef}
        selectedSessionId={selectedSessionId}
        onSelectSession={setSelectedSessionId}
        onCreateSession={handleCreateSession}
      />
      <ChatPanel sessionId={selectedSessionId} />
    </div>
  );
}

export default App;

