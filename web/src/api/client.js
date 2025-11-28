const BASE_URL = import.meta.env.VITE_API_URL || '';

export const apiClient = {
  // List all sessions
  async listSessions() {
    const response = await fetch(`${BASE_URL}/sessions/`, {
      headers: { 'Accept': 'application/json' }
    });
    console.log(response);
    return response.json();
  },

  // Create a new session
  async createSession() {
    const response = await fetch(`${BASE_URL}/sessions/`, {
      method: 'POST',
      headers: { 'Accept': 'application/json' }
    });
    return response.json();
  },

  // Get a specific session
  async getSession(sessionId) {
    const response = await fetch(`${BASE_URL}/sessions/${sessionId}`, {
      headers: { 'Accept': 'application/json' }
    });
    return response.json();
  },

  // Send message to agent
  async sendMessage(sessionId, messageText, files = []) {
    const parts = [];
    
    // Add text if provided
    if (messageText && messageText.trim()) {
      parts.push({ text: messageText });
    }
    
    // Add files as inlineData
    for (const file of files) {
      const base64Data = await fileToBase64(file);
      parts.push({
        inlineData: {
          data: base64Data,
          mimeType: file.type || 'application/octet-stream',
          displayName: file.name
        }
      });
    }
    
    const response = await fetch(`${BASE_URL}/sessions/${sessionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        new_message: {
          parts: parts,
          role: 'user'
        }
      })
    });
    return response.json();
  },

  // Send function response (for tool confirmations)
  async sendFunctionResponse(sessionId, functionCallId, functionName, confirmed) {
    const response = await fetch(`${BASE_URL}/sessions/${sessionId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        new_message: {
          parts: [
            {
              function_response: {
                id: functionCallId,
                name: functionName,
                response: {
                  confirmed: confirmed
                }
              }
            }
          ],
          role: 'user'
        }
      })
    });
    return response.json();
  },

  // Delete a session
  async deleteSession(sessionId) {
    const response = await fetch(`${BASE_URL}/sessions/${sessionId}`, {
      method: 'DELETE',
      headers: { 'Accept': 'application/json' }
    });
    return response.ok;
  }
};

// Helper function to convert file to base64
function fileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      // Remove data URL prefix (e.g., "data:image/png;base64,")
      const base64 = reader.result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

