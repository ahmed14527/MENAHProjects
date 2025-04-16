import React, { useState } from 'react';
import { sendMessage } from '../api';

const MessageForm = () => {
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = { content };

    try {
      await sendMessage(data);
      alert('Message sent');
    } catch (err) {
      alert('Failed to send message');
    }
  };

  return (
    <div>
      <h2>Send Message</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Message</label>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
        </div>
        <div>
          <button type="submit">Send</button>
        </div>
      </form>
    </div>
  );
};

export default MessageForm;
