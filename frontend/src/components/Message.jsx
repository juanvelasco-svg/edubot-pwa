import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const Message = ({ message, onRegenerate }) => {
  const isBot = message.sender === 'bot'
  
  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className={lex }>
      <div className={max-w-[85%] }>
        {isBot && (
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center mb-2">
            <span className="text-white font-bold">📚</span>
          </div>
        )}

        <div 
          className={ounded-2xl p-4 shadow-md }
        >
          <div className="prose max-w-none">
            {isBot ? (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            ) : (
              <p>{message.content}</p>
            )}
          </div>
        </div>

        <div className={lex items-center mt-1 space-x-2 }>
          <span className={	ext-xs }>
            {formatTime(message.timestamp)}
          </span>
          
          {isBot && onRegenerate && (
            <button
              onClick={onRegenerate}
              className="text-xs text-blue-500 hover:text-purple-600 transition-colors"
              title="Regenerar respuesta"
            >
              ♻️ Regenerar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Message
