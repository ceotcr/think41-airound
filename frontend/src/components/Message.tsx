import React from 'react';
import type { Message as MessageType } from '../types/chat';

interface MessageProps {
    message: MessageType;
}

const Message: React.FC<MessageProps> = ({ message }) => {
    return (
        <div className={`flex mb-4 ${message.isFromUser ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs md:max-w-md lg:max-w-lg rounded-lg px-4 py-2 ${message.isFromUser
                ? 'bg-blue-500 text-white rounded-br-none'
                : 'bg-gray-200 text-gray-800 rounded-bl-none'}`}
            >
                <div className="text-sm">{message.content}</div>
                <div className={`text-xs mt-1 text-right ${message.isFromUser
                    ? 'text-blue-100'
                    : 'text-gray-500'}`}
                >
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </div>
    );
};

export default Message;