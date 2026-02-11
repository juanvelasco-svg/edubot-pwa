from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from .config import settings
import os
import logging

logger = logging.getLogger(__name__)

def load_documents() -> List:
    documents = []
    
    if not os.path.exists(settings.documents_path):
        logger.warning(f"Directorio no encontrado: {settings.documents_path}")
        return documents
    
    pdf_files = [f for f in os.listdir(settings.documents_path) if f.endswith('.pdf')]
    
    if not pdf_files:
        logger.warning("No se encontraron PDFs")
        return documents
    
    logger.info(f"Encontrados {len(pdf_files)} PDFs")
    
    for pdf_file in pdf_files:
        file_path = os.path.join(settings.documents_path, pdf_file)
        try:
            logger.info(f"Cargando: {pdf_file}")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            
            for doc in docs:
                doc.metadata["source"] = pdf_file
            
            documents.extend(docs)
            logger.info(f"✓ Cargado {pdf_file}")
            
        except Exception as e:
            logger.error(f"Error cargando {pdf_file}: {str(e)}")
    
    return documents

def split_documents(documents: List) -> List:
    if not documents:
        return []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Divididos en {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        chunk.metadata["total_chunks"] = len(chunks)
    
    return chunks

def process_documents() -> List:
    logger.info("Iniciando procesamiento...")
    
    documents = load_documents()
    if not documents:
        logger.warning("No hay documentos")
        return []
    
    chunks = split_documents(documents)
    
    logger.info(f"Procesamiento completado: {len(chunks)} chunks")
    return chunks
