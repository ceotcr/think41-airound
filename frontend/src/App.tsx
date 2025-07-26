import React from 'react';
import ChatWindow from './components/ChatWindow';
import { useChatActions } from './stores/chat';

const App: React.FC = () => {
  const { startNewConversation } = useChatActions();

  return (
    <div className="app">
      <aside className="sidebar">
        <button onClick={startNewConversation}>New Chat</button>
      </aside>
      <main className="main-content">
        <ChatWindow />
      </main>
    </div>
  );
};

export default App;