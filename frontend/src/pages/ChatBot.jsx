import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { MessageSquare, Send, Trash2, HelpCircle, User, Bot, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

export const ChatBot = () => {
  const { t, language } = useLanguage();
  const { token } = useAuth();
  
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  
  const chatEndRef = useRef(null);

  // Suggested queries list
  const samplePrompts = [
    "What is the best time to visit Taj Mahal?",
    "Suggest some budget travel tips for India.",
    "Which is the safest tourist place for solo travel?",
    "What are the best hill stations in Himachal Pradesh?"
  ];

  // Fetch chat history on load (only if logged in)
  useEffect(() => {
    const fetchChatHistory = async () => {
      if (!token) return;
      try {
        setLoadingHistory(true);
        const response = await axios.get('/api/chat/history');
        setMessages(response.data);
      } catch (err) {
        console.error('Error fetching chat history:', err);
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchChatHistory();
  }, [token]);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e, customText = null) => {
    if (e) e.preventDefault();
    
    const textToSend = customText || input;
    if (!textToSend.trim()) return;
    if (sending) return;

    if (!token) {
      // Local demo response if not logged in
      const tempUserMsg = { id: Date.now(), sender: 'user', message: textToSend, created_at: new Date() };
      const tempAiMsg = { 
        id: Date.now() + 1, 
        sender: 'ai', 
        message: "Hello! I am TourEase AI assistant. To enable fully saved chat logs and full AI features, please sign in or register an account. Locally: Baga Beach is in Goa, Munnar is in Kerala, Taj Mahal is in Agra, Uttar Pradesh.", 
        created_at: new Date() 
      };
      setMessages(prev => [...prev, tempUserMsg, tempAiMsg]);
      setInput('');
      return;
    }

    try {
      setSending(true);
      setInput('');

      // Add temporary user message to UI for visual speed
      const tempUserMsg = { id: Date.now(), sender: 'user', message: textToSend, created_at: new Date() };
      setMessages(prev => [...prev, tempUserMsg]);

      // Call API
      const response = await axios.post(`/api/chat?lang=${language}`, {
        message: textToSend
      });

      // Update history from backend response
      setMessages(response.data.history);
    } catch (err) {
      console.error('Error in chat:', err);
      toast.error('AI assistant offline. Verify backend status.');
    } finally {
      setSending(false);
    }
  };

  const handleClearHistory = async () => {
    if (!token) {
      setMessages([]);
      return;
    }
    try {
      await axios.delete('/api/chat/history');
      setMessages([]);
      toast.success('Chat history cleared!');
    } catch (err) {
      console.error('Error clearing chat history:', err);
      toast.error('Could not clear chat history.');
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 min-h-[calc(100vh-8rem)] flex flex-col">
      {/* Header card */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-5 shadow-sm mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-emerald-100 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 rounded-2xl">
            <MessageSquare className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-xl font-extrabold text-slate-850 dark:text-white flex items-center gap-1.5">
              <span>{t('chatTitle')}</span>
              <span className="text-xs font-semibold bg-emerald-50 dark:bg-emerald-950 text-emerald-600 dark:text-emerald-400 border border-emerald-250 dark:border-emerald-900 px-2 py-0.5 rounded-lg flex items-center gap-1">
                <Sparkles className="w-3 h-3 fill-emerald-500/20" /> Gemini 1.5
              </span>
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{t('chatSubtitle')}</p>
          </div>
        </div>

        {messages.length > 0 && (
          <button
            onClick={handleClearHistory}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold text-rose-600 hover:bg-rose-50 dark:text-rose-450 dark:hover:bg-rose-950/20 border border-transparent hover:border-rose-200 transition-colors"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>{t('chatClearBtn')}</span>
          </button>
        )}
      </div>

      {/* Main chat messages container */}
      <div className="flex-grow bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm flex flex-col h-[500px] overflow-hidden mb-4">
        
        {/* Messages scroll box */}
        <div className="flex-grow overflow-y-auto space-y-4 pr-2 mb-4 scroll-smooth">
          {loadingHistory ? (
            <div className="flex items-center justify-center h-full">
              <div className="w-8 h-8 border-3 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          ) : messages.length === 0 ? (
            /* Prompt suggest display */
            <div className="h-full flex flex-col items-center justify-center text-center p-6 max-w-lg mx-auto">
              <Bot className="w-14 h-14 text-emerald-500 mb-4 animate-bounce" />
              <h3 className="text-lg font-bold text-slate-800 dark:text-white">Namaste! How can I guide you today?</h3>
              <p className="text-xs text-slate-400 dark:text-slate-500 mt-1.5 mb-6">
                Click a sample topic below or type your custom query in the text field to get local recommendations.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full text-left">
                {samplePrompts.map((prompt, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleSend(null, prompt)}
                    className="p-3 bg-slate-50 hover:bg-emerald-50 dark:bg-slate-950 dark:hover:bg-emerald-950/20 border border-slate-200 dark:border-slate-800 hover:border-emerald-500/50 rounded-2xl text-xs font-semibold text-slate-600 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-all flex items-start gap-1.5"
                  >
                    <HelpCircle className="w-3.5 h-3.5 text-emerald-550 shrink-0 mt-0.5" />
                    <span>{prompt}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            /* Dialogue bubbles */
            <div className="space-y-4">
              {messages.map((msg) => {
                const isUser = msg.sender === 'user';
                return (
                  <div
                    key={msg.id || Math.random()}
                    className={`flex gap-3 max-w-[85%] ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
                  >
                    {/* Icon */}
                    <div className={`w-8 h-8 rounded-full shrink-0 flex items-center justify-center text-xs shadow-sm ${
                      isUser 
                        ? 'bg-emerald-600 text-white' 
                        : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
                    }`}>
                      {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4 text-emerald-550" />}
                    </div>

                    {/* Balloon body */}
                    <div className={`p-4 rounded-3xl text-sm leading-relaxed shadow-sm font-medium ${
                      isUser
                        ? 'bg-emerald-600 text-white rounded-tr-none'
                        : 'bg-slate-50 border border-slate-200 text-slate-850 dark:bg-slate-950 dark:border-slate-800 dark:text-slate-100 rounded-tl-none'
                    }`}>
                      <p className="whitespace-pre-wrap">{msg.message}</p>
                      <p className={`text-[9px] mt-1.5 ${isUser ? 'text-emerald-200' : 'text-slate-400'}`}>
                        {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                  </div>
                );
              })}
              {sending && (
                <div className="flex gap-3 max-w-[80%] mr-auto items-center">
                  <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-700 dark:bg-slate-800 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-emerald-500" />
                  </div>
                  <div className="p-3 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-3xl rounded-tl-none flex gap-1.5 items-center">
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce"></span>
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                    <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
          )}
        </div>

        {/* Input box */}
        <form onSubmit={handleSend} className="flex gap-2 border-t border-slate-100 dark:border-slate-800 pt-4 mt-auto">
          <input
            type="text"
            placeholder={t('chatInputPlaceholder')}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={sending}
            className="flex-grow p-3 bg-slate-50 dark:bg-slate-950 text-slate-850 dark:text-slate-100 border border-slate-200 dark:border-slate-800 rounded-xl outline-none focus:border-emerald-500 text-sm font-semibold disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={sending || !input.trim()}
            className="p-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-200 dark:disabled:bg-slate-850 text-white font-bold transition-all shadow-md shadow-emerald-600/10 hover-scale disabled:scale-100 shrink-0"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatBot;
