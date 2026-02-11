import React, { useState, useRef } from 'react'

const InputBox = ({ onSendMessage, onClearChat, disabled }) => {
  const [message, setMessage] = useState('')
  const inputRef = useRef(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSendMessage(message)
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <button
        type="button"
        onClick={onClearChat}
        className="px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors text-gray-700"
        title="Nueva conversación"
        disabled={disabled}
      >
        ✨ Nuevo tema
      </button>

      <div className="flex-1 relative">
        <input
          ref={inputRef}
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe tu pregunta aquí... (máx. 500 caracteres)"
          maxLength="500"
          disabled={disabled}
          className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
          aria-label="Mensaje para EduBot"
        />
        
        {message.length > 0 && (
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500">
            {message.length}/500
          </span>
        )}
      </div>

      <button
        type="submit"
        disabled={disabled || !message.trim()}
        className={px-6 py-3 rounded-lg transition-all  text-white font-medium flex items-center justify-center}
        aria-label="Enviar mensaje"
      >
        {disabled ? (
          <span className="animate-spin">⏳</span>
        ) : (
          '➤'
        )}
      </button>
    </form>
  )
}

export default InputBox
