import React from 'react';
import { Monitor, Clipboard, Eye, RefreshCw } from 'lucide-react';
import { useDesktopContext } from '../hooks/useChat';
import '../styles/ContextDisplay.css';

export function ContextDisplay() {
  const { context, loading, refresh } = useDesktopContext();

  const activeWindow = context?.active_window || 'None';
  const clipboard = context?.clipboard || 'Empty';
  const cursorPosition = context?.cursor_position
    ? `X: ${context.cursor_position[0]}, Y: ${context.cursor_position[1]}`
    : 'Unknown';
  const timestamp = context?.timestamp
    ? new Date(context.timestamp).toLocaleTimeString()
    : 'Never';

  return (
    <div className="context-display-card">
      <div className="context-display-header">
        <h3>
          <Monitor size={16} className="header-icon" /> Desktop Context
        </h3>
        <button
          onClick={refresh}
          disabled={loading}
          className={`refresh-btn ${loading ? 'loading' : ''}`}
          title="Refresh Context"
        >
          <RefreshCw size={14} />
        </button>
      </div>

      <div className="context-display-body">
        <div className="context-detail-item">
          <div className="detail-label">Active Window</div>
          <div className="detail-value active-window-text" title={activeWindow}>
            {activeWindow}
          </div>
        </div>

        <div className="context-detail-item">
          <div className="detail-label">
            <Eye size={12} style={{ marginRight: 4 }} /> Cursor Location
          </div>
          <div className="detail-value cursor-text">{cursorPosition}</div>
        </div>

        <div className="context-detail-item">
          <div className="detail-label">
            <Clipboard size={12} style={{ marginRight: 4 }} /> Clipboard Preview
          </div>
          <div className="detail-value clipboard-box" title={clipboard}>
            {clipboard.length > 80 ? `${clipboard.substring(0, 80)}...` : clipboard}
          </div>
        </div>
      </div>

      <div className="context-display-footer">
        <span>Updated: {timestamp}</span>
      </div>
    </div>
  );
}
