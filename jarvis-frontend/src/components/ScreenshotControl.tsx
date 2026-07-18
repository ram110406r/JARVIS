import React, { useState } from 'react';
import { Camera, Image as ImageIcon, Eye, Loader2 } from 'lucide-react';
import { captureScreenshot } from '../services/api';
import { useChatStore } from '../store/store';
import '../styles/ScreenshotControl.css';

export function ScreenshotControl() {
  const [loading, setLoading] = useState(false);
  const [analyze, setAnalyze] = useState(true);
  const [screenshotPath, setScreenshotPath] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<string | null>(null);
  
  const { addMessage } = useChatStore();

  const handleCapture = async () => {
    setLoading(true);
    setAnalysisResult(null);
    try {
      const response = await captureScreenshot(analyze);
      if (response && response.success) {
        // Build direct URL to screenshot. Add cache breaker timestamp.
        const imageUrl = `http://127.0.0.1:8000${response.path}?t=${Date.now()}`;
        setScreenshotPath(imageUrl);
        setAnalysisResult(response.analysis);

        // Add user notification message in chat
        addMessage({
          id: Date.now().toString(),
          role: 'system',
          content: `📸 Screenshot captured. ${analyze ? 'Analyzing contents...' : ''}`,
          timestamp: new Date(),
        });

        if (analyze && response.analysis) {
          addMessage({
            id: (Date.now() + 1).toString(),
            role: 'assistant',
            content: `👁️ Screenshot analysis results:\n${response.analysis}`,
            timestamp: new Date(),
          });
        }
      } else {
        console.error('Screenshot capture response unsuccessful:', response);
      }
    } catch (error) {
      console.error('Failed to capture screenshot:', error);
      addMessage({
        id: Date.now().toString(),
        role: 'system',
        content: `❌ Screenshot capture failed. Ensure the backend is running.`,
        timestamp: new Date(),
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="screenshot-card">
      <div className="screenshot-header">
        <h3>
          <Camera size={16} className="header-icon" /> Screen Capture
        </h3>
      </div>

      <div className="screenshot-body">
        <button
          onClick={handleCapture}
          disabled={loading}
          className="capture-button"
        >
          {loading ? (
            <>
              <Loader2 size={16} className="spinner" />
              <span>Capturing...</span>
            </>
          ) : (
            <>
              <Camera size={16} />
              <span>Capture Screen</span>
            </>
          )}
        </button>

        <label className="analyze-toggle">
          <input
            type="checkbox"
            checked={analyze}
            onChange={(e) => setAnalyze(e.target.checked)}
            disabled={loading}
          />
          <span className="toggle-label">Analyze with Vision/OCR</span>
        </label>

        {screenshotPath && (
          <div className="screenshot-preview-container">
            <div className="preview-label">
              <ImageIcon size={12} style={{ marginRight: 4 }} /> Captured Image
            </div>
            <div className="image-wrapper">
              <img
                src={screenshotPath}
                alt="Latest screenshot"
                className="screenshot-img"
                onClick={() => window.open(screenshotPath, '_blank')}
              />
              <div className="zoom-overlay">
                <Eye size={16} />
                <span>View Fullscreen</span>
              </div>
            </div>
          </div>
        )}

        {analysisResult && (
          <div className="ocr-result-container">
            <div className="preview-label">OCR / Vision Output</div>
            <div className="ocr-text">{analysisResult}</div>
          </div>
        )}
      </div>
    </div>
  );
}
