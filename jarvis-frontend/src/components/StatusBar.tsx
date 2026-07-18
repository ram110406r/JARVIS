import React from 'react';
import { Activity, AlertCircle } from 'lucide-react';
import { useBackendStatus } from '../hooks/useChat';
import '../styles/StatusBar.css';

export function StatusBar() {
  const { backendConnected, loading } = useBackendStatus();

  if (loading) {
    return (
      <div className="status-bar">
        <div className="status-item">
          <div className="status-indicator loading"></div>
          <span>Connecting...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="status-bar">
      <div className="status-item">
        <div className={`status-indicator ${backendConnected ? 'connected' : 'disconnected'}`}>
          {backendConnected ? <Activity size={16} /> : <AlertCircle size={16} />}
        </div>
        <span>{backendConnected ? 'Backend Connected' : 'Backend Offline'}</span>
      </div>

      <div className="status-item">
        <span className="model-info">Model: llama2</span>
      </div>

      <div className="status-item">
        <span className="phase-info">Phase 1 MVP</span>
      </div>
    </div>
  );
}
