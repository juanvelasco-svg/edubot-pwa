from langchain_community.vectorstores import Chroma
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
        # NO inicializar embeddings aquí (evita descarga en build)
    
    def _initialize_embeddings(self):
        """Inicializa embeddings SOLO cuando se necesiten (en runtime)"""
        if self.embeddings is None:
            try:
                logger.info("Inicializando embeddings (descargando modelo si es necesario)...")
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="all-MiniLM-L6-v2",  # ✅ Modelo pequeño (80MB) vs 900MB
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
                logger.info("✓ Embeddings inicializados")
            except Exception as e:
                logger.error(f"Error inicializando embeddings: {str(e)}")
                raise
    
    def create_vectorstore(self, documents: List):
        if not documents:
            raise ValueError("No hay documentos")
        
        logger.info(f"Creando vectorstore con {len(documents)} documentos...")
        
        try:
            self._initialize_embeddings()  # ✅ Descarga modelo AQUÍ (en runtime)
            persist_directory = os.path.join(os.getcwd(), settings.vectorstore_path)
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=persist_directory
            )
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
            self.vectorstore.persist()
            logger.info("✓ Vectorstore guardado")
        except Exception as e:
            logger.error(f"Error guardando: {str(e)}")
            raise
    
    def load_vectorstore(self) -> Optional[Chroma]:
        persist_directory = os.path.join(os.getcwd(), settings.vectorstore_path)
        
        if not os.path.exists(persist_directory):
            logger.warning("Vectorstore no encontrado")
            return None
        
        try:
            logger.info("Cargando vectorstore...")
            self._initialize_embeddings()  # ✅ Descarga modelo AQUÍ (en runtime)
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
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
