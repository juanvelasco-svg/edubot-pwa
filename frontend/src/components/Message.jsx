import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const Message = ({ message, onRegenerate }) => {
  const isBot = message.sender === 'bot'
  
  const formatTime = (date) => {
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return hours + ':' + minutes
  }

  return (
    <div className={isBot ? 'flex justify-start' : 'flex justify-end'}>
      <div className={isBot ? 'max-w-[85%] items-start' : 'max-w-[85%] items-end'}>
        {isBot && (
          <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mb-2">
            <span className="text-white font-bold">E</span>
          </div>
        )}

        <div 
          className={isBot 
            ? 'rounded-2xl p-4 shadow-md bg-white rounded-tl-sm' 
            : 'rounded-2xl p-4 shadow-md bg-blue-500 text-white rounded-tr-sm'
          }
        >
          {isBot ? (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {message.content}
            </ReactMarkdown>
          ) : (
            <p>{message.content}</p>
          )}
        </div>

        <div className={isBot ? 'flex items-center mt-1 space-x-2 justify-start' : 'flex items-center mt-1 space-x-2 justify-end'}>
          <span className={isBot ? 'text-xs text-gray-500' : 'text-xs text-blue-100'}>
            {formatTime(message.timestamp)}
          </span>
          
          {isBot && onRegenerate && (
            <button
              onClick={onRegenerate}
              className="text-xs text-blue-500 hover:text-purple-600"
            >
              Regenerar
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

export default Message
