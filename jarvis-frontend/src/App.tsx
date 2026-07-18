import React, { useEffect } from 'react';
import { ChatWindow } from './components/ChatWindow';
import { VoiceControl } from './components/VoiceControl';
import { StatusBar } from './components/StatusBar';
import { ContextDisplay } from './components/ContextDisplay';
import { ScreenshotControl } from './components/ScreenshotControl';
import './App.css';

function App() {
  useEffect(() => {
    // Set up global keyboard shortcuts
    const handleKeyDown = (e: KeyboardEvent) => {
      // Space bar for push-to-talk (can be extended later)
      if (e.code === 'Space' && e.target === document.body) {
        e.preventDefault();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🤖 JARVIS Phase 1</h1>
        <p>AI Desktop Companion</p>
      </header>

      <div className="app-container">
        <main className="app-main">
          <ChatWindow />
        </main>

        <aside className="app-sidebar">
          <VoiceControl />
          <ContextDisplay />
          <ScreenshotControl />
        </aside>
      </div>

      <footer className="app-footer">
        <StatusBar />
      </footer>
    </div>
  );
}

export default App;
