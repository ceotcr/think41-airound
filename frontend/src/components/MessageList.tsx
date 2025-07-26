import React from 'react';
import Message from './Message';
import { useMessages } from '../stores/chat';

const MessageList: React.FC = () => {
    const messages = useMessages();

    return (
        <div className="flex flex-col space-y-4 p-4 overflow-y-auto h-full">
            {messages.map((message) => (
                <Message key={message.id} message={message} />
            ))}

            {/* Empty state */}
            {messages.length === 0 && (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                    <div className="text-lg mb-2">No messages yet</div>
                    <div className="text-sm">Start a conversation</div>
                </div>
            )}
        </div>
    );
};

export default MessageList;