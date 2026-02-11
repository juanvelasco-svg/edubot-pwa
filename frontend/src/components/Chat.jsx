import React, { useState, useEffect, useRef } from 'react'
import Message from './Message'
import InputBox from './InputBox'
import { sendMessage } from '../services/api'

const Chat = () => {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    const welcomeMessage = {
      id: 'welcome',
      content: Hola! Soy tu Asistente de Estudio

Estoy aquí para ayudarte a comprender mejor el material del curso. Tengo acceso a todos los apuntes y documentos académicos.

Puedo ayudarte a:
- Explicar conceptos del temario
- Aclarar dudas específicas  
- Repasar temas antes del examen
- Relacionar ideas entre diferentes temas

Recuerda: aprenderás mejor si razonamos juntos. No estoy aquí para hacer tu tarea, sino para guiarte.

¿Qué tema quieres explorar hoy?,
      sender: 'bot',
      timestamp: new Date()
    }

    setMessages([welcomeMessage])
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async (message) => {
    if (!message.trim()) return

    const userMessage = {
      id: Date.now(),
      content: message,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      const response = await sendMessage(message)
      
      const botMessage = {
        id: Date.now() + 1,
        content: response.response,
        sender: 'bot',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (err) {
      setError('Error al conectar con el servidor. Por favor, inténtalo de nuevo.')
      console.error('Error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleClearChat = () => {
    if (confirm('¿Quieres empezar una nueva conversación?')) {
      setMessages([])
      const welcomeMessage = {
        id: 'welcome',
        content: Hola! Soy tu Asistente de Estudio

Estoy aquí para ayudarte a comprender mejor el material del curso. Tengo acceso a todos los apuntes y documentos académicos.

Puedo ayudarte a:
- Explicar conceptos del temario
- Aclarar dudas específicas  
- Repasar temas antes del examen
- Relacionar ideas entre diferentes temas

Recuerda: aprenderás mejor si razonamos juntos. No estoy aquí para hacer tu tarea, sino para guiarte.

¿Qué tema quieres explorar hoy?,
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages([welcomeMessage])
    }
  }

  return (
    <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col px-4 py-6">
      <div className="flex-1 overflow-y-auto mb-4 space-y-4 pr-2">
        {messages.map((message) => (
          <Message 
            key={message.id} 
            message={message} 
            onRegenerate={() => handleSendMessage(message.content)}
          />
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-tl-sm p-4 shadow-md max-w-[80%] animate-pulse">
              <div className="space-y-2">
                <div className="skeleton h-4 w-48"></div>
                <div className="skeleton h-4 w-64"></div>
                <div className="skeleton h-4 w-56"></div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-r-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <InputBox 
        onSendMessage={handleSendMessage} 
        onClearChat={handleClearChat}
        disabled={isLoading}
      />
    </div>
  )
}

export default Chat
