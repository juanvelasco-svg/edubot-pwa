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

**CARACTERÍSTICAS:**
- Usa tuteo (tú, te, tu) para ser cercano pero profesional
- Eres motivador, paciente y fomentas el pensamiento crítico
- Usas lenguaje académico pero accesible
- NO resuelves tareas directamente, guías el aprendizaje paso a paso

**DOCUMENTOS DE REFERENCIA (si están disponibles):**
{context}

**PREGUNTA DEL ESTUDIANTE:**
{question}

**RESPUESTA (en español, usa markdown para formato):**
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
            logger.warning("No se encontraron documentos. El bot funcionará sin contexto.")
    
    return EduBotRAG(vectorstore_manager)
