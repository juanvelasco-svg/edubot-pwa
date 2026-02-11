import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('Error en la solicitud API:', error)
    
    if (error.response) {
      switch (error.response.status) {
        case 429:
          throw new Error('Demasiadas solicitudes. Por favor, espera un momento.')
        case 503:
          throw new Error('Servicio no disponible temporalmente.')
        case 500:
          throw new Error('Error interno del servidor.')
        default:
          throw new Error(error.response.data?.detail || 'Error en la solicitud.')
      }
    } else if (error.request) {
      throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.')
    } else {
      throw new Error('Error al configurar la solicitud.')
    }
  }
)

export const sendMessage = async (message) => {
  const response = await api.post('/chat', {
    message: message,
    conversation_id: null
  })
  
  return response.data
}

export default api
