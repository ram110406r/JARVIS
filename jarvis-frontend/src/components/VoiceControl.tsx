import React, { useState } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { useVoice } from '../hooks/useChat';
import { useAppStore } from '../store/store';
import '../styles/VoiceControl.css';

export function VoiceControl() {
  const { isSupported, startRecording, stopRecording } = useVoice();
  const { isRecording, transcribedText } = useAppStore();
  const [tooltipVisible, setTooltipVisible] = useState(false);

  if (!isSupported) {
    return (
      <div className="voice-control disabled">
        <div className="voice-badge">🎤 Not supported</div>
      </div>
    );
  }

  const handleToggle = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  return (
    <div className="voice-control">
      <button
        onClick={handleToggle}
        className={`voice-button ${isRecording ? 'recording' : ''}`}
        onMouseEnter={() => setTooltipVisible(true)}
        onMouseLeave={() => setTooltipVisible(false)}
        title={isRecording ? 'Stop recording (Space)' : 'Start recording (Space)'}
      >
        {isRecording ? <MicOff size={24} /> : <Mic size={24} />}
      </button>

      {tooltipVisible && (
        <div className="voice-tooltip">
          {isRecording ? 'Recording...' : 'Push to talk'}
        </div>
      )}

      {transcribedText && (
        <div className="transcription">
          <div className="transcription-label">Transcription:</div>
          <div className="transcription-text">{transcribedText}</div>
        </div>
      )}

      {isRecording && <div className="recording-indicator">🔴 Recording</div>}
    </div>
  );
}
