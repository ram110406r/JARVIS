/**
 * API Service for JARVIS Backend Communication
 */

import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

// Create axios instance with base config
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const endpoints = {
  health: '/health',
  config: '/config',
  chat: '/api/chat',
  screenshot: '/api/screenshot',
  context: '/api/context',
  tools: {
    browser: '/api/tools/browser',
    filesystem: '/api/tools/filesystem',
    terminal: '/api/tools/terminal',
  },
  voice: '/api/voice', // WebSocket endpoint
};

// Health check
export async function checkHealth() {
  try {
    const response = await api.get(endpoints.health);
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return null;
  }
}

// Get backend config
export async function getConfig() {
  try {
    const response = await api.get(endpoints.config);
    return response.data;
  } catch (error) {
    console.error('Config fetch failed:', error);
    return null;
  }
}

// Send chat message
export async function sendChatMessage(message: string, context?: Record<string, any>) {
  try {
    const response = await api.post(endpoints.chat, {
      message,
      context: context || {},
    });
    return response.data;
  } catch (error) {
    console.error('Chat request failed:', error);
    throw error;
  }
}

// Capture screenshot
export async function captureScreenshot(analyze = false) {
  try {
    const response = await api.post(endpoints.screenshot, {
      analyze,
    });
    return response.data;
  } catch (error) {
    console.error('Screenshot capture failed:', error);
    throw error;
  }
}

// Get desktop context
export async function getContext() {
  try {
    const response = await api.get(endpoints.context);
    return response.data;
  } catch (error) {
    console.error('Context fetch failed:', error);
    return null;
  }
}

// WebSocket for voice
export function createVoiceWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const ws = new WebSocket(`${protocol}//127.0.0.1:8000${endpoints.voice}`);
  return ws;
}

// Browser search
export async function browserSearch(query: string) {
  try {
    const response = await api.post(endpoints.tools.browser, null, {
      params: { query },
    });
    return response.data;
  } catch (error) {
    console.error('Browser search failed:', error);
    throw error;
  }
}

// Filesystem operation
export async function filesystemOperation(
  operation: string,
  path?: string,
  content?: string
) {
  try {
    const response = await api.post(endpoints.tools.filesystem, {
      operation,
      path,
      content,
    });
    return response.data;
  } catch (error) {
    console.error('Filesystem operation failed:', error);
    throw error;
  }
}

// Terminal operation
export async function terminalOperation(command: string, validateOnly = true) {
  try {
    const response = await api.post(endpoints.tools.terminal, {
      command,
      validate_only: validateOnly,
    });
    return response.data;
  } catch (error) {
    console.error('Terminal operation failed:', error);
    throw error;
  }
}
