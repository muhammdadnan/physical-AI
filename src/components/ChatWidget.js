import React, { useState, useRef, useEffect } from 'react';
import styles from './ChatWidget.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI assistant for Physical AI & Humanoid Robotics. How can I help you today?", sender: 'bot', timestamp: new Date() }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputValue.trim() === '') return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    // Simulate bot response after delay
    setTimeout(() => {
      const botResponse = {
        id: messages.length + 2,
        text: getBotResponse(inputValue),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000);
  };

  const getBotResponse = (userInput) => {
    const input = userInput.toLowerCase();

    if (input.includes('hello') || input.includes('hi') || input.includes('hey')) {
      return "Hello there! How can I assist you with Physical AI and Humanoid Robotics today?";
    } else if (input.includes('module') || input.includes('course')) {
      return "We have 4 comprehensive modules: Module 1 covers ROS 2 fundamentals, Module 2 covers Digital Twin technologies, Module 3 covers AI-Robot Brain with NVIDIA Isaac, and Module 4 covers Vision-Language-Action systems. Which module interests you?";
    } else if (input.includes('ros') || input.includes('ros2')) {
      return "ROS 2 (Robot Operating System 2) is covered in Module 1. It's the foundation for robotic applications, covering nodes, topics, services, and actions. You'll learn how to build complex and robust robot behavior across various platforms.";
    } else if (input.includes('isaac') || input.includes('nvidia')) {
      return "NVIDIA Isaac is covered in Module 3. It includes Isaac Sim for photorealistic simulation, Isaac ROS for perception and navigation, and VSLAM for visual SLAM. These technologies are essential for advanced humanoid robot AI systems.";
    } else if (input.includes('nav2') || input.includes('navigation')) {
      return "Nav2 is the navigation framework for ROS 2, covered in Module 3. It provides flexible architecture for humanoid robot navigation with global and local planners, recovery behaviors, and plugin-based design.";
    } else if (input.includes('vslam') || input.includes('slam')) {
      return "Visual SLAM (VSLAM) is covered in Module 3. It allows robots to build maps of unknown environments using visual sensors while simultaneously localizing themselves. Isaac ROS provides optimized VSLAM packages with GPU acceleration.";
    } else if (input.includes('project') || input.includes('exercise')) {
      return "Each module includes hands-on mini-projects to reinforce your learning. Module 1 has a ROS 2 controller project, Module 2 has a digital twin simulation project, Module 3 has a complete AI brain implementation, and Module 4 has VLA system projects.";
    } else if (input.includes('thank') || input.includes('thanks')) {
      return "You're welcome! Feel free to ask more questions about Physical AI and Humanoid Robotics.";
    } else {
      return "I'm here to help with questions about Physical AI & Humanoid Robotics. You can ask me about any of the 4 modules, ROS 2, Isaac Sim, VSLAM, Nav2, or any other topic related to the course content.";
    }
  };

  return (
    <div className={styles.chatContainer}>
      {isOpen ? (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div className={styles.headerInfo}>
              <div className={styles.botAvatar}>🤖</div>
              <div>
                <h4>AI Assistant</h4>
                <p>Physical AI & Humanoid Robotics</p>
              </div>
            </div>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${styles[message.sender]}`}
              >
                {message.sender === 'bot' && (
                  <div className={styles.botAvatarSmall}>🤖</div>
                )}
                <div className={styles.messageContent}>
                  {message.text}
                </div>
                {message.sender === 'user' && (
                  <div className={styles.userAvatar}>👤</div>
                )}
              </div>
            ))}
            {isTyping && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.botAvatarSmall}>🤖</div>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className={styles.chatInputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder="Type your question about Physical AI & Robotics..."
              className={styles.chatInput}
            />
            <button type="submit" className={styles.sendButton} disabled={inputValue.trim() === ''}>
              ➤
            </button>
          </form>
        </div>
      ) : (
        <button
          className={styles.chatButton}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          💬
        </button>
      )}
    </div>
  );
};

export default ChatWidget;