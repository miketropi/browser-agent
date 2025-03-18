import { useState } from 'react';

const MessageBox = ({ onSend, placeholder = "Type your message here...", disabled = false }) => {
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setMessage(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage('');
    }
  };

  const handleKeyDown = (e) => {
    // Submit on Ctrl+Enter or Cmd+Enter
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="w-full bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <form onSubmit={handleSubmit} className="flex flex-col">
        <textarea
          value={message}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          rows={3}
          className="w-full p-3 text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-t-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          aria-label="Message input"
        />
        <div className="flex justify-between items-center p-2 bg-gray-50 dark:bg-gray-900 rounded-b-lg">
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Press Ctrl+Enter to send
          </div>
          <button
            type="submit"
            disabled={!message.trim() || disabled}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors ${
              !message.trim() || disabled
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
            }`}
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};

export default MessageBox;
