import React, { useState } from 'react';
import { useChatActions, useInputValue } from '../stores/chat';

const UserInput: React.FC = () => {
    const inputValue = useInputValue();
    const { sendMessage, setInputValue } = useChatActions();
    const [isComposing, setIsComposing] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (inputValue.trim()) {
            sendMessage(inputValue);
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            className="flex items-center gap-2 p-2 bg-white rounded-lg shadow-sm border border-gray-200 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all"
        >
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onCompositionStart={() => setIsComposing(true)}
                onCompositionEnd={() => setIsComposing(false)}
                onKeyDown={(e) => {
                    if (e.key === 'Enter' && !isComposing && !e.shiftKey) {
                        handleSubmit(e);
                    }
                }}
                placeholder="Type your message..."
                className="flex-1 px-4 py-2 outline-none text-gray-700 placeholder-gray-400 bg-transparent"
            />
            <button
                type="submit"
                disabled={!inputValue.trim()}
                className={`p-2 rounded-full ${inputValue.trim()
                    ? 'bg-blue-500 text-white hover:bg-blue-600 cursor-pointer'
                    : 'bg-gray-200 text-gray-400 cursor-not-allowed'} transition-colors`}
            >
                Send
            </button>
        </form>
    );
};

export default UserInput;