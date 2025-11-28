import { useState, useEffect, useImperativeHandle, forwardRef } from 'react';
import { apiClient } from '../api/client';
import './SessionsPanel.css';

export const SessionsPanel = forwardRef(({ selectedSessionId, onSelectSession, onCreateSession }, ref) => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSessions();
    // Refresh sessions every 5 seconds to keep list updated
    const interval = setInterval(() => {
      loadSessions();
    }, 8000);
    return () => clearInterval(interval);
  }, []);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const data = await apiClient.listSessions();
      setSessions(data.sessions || []);
    } catch (error) {
      console.error('Failed to load sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  useImperativeHandle(ref, () => ({
    refresh: loadSessions
  }));

  const handleDelete = async (sessionId, e) => {
    e.stopPropagation();
    if (confirm('Delete this session?')) {
      await apiClient.deleteSession(sessionId);
      loadSessions();
      if (selectedSessionId === sessionId) {
        onSelectSession(null);
      }
    }
  };

  return (
    <div className="sessions-panel">
      <div className="sessions-header">
        <h2>Sessions</h2>
        <button onClick={onCreateSession} className="new-session-btn">
          + New Session
        </button>
      </div>
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <div className="sessions-list">
          {sessions.length === 0 ? (
            <div className="empty-sessions">
              <p>No sessions yet</p>
              <p className="empty-hint">Create a new session to get started</p>
            </div>
          ) : (
            sessions.map((session) => (
              <div
                key={session.id}
                className={`session-item ${selectedSessionId === session.id ? 'active' : ''}`}
                onClick={() => onSelectSession(session.id)}
              >
                <div className="session-info">
                  <div className="session-title">
                    {session.id.slice(0, 5)}...
                  </div>
                  <div className="session-meta">
                    {session.events?.length || 0} messages
                  </div>
                </div>
                <button
                  className="delete-btn"
                  onClick={(e) => handleDelete(session.id, e)}
                >
                  ×
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
});

