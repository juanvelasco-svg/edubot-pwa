from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional
from .config import settings
import os
import logging

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        try:
            logger.info("Inicializando embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="paraphrase-multilingual-mpnet-base-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("✓ Embeddings inicializados")
        except Exception as e:
            logger.error(f"Error inicializando embeddings: {str(e)}")
            raise
    
    def create_vectorstore(self, documents: List) -> FAISS:
        if not documents:
            raise ValueError("No hay documentos")
        
        logger.info(f"Creando vectorstore con {len(documents)} documentos...")
        
        try:
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)
            logger.info("✓ Vectorstore creado")
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"Error creando vectorstore: {str(e)}")
            raise
    
    def save_vectorstore(self):
        if not self.vectorstore:
            raise ValueError("No hay vectorstore")
        
        try:
            logger.info(f"Guardando vectorstore...")
            self.vectorstore.save_local(settings.vectorstore_path)
            logger.info("✓ Vectorstore guardado")
        except Exception as e:
            logger.error(f"Error guardando: {str(e)}")
            raise
    
    def load_vectorstore(self) -> Optional[FAISS]:
        if not os.path.exists(settings.vectorstore_path):
            logger.warning("Vectorstore no encontrado")
            return None
        
        try:
            logger.info("Cargando vectorstore...")
            self.vectorstore = FAISS.load_local(
                settings.vectorstore_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("✓ Vectorstore cargado")
            return self.vectorstore
            
        except Exception as e:
            logger.error(f"Error cargando: {str(e)}")
            return None
    
    def get_retriever(self, top_k: int = None):
        if not self.vectorstore:
            raise ValueError("Vectorstore no inicializado")
        
        k = top_k or settings.top_k
        return self.vectorstore.as_retriever(search_kwargs={"k": k})
