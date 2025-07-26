export interface Message {
    id: string;
    content: string;
    isFromUser: boolean;
    timestamp: Date;
    metadata?: Record<string, unknown>;
}

export interface Conversation {
    id: string;
    title: string;
    createdAt: Date;
    updatedAt: Date;
}

export interface ChatState {
    messages: Message[];
    currentConversation: Conversation | null;
    isLoading: boolean;
    error: string | null;
    inputValue: string;
    conversations: Conversation[];
    actions: {
        sendMessage: (content: string) => Promise<void>;
        startNewConversation: () => void;
        setInputValue: (value: string) => void;
        loadConversation: (conversationId: string) => Promise<void>;
    };
}