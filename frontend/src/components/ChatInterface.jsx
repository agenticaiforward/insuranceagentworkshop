import React, { useState, useEffect, useRef } from 'react';
import { Send, Bot, User, Sparkles, Upload, FileText, X } from 'lucide-react';

function ChatInterface() {
    const [messages, setMessages] = useState([
        {
            role: 'agent',
            content: "Hi! I'm your AI insurance agent powered by Google Gemini. I can help you get personalized quotes for auto or home insurance, or analyze your existing policy. What would you like to do?"
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState(null);
    const [uploadedFile, setUploadedFile] = useState(null);
    const [showUpload, setShowUpload] = useState(false);
    const messagesEndRef = useRef(null);
    const inputRef = useRef(null);
    const fileInputRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);
    useEffect(() => {
        inputRef.current?.focus();
    }, []);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: input,
                    session_id: sessionId
                })
            });

            const data = await response.json();

            if (!sessionId) {
                setSessionId(data.session_id);
            }

            const agentMessage = { role: 'agent', content: data.response };
            setMessages(prev => [...prev, agentMessage]);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, {
                role: 'agent',
                content: 'Sorry, I encountered an error connecting to the server. Please make sure the backend is running and try again.'
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        if (file) {
            setUploadedFile(file);
        }
    };

    const handleUpload = async () => {
        if (!uploadedFile) return;

        setIsLoading(true);
        const formData = new FormData();
        formData.append('file', uploadedFile);

        // Add user message about upload
        setMessages(prev => [...prev, {
            role: 'user',
            content: `📄 Uploading ${uploadedFile.name} for analysis...`
        }]);

        try {
            const response = await fetch('http://127.0.0.1:8000/api/analyze-quote', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                const comparison = data.comparison_quote;
                const extracted = data.extracted_data;

                const analysisMessage = `📊 **Document Analysis Complete!**

**Current Policy:**
• Provider: ${extracted.provider}
• Type: ${extracted.policy_type}
• Current Premium: $${comparison.current_monthly_premium}/month

**Our Quote:**
• Monthly Premium: $${comparison.our_monthly_premium}/month
• **You Save: $${comparison.monthly_savings}/month** (${comparison.savings_percent}% less!)
• Annual Savings: $${comparison.annual_savings}/year

${comparison.recommendation}

Would you like me to explain how we calculated this or help you switch providers?`;

                setMessages(prev => [...prev, {
                    role: 'agent',
                    content: analysisMessage
                }]);
            } else {
                setMessages(prev => [...prev, {
                    role: 'agent',
                    content: `I had trouble analyzing that document: ${data.message || data.error}. Please make sure it's a clear image or PDF of your insurance policy.`
                }]);
            }
        } catch (error) {
            console.error('Upload error:', error);
            setMessages(prev => [...prev, {
                role: 'agent',
                content: 'Sorry, I encountered an error uploading your document. Please try again.'
            }]);
        } finally {
            setIsLoading(false);
            setUploadedFile(null);
            setShowUpload(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return (
        <div className="flex flex-col h-screen bg-gradient-to-br from-slate-50 to-blue-50">
            {/* Header */}
            <div className="bg-white border-b border-slate-200 px-6 py-4 shadow-sm">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                            <Sparkles className="h-5 w-5 text-white" />
                        </div>
                        <div>
                            <h1 className="text-lg font-bold text-slate-900">AgenticInsure AI</h1>
                            <p className="text-xs text-slate-500">Powered by Google Gemini</p>
                        </div>
                    </div>
                    <button
                        onClick={() => setShowUpload(!showUpload)}
                        className="flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 transition-colors text-sm font-medium"
                    >
                        <Upload className="h-4 w-4" />
                        Upload Policy
                    </button>
                </div>
            </div>

            {/* Upload Panel */}
            {showUpload && (
                <div className="bg-blue-50 border-b border-blue-200 px-6 py-4">
                    <div className="max-w-4xl mx-auto">
                        <div className="bg-white rounded-lg p-4 border-2 border-dashed border-blue-300">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-3">
                                    <FileText className="h-8 w-8 text-blue-500" />
                                    <div>
                                        <p className="font-medium text-slate-900">Upload Your Current Insurance Policy</p>
                                        <p className="text-sm text-slate-500">PDF, PNG, or JPG - I'll analyze it and find you a better deal!</p>
                                    </div>
                                </div>
                                <button
                                    onClick={() => setShowUpload(false)}
                                    className="text-slate-400 hover:text-slate-600"
                                >
                                    <X className="h-5 w-5" />
                                </button>
                            </div>

                            <div className="mt-4 flex items-center gap-3">
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept=".pdf,.png,.jpg,.jpeg"
                                    onChange={handleFileSelect}
                                    className="hidden"
                                />
                                <button
                                    onClick={() => fileInputRef.current?.click()}
                                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
                                >
                                    Choose File
                                </button>
                                {uploadedFile && (
                                    <>
                                        <span className="text-sm text-slate-600">{uploadedFile.name}</span>
                                        <button
                                            onClick={handleUpload}
                                            disabled={isLoading}
                                            className="ml-auto px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors text-sm font-medium"
                                        >
                                            {isLoading ? 'Analyzing...' : 'Analyze Document'}
                                        </button>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-4 py-6">
                <div className="max-w-4xl mx-auto space-y-6">
                    {messages.map((msg, i) => (
                        <div key={i} className={`flex gap-3 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            {msg.role === 'agent' && (
                                <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                                    <Bot className="h-4 w-4 text-white" />
                                </div>
                            )}
                            <div className={`max-w-[75%] rounded-2xl px-4 py-3 ${msg.role === 'user'
                                ? 'bg-blue-600 text-white'
                                : 'bg-white text-slate-900 shadow-sm border border-slate-100'
                                }`}>
                                <p className="text-sm whitespace-pre-wrap leading-relaxed">{msg.content}</p>
                            </div>
                            {msg.role === 'user' && (
                                <div className="h-8 w-8 rounded-full bg-slate-700 flex items-center justify-center flex-shrink-0">
                                    <User className="h-4 w-4 text-white" />
                                </div>
                            )}
                        </div>
                    ))}

                    {isLoading && (
                        <div className="flex gap-3 justify-start">
                            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                                <Bot className="h-4 w-4 text-white" />
                            </div>
                            <div className="bg-white rounded-2xl px-4 py-3 shadow-sm border border-slate-100">
                                <div className="flex space-x-2">
                                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                                    <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                                </div>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input */}
            <div className="bg-white border-t border-slate-200 px-4 py-4 shadow-lg">
                <div className="max-w-4xl mx-auto">
                    <div className="flex gap-3 items-end">
                        <div className="flex-1 relative">
                            <textarea
                                ref={inputRef}
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask me about insurance or upload your current policy..."
                                className="w-full rounded-2xl border border-slate-300 px-4 py-3 pr-12 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-sm"
                                rows="1"
                                style={{
                                    minHeight: '48px',
                                    maxHeight: '120px',
                                    height: 'auto'
                                }}
                                disabled={isLoading}
                            />
                        </div>
                        <button
                            onClick={sendMessage}
                            disabled={isLoading || !input.trim()}
                            className="bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full p-3 hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg flex-shrink-0"
                        >
                            <Send className="h-5 w-5" />
                        </button>
                    </div>
                    <p className="text-xs text-slate-500 mt-2 text-center">
                        Powered by Google Gemini • Press Enter to send • Click "Upload Policy" to analyze existing quotes
                    </p>
                </div>
            </div>
        </div>
    );
}

export default ChatInterface;
