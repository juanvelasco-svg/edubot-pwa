@"
# EduBot - Chatbot Educativo PWA

Asistente de estudio inteligente para estudiantes universitarios. Basado en RAG con documentos académicos.

## 🚀 Características

- **PWA Installable**: Funciona offline y se instala como app nativa
- **RAG Avanzado**: Respuestas basadas en documentos académicos específicos
- **Multi-usuario**: Soporta +100 estudiantes simultáneamente
- **Totalmente Gratuito**: Despliegue en servicios gratuitos

## 📋 Requisitos

- Node.js 18+
- Python 3.11+
- API Key de Groq (gratis)

## 🛠️ Instalación Local

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tu API key de Groq
python src/main.py
