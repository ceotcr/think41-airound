import { create } from 'zustand';
import type { Message, ChatState } from '../types/chat';
import { v4 as uuidv4 } from 'uuid';

const useChatStore = create<ChatState>((set, get) => ({
    messages: [],
    currentConversation: null,
    isLoading: false,
    error: null,
    inputValue: '',
    conversations: [],

    actions: {
        sendMessage: async (content: string) => {
            const { currentConversation, messages } = get();

            try {
                set({ isLoading: true, error: null });

                // Create new conversation if none exists
                let conversation = currentConversation;
                if (!conversation) {
                    conversation = {
                        id: uuidv4(),
                        title: content.slice(0, 30),
                        createdAt: new Date(),
                        updatedAt: new Date(),
                    };
                    set({
                        currentConversation: conversation,
                        conversations: [...get().conversations, conversation]
                    });
                }

                // Add user message
                const userMessage: Message = {
                    id: uuidv4(),
                    content,
                    isFromUser: true,
                    timestamp: new Date(),
                };

                set({
                    messages: [...messages, userMessage],
                    inputValue: ''
                });

                // Simulate API call to get AI response
                const aiResponse: Message = {
                    id: uuidv4(),
                    content: `This is a response to: "${content}"`,
                    isFromUser: false,
                    timestamp: new Date(),
                };

                set({
                    messages: [...get().messages, aiResponse],
                    isLoading: false
                });

            } catch (err) {
                set({
                    error: 'Failed to send message',
                    isLoading: false
                });
            }
        },

        startNewConversation: () => {
            set({
                currentConversation: null,
                messages: [],
                inputValue: ''
            });
        },

        setInputValue: (value: string) => {
            set({ inputValue: value });
        },

        loadConversation: async (conversationId: string) => {
            try {
                set({ isLoading: true, error: null });

                // Simulate API call to fetch conversation
                const conversation = get().conversations.find(c => c.id === conversationId);
                if (conversation) {
                    // Simulate fetching messages for this conversation
                    const messages: Message[] = [
                        {
                            id: uuidv4(),
                            content: `Previous message in conversation ${conversationId}`,
                            isFromUser: true,
                            timestamp: new Date(Date.now() - 10000),
                        },
                        {
                            id: uuidv4(),
                            content: `Previous response in conversation ${conversationId}`,
                            isFromUser: false,
                            timestamp: new Date(Date.now() - 5000),
                        }
                    ];

                    set({
                        currentConversation: conversation,
                        messages,
                        isLoading: false
                    });
                }
            } catch (err) {
                set({
                    error: 'Failed to load conversation',
                    isLoading: false
                });
            }
        }
    }
}));

// Selector hooks for easier consumption
export const useMessages = () => useChatStore(state => state.messages);
export const useCurrentConversation = () => useChatStore(state => state.currentConversation);
export const useIsLoading = () => useChatStore(state => state.isLoading);
export const useError = () => useChatStore(state => state.error);
export const useInputValue = () => useChatStore(state => state.inputValue);
export const useConversations = () => useChatStore(state => state.conversations);
export const useChatActions = () => useChatStore(state => state.actions);