import { create } from 'zustand';

export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  toolUsed?: string;
}

export interface ChatStore {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  addMessage: (message: Message) => void;
  addMessages: (messages: Message[]) => void;
  clearMessages: () => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useChatStore = create<ChatStore>((set) => ({
  messages: [
    {
      id: '0',
      role: 'system',
      content: '🤖 JARVIS online. How can I assist you today?',
      timestamp: new Date(),
    },
  ],
  isLoading: false,
  error: null,

  addMessage: (message: Message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),

  addMessages: (messages: Message[]) =>
    set((state) => ({
      messages: [...state.messages, ...messages],
    })),

  clearMessages: () =>
    set({
      messages: [
        {
          id: '0',
          role: 'system',
          content: '🤖 JARVIS online. How can I assist you today?',
          timestamp: new Date(),
        },
      ],
    }),

  setLoading: (loading: boolean) => set({ isLoading: loading }),

  setError: (error: string | null) => set({ error }),
}));

// Voice/Context store
export interface AppStore {
  backendConnected: boolean;
  isRecording: boolean;
  transcribedText: string;
  desktopContext: any;
  setBackendConnected: (connected: boolean) => void;
  setRecording: (recording: boolean) => void;
  setTranscribedText: (text: string) => void;
  setDesktopContext: (context: any) => void;
}

export const useAppStore = create<AppStore>((set) => ({
  backendConnected: false,
  isRecording: false,
  transcribedText: '',
  desktopContext: null,

  setBackendConnected: (connected: boolean) => set({ backendConnected: connected }),
  setRecording: (recording: boolean) => set({ isRecording: recording }),
  setTranscribedText: (text: string) => set({ transcribedText: text }),
  setDesktopContext: (context: any) => set({ desktopContext: context }),
}));
