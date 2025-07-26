import React from 'react';
import { useCurrentConversation, useIsLoading } from '../stores/chat';
import MessageList from './MessageList';
import UserInput from './UserInput';

const ChatWindow: React.FC = () => {
    const currentConversation = useCurrentConversation();
    const isLoading = useIsLoading();

    return (
        <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-lg overflow-hidden">
            <header className="bg-white px-6 py-4 border-b border-gray-200">
                <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold text-gray-800">
                        {currentConversation?.title || 'New Chat'}
                    </h2>
                    {isLoading && (
                        <div className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
                            <span className="text-sm text-gray-500">Thinking...</span>
                        </div>
                    )}
                </div>
            </header>

            <div className="flex-1 overflow-y-auto p-4">
                <MessageList />
            </div>

            <div className="bg-white px-4 py-3 border-t border-gray-200">
                <UserInput />
            </div>
        </div>
    );
};

export default ChatWindow;