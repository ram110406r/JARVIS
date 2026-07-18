import { useState, useCallback, useRef, useEffect } from 'react';
import { useChatStore, useAppStore } from '../store/store';
import { sendChatMessage, getContext, checkHealth } from '../services/api';

export function useChat() {
  const { messages, addMessage, setLoading, setError, isLoading } = useChatStore();

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      // Add user message
      const userMessage = {
        id: Date.now().toString(),
        role: 'user' as const,
        content,
        timestamp: new Date(),
      };
      addMessage(userMessage);

      setLoading(true);
      setError(null);

      try {
        // Get current context
        const context = await getContext();

        // Send to backend
        const response = await sendChatMessage(content, context);

        // Add assistant message
        const assistantMessage = {
          id: (Date.now() + 1).toString(),
          role: 'assistant' as const,
          content: response.response || 'No response received',
          timestamp: new Date(),
          toolUsed: response.tool_used,
        };
        addMessage(assistantMessage);
      } catch (error) {
        setError(error instanceof Error ? error.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    },
    [addMessage, setLoading, setError]
  );

  return {
    messages,
    isLoading,
    sendMessage,
  };
}

export function useVoice() {
  const { setRecording, setTranscribedText } = useAppStore();
  const { addMessage, setLoading } = useChatStore();
  const [isSupported, setIsSupported] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Check browser support
    const isSupported =
      navigator.mediaDevices &&
      navigator.mediaDevices.getUserMedia;
    setIsSupported(!!isSupported);

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Open WebSocket connection
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//127.0.0.1:8000/api/voice`;
      const socket = new WebSocket(wsUrl);
      socket.binaryType = 'arraybuffer';
      socketRef.current = socket;
      
      setTranscribedText('Listening...');
      setLoading(true);

      socket.onopen = () => {
        console.log('🎤 Voice WebSocket connected');
      };

      socket.onmessage = async (event) => {
        if (typeof event.data === 'string') {
          try {
            const data = JSON.parse(event.data);
            if (data.type === 'transcription') {
              setTranscribedText(data.text);
              
              // Add user message
              addMessage({
                id: Date.now().toString(),
                role: 'user',
                content: data.text,
                timestamp: new Date()
              });
            } else if (data.type === 'response') {
              // Add assistant message
              addMessage({
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: data.text,
                timestamp: new Date()
              });
            }
          } catch (e) {
            console.error('Error parsing voice socket text:', e);
          }
        } else {
          // Binary message (audio bytes)
          try {
            const audioBlob = new Blob([event.data], { type: 'audio/wav' });
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play().catch(err => console.error('Audio play error:', err));
            setLoading(false);
          } catch (e) {
            console.error('Error handling voice socket binary:', e);
            setLoading(false);
          }
        }
      };

      socket.onerror = (err) => {
        console.error('Voice socket error:', err);
        setLoading(false);
      };

      socket.onclose = () => {
        console.log('🎤 Voice WebSocket closed');
      };

      const recorder = new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;

      const audioChunks: Blob[] = [];
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        console.log('Recording stopped, sending to voice socket...', audioBlob);
        
        if (socket.readyState === WebSocket.OPEN) {
          const buffer = await audioBlob.arrayBuffer();
          socket.send(buffer);
        } else {
          socket.onopen = async () => {
            const buffer = await audioBlob.arrayBuffer();
            socket.send(buffer);
          };
        }
      };

      recorder.start();
      setRecording(true);
    } catch (error) {
      console.error('Microphone access denied:', error);
      setLoading(false);
    }
  }, [setRecording, setTranscribedText, addMessage, setLoading]);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
      setRecording(false);
    }
  }, [setRecording]);

  return {
    isSupported,
    startRecording,
    stopRecording,
  };
}

export function useBackendStatus() {
  const { backendConnected, setBackendConnected } = useAppStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        const health = await checkHealth();
        setBackendConnected(!!health);
      } catch {
        setBackendConnected(false);
      } finally {
        setLoading(false);
      }
    };

    checkConnection();

    // Check every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, [setBackendConnected]);

  return {
    backendConnected,
    loading,
  };
}

export function useDesktopContext() {
  const { desktopContext, setDesktopContext } = useAppStore();
  const [loading, setLoading] = useState(false);

  const fetchContext = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getContext();
      setDesktopContext(data);
    } catch (error) {
      console.error('Failed to fetch context:', error);
    } finally {
      setLoading(false);
    }
  }, [setDesktopContext]);

  useEffect(() => {
    fetchContext();
    // Poll context every 5 seconds
    const interval = setInterval(fetchContext, 5000);
    return () => clearInterval(interval);
  }, [fetchContext]);

  return {
    context: desktopContext,
    loading,
    refresh: fetchContext,
  };
}
