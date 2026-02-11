from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .config import settings
from .vector_store import VectorStoreManager
import logging

logger = logging.getLogger(__name__)

class EduBotRAG:
    def __init__(self, vectorstore_manager: VectorStoreManager):
        self.vectorstore_manager = vectorstore_manager
        self.llm = None
        self.chain = None
        self._initialize_llm()
        self._create_chain()
    
    def _initialize_llm(self):
        try:
            logger.info(f"Inicializando LLM: {settings.model_name}")
            self.llm = ChatGroq(
                groq_api_key=settings.groq_api_key,
                model_name=settings.model_name,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            logger.info("✓ LLM inicializado")
        except Exception as e:
            logger.error(f"Error inicializando LLM: {str(e)}")
            raise
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        template = """
Eres EduBot, un asistente de estudio universitario experto y pedagógico.
Tu rol es ayudar a los estudiantes a comprender mejor el material académico.

**CARACTERÍSTICAS:**
- Usa tuteo (tú, te, tu) para ser cercano pero profesional
- Eres motivador, paciente y fomentas el pensamiento crítico
- Usas lenguaje académico pero accesible
- NO resuelves tareas directamente, guías el aprendizaje paso a paso
- Incluyes ejemplos y analogías para clarificar conceptos

**REGLAS:**
1. Si la información NO está en los documentos, di:
   "Este tema no está en el material del curso disponible. Te recomiendo revisar la bibliografía adicional o consultar con el profesor."

2. Si detectas que quieren que resuelvas una tarea completa, responde:
   "Entiendo que necesitas ayuda con este ejercicio. ¿Qué tal si te explico el concepto primero y luego te guío paso a paso? ¿Qué parte te resulta más difícil?"

3. Siempre incluye preguntas de seguimiento como:
   "¿Tiene sentido? ¿Quieres que profundice en algún aspecto?"
   "¿Quieres un ejemplo práctico de esto?"

**DOCUMENTOS DE REFERENCIA:**
{context}

**PREGUNTA DEL ESTUDIANTE:**
{question}

**RESPUESTA (en español, 300-500 palabras máximo, usa markdown para formato):**
"""
        return ChatPromptTemplate.from_template(template)
    
    def _create_chain(self):
        prompt = self._create_prompt_template()
        retriever = self.vectorstore_manager.get_retriever()
        
        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def get_response(self, question: str) -> str:
        try:
            logger.info(f"Procesando pregunta...")
            
            if len(question) > 500:
                return "Tu pregunta es demasiado larga. Por favor, hazla más concisa (máx. 500 caracteres)."
            
            if len(question.strip()) < 3:
                return "Por favor, haz una pregunta más específica para poder ayudarte mejor."
            
            response = self.chain.invoke(question)
            
            if len(response) > 300:
                follow_up = "\n\n¿Tiene sentido lo que te he explicado? ¿Quieres que profundice en algún aspecto específico o prefieres un ejemplo práctico?"
                response += follow_up
            
            logger.info("✓ Respuesta generada")
            return response
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {str(e)}")
            return "Lo siento, ocurrió un error. Por favor, inténtalo de nuevo más tarde."

def initialize_edubot() -> EduBotRAG:
    vectorstore_manager = VectorStoreManager()
    
    vectorstore = vectorstore_manager.load_vectorstore()
    
    if not vectorstore:
        logger.info("Vectorstore no encontrado, creando nuevo...")
        from .document_loader import process_documents
        
        documents = process_documents()
        if documents:
            vectorstore = vectorstore_manager.create_vectorstore(documents)
            vectorstore_manager.save_vectorstore()
        else:
            raise ValueError("No se pudieron cargar documentos")
    
    return EduBotRAG(vectorstore_manager)
