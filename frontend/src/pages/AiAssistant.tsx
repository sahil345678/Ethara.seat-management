import { useState, useRef, useEffect } from 'react';
import { useAiQuery } from '../hooks/useAi';
import { Send, Bot, User, Sparkles, Loader2, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

export const AiAssistant = () => {
  const [messages, setMessages] = useState<{ role: 'user' | 'ai'; text: string; isError?: boolean }[]>([
    { role: 'ai', text: 'Hello! I am the Ethara AI Assistant. I can help you find employees, check seat utilization, or locate available spaces. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const { mutateAsync: sendQuery, isPending } = useAiQuery();
  const endRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isPending]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isPending) return;

    const query = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: query }]);

    try {
      const response = await sendQuery(query);
      setMessages(prev => [...prev, { role: 'ai', text: response.answer }]);
    } catch (error: any) {
      setMessages(prev => [...prev, { 
        role: 'ai', 
        text: error.message || 'I encountered an error connecting to the backend service. Please ensure the API is running.',
        isError: true
      }]);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col max-w-4xl mx-auto animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-3xl font-black text-gray-900 tracking-tight flex items-center">
          <Sparkles className="w-8 h-8 text-blue-600 mr-3" />
          AI Assistant
        </h1>
        <p className="mt-1 text-base text-gray-500">Powered by Google Gemini 1.5 & the Service Layer Router.</p>
      </div>

      {/* Chat Container */}
      <div className="flex-1 card overflow-hidden flex flex-col bg-white shadow-sm border border-gray-200">
        
        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 bg-gray-50/30">
          {messages.map((msg, idx) => (
            <div key={idx} className={clsx("flex gap-4 max-w-3xl", msg.role === 'user' ? "ml-auto flex-row-reverse" : "mr-auto")}>
              
              <div className={clsx("flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center shadow-sm ring-1 ring-inset", 
                msg.role === 'user' ? "bg-indigo-100 text-indigo-700 ring-indigo-200" : "bg-blue-600 text-white ring-blue-700"
              )}>
                {msg.role === 'user' ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
              </div>
              
              <div className={clsx("px-5 py-3.5 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap shadow-sm", 
                msg.role === 'user' 
                  ? "bg-indigo-600 text-white rounded-tr-sm" 
                  : msg.isError 
                    ? "bg-red-50 text-red-800 border border-red-200 rounded-tl-sm"
                    : "bg-white text-gray-800 border border-gray-100 rounded-tl-sm"
              )}>
                {msg.isError && <AlertCircle className="w-4 h-4 inline mr-2 text-red-500 mb-0.5" />}
                {msg.text}
              </div>
            </div>
          ))}
          
          {isPending && (
            <div className="flex gap-4 max-w-3xl mr-auto">
              <div className="flex-shrink-0 h-10 w-10 rounded-full bg-blue-600 text-white flex items-center justify-center shadow-sm">
                <Bot className="w-5 h-5" />
              </div>
              <div className="px-5 py-3.5 rounded-2xl bg-white border border-gray-100 rounded-tl-sm shadow-sm flex items-center">
                <Loader2 className="w-4 h-4 animate-spin text-blue-600 mr-2" />
                <span className="text-sm text-gray-500">Analyzing intent and querying database...</span>
              </div>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Input Form */}
        <div className="p-4 bg-white border-t border-gray-100">
          <form onSubmit={handleSubmit} className="relative flex items-center">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask 'Where is John seated?' or 'Show available seats on floor 2'..."
              className="w-full rounded-full border-gray-300 bg-gray-50 pl-5 pr-14 py-3.5 text-sm focus:border-blue-500 focus:ring-blue-500 shadow-inner transition-colors focus:bg-white"
              disabled={isPending}
            />
            <button
              type="submit"
              disabled={!input.trim() || isPending}
              className="absolute right-2 p-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:hover:bg-blue-600 transition-colors shadow-sm"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <p className="text-[10px] text-center mt-2 text-gray-400">
            Natural language interface securely routed through internal API endpoints. No direct DB access.
          </p>
        </div>
      </div>
    </div>
  );
};
