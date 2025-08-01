"""
Syllabus Management Module
Handles download, parsing, and indexing of educational syllabi
"""

import os
import json
import requests
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import PyPDF2
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import hashlib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SyllabusChunk:
    """Data class for syllabus content chunks"""
    text: str
    metadata: Dict
    embedding_id: int

class SyllabusManager:
    """Manages syllabus download, parsing, and RAG indexing"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.syllabi_dir = self.data_dir / "syllabi"
        self.embeddings_dir = self.data_dir / "vector_store"
        self.cache_dir = self.data_dir / "cache"
        
        # Create directories
        for dir_path in [self.syllabi_dir, self.embeddings_dir, self.cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # FAISS index
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self.index = None
        self.chunks_metadata = []
        
        # Load existing index if available
        self._load_existing_index()
        
        # Syllabus source URLs
        self.syllabus_sources = {
            "Karnataka State Board": {
                "base_url": "https://textbooks.karnataka.gov.in/en/class-{grade}",
                "subjects": {
                    "Math": "mathematics",
                    "Science": "science", 
                    "Social Studies": "social-science",
                    "English": "english"
                }
            },
            "ICSE": {
                "base_url": "https://byjus.com/icse-class-{grade}-syllabus",
                "subjects": {
                    "Math": "mathematics",
                    "Science": "science",
                    "Social Studies": "social-studies", 
                    "English": "english"
                }
            }
        }
    
    def download_syllabus(self, board: str, grade: str, subject: str) -> Optional[str]:
        """
        Download syllabus PDF from official sources
        
        Args:
            board: Education board (Karnataka State Board, ICSE)
            grade: Grade level (5th, 6th, 7th, 8th)
            subject: Subject name
            
        Returns:
            Path to downloaded PDF or None if failed
        """
        try:
            # Create filename
            filename = f"{board.replace(' ', '_')}_{grade}_{subject.replace(' ', '_')}.pdf"
            file_path = self.syllabi_dir / filename
            
            # Check if already exists
            if file_path.exists():
                logger.info(f"Syllabus already exists: {filename}")
                return str(file_path)
            
            # Get download URL
            download_url = self._get_download_url(board, grade, subject)
            if not download_url:
                logger.warning(f"No download URL found for {board} {grade} {subject}")
                return self._create_sample_syllabus(board, grade, subject, str(file_path))
            
            # Download PDF
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Downloaded syllabus: {filename}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to download syllabus: {e}")
            # Create sample syllabus as fallback
            return self._create_sample_syllabus(board, grade, subject, str(file_path))
    
    def _get_download_url(self, board: str, grade: str, subject: str) -> Optional[str]:
        """Get download URL for syllabus"""
        if board not in self.syllabus_sources:
            return None
        
        source = self.syllabus_sources[board]
        grade_num = grade.replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
        
        # This is a simplified URL construction
        # In a real implementation, you'd need to scrape the actual URLs
        base_url = source["base_url"].format(grade=grade_num)
        subject_slug = source["subjects"].get(subject, subject.lower())
        
        # Note: These URLs are examples - you'd need actual working URLs
        return f"{base_url}/{subject_slug}.pdf"
    
    def _create_sample_syllabus(self, board: str, grade: str, subject: str, file_path: str) -> str:
        """Create a sample syllabus for testing/fallback"""
        sample_content = self._get_sample_syllabus_content(board, grade, subject)
        
        # Create a simple PDF using reportlab (you'd need to install it)
        # For now, save as text file
        text_path = file_path.replace('.pdf', '.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        logger.info(f"Created sample syllabus: {text_path}")
        return text_path
    
    def _get_sample_syllabus_content(self, board: str, grade: str, subject: str) -> str:
        """Generate sample syllabus content"""
        samples = {
            "Math": f"""
{board} - {grade} Grade Mathematics Syllabus

Chapter 1: Number Systems
- Understanding large numbers
- Place value and face value
- Comparing and ordering numbers
- Rounding off numbers

Chapter 2: Basic Operations
- Addition and subtraction
- Multiplication and division
- BODMAS rule
- Word problems

Chapter 3: Fractions
- Understanding fractions
- Proper and improper fractions
- Mixed numbers
- Addition and subtraction of fractions

Chapter 4: Decimals
- Introduction to decimals
- Place value in decimals
- Comparing decimals
- Operations with decimals

Chapter 5: Geometry
- Lines, angles, and shapes
- Triangles and quadrilaterals
- Perimeter and area
- Basic constructions

Chapter 6: Measurement
- Length, weight, and capacity
- Time and calendar
- Money and transactions
- Data handling
            """,
            "Science": f"""
{board} - {grade} Grade Science Syllabus

Unit 1: Living World
- Plants and their parts
- Animal kingdom
- Food and nutrition
- Health and hygiene

Unit 2: Physical World
- Matter and its states
- Light and sound
- Motion and force
- Simple machines

Unit 3: Natural Phenomena
- Weather and climate
- Water cycle
- Rocks and minerals
- Solar system

Unit 4: Environmental Studies
- Pollution and conservation
- Natural resources
- Ecosystem and food chains
- Sustainable development
            """,
            "Social Studies": f"""
{board} - {grade} Grade Social Studies Syllabus

Part A: History
- Ancient civilizations
- Medieval period
- Freedom struggle
- Important personalities

Part B: Geography
- Earth and its features
- Climate and weather
- Natural resources
- Maps and globes

Part C: Civics
- Government and democracy
- Rights and duties
- Local government
- National symbols

Part D: Economics
- Basic economic concepts
- Agriculture and industry
- Trade and commerce
- Money and banking
            """,
            "English": f"""
{board} - {grade} Grade English Syllabus

Section A: Reading
- Comprehension passages
- Vocabulary building
- Reading strategies
- Literature appreciation

Section B: Writing
- Essay writing
- Letter writing
- Story writing
- Grammar and usage

Section C: Speaking
- Oral communication
- Presentations
- Group discussions
- Pronunciation

Section D: Literature
- Poems and stories
- Drama and plays
- Character analysis
- Theme exploration
            """
        }
        
        return samples.get(subject, f"Sample {subject} syllabus for {grade} grade")
    
    def parse_and_index_syllabus(self, pdf_path: str) -> bool:
        """
        Parse PDF and create FAISS index
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Success status
        """
        try:
            # Extract text from PDF
            text_content = self._extract_text_from_pdf(pdf_path)
            if not text_content:
                return False
            
            # Extract metadata from filename
            filename = Path(pdf_path).stem
            parts = filename.split('_')
            if len(parts) >= 3:
                board = parts[0].replace('_', ' ')
                grade = parts[1]
                subject = '_'.join(parts[2:]).replace('_', ' ')
            else:
                board, grade, subject = "Unknown", "Unknown", "Unknown"
            
            # Chunk the text
            chunks = self._chunk_text(text_content)
            
            # Generate embeddings
            embeddings = []
            for i, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode(chunk)
                embeddings.append(embedding)
                
                # Store metadata
                chunk_metadata = {
                    'text': chunk,
                    'board': board,
                    'grade': grade,
                    'subject': subject,
                    'chunk_id': len(self.chunks_metadata),
                    'source_file': pdf_path
                }
                self.chunks_metadata.append(chunk_metadata)
            
            # Add to FAISS index
            if self.index is None:
                self.index = faiss.IndexFlatL2(self.dimension)
            
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
            
            # Save index
            self._save_index()
            
            logger.info(f"Successfully indexed {len(chunks)} chunks from {pdf_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to parse and index {pdf_path}: {e}")
            return False
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            # Handle text files (our sample fallback)
            if pdf_path.endswith('.txt'):
                with open(pdf_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            # Handle PDF files
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Failed to extract text from {pdf_path}: {e}")
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def query_syllabus(self, query: str, board: str = None, grade: str = None, 
                      subject: str = None, top_k: int = 5) -> List[Dict]:
        """
        Query the syllabus using RAG
        
        Args:
            query: Search query
            board: Filter by board
            grade: Filter by grade  
            subject: Filter by subject
            top_k: Number of results to return
            
        Returns:
            List of relevant chunks with metadata
        """
        try:
            if self.index is None or len(self.chunks_metadata) == 0:
                return []
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query]).astype('float32')
            
            # Search in FAISS
            distances, indices = self.index.search(query_embedding, min(top_k * 3, len(self.chunks_metadata)))
            
            # Filter results by metadata
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks_metadata):
                    metadata = self.chunks_metadata[idx]
                    
                    # Apply filters
                    if board and metadata.get('board', '').lower() != board.lower():
                        continue
                    if grade and metadata.get('grade', '').lower() != grade.lower():
                        continue
                    if subject and metadata.get('subject', '').lower() != subject.lower():
                        continue
                    
                    results.append({
                        'text': metadata['text'],
                        'score': float(dist),
                        'metadata': metadata
                    })
                    
                    if len(results) >= top_k:
                        break
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to query syllabus: {e}")
            return []
    
    def _load_existing_index(self):
        """Load existing FAISS index and metadata"""
        try:
            index_path = self.embeddings_dir / "syllabus.index"
            metadata_path = self.embeddings_dir / "metadata.json"
            
            if index_path.exists() and metadata_path.exists():
                self.index = faiss.read_index(str(index_path))
                
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    self.chunks_metadata = json.load(f)
                
                logger.info(f"Loaded existing index with {len(self.chunks_metadata)} chunks")
        except Exception as e:
            logger.error(f"Failed to load existing index: {e}")
    
    def _save_index(self):
        """Save FAISS index and metadata"""
        try:
            if self.index is not None:
                index_path = self.embeddings_dir / "syllabus.index"
                faiss.write_index(self.index, str(index_path))
                
                metadata_path = self.embeddings_dir / "metadata.json"
                with open(metadata_path, 'w', encoding='utf-8') as f:
                    json.dump(self.chunks_metadata, f, indent=2, ensure_ascii=False)
                
                logger.info("Saved FAISS index and metadata")
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
    
    def get_syllabus_topics(self, board: str, grade: str, subject: str) -> List[str]:
        """Get list of topics from syllabus"""
        try:
            # Query for chapter/unit/topic headings
            queries = ["chapter", "unit", "topic", "lesson", "section"]
            all_topics = set()
            
            for query in queries:
                results = self.query_syllabus(query, board, grade, subject, top_k=10)
                for result in results:
                    text = result['text']
                    # Simple topic extraction (could be improved with NLP)
                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if any(keyword in line.lower() for keyword in ['chapter', 'unit', 'topic', 'lesson']):
                            if len(line) < 100:  # Likely a heading
                                all_topics.add(line)
            
            return list(all_topics)[:20]  # Return top 20 topics
            
        except Exception as e:
            logger.error(f"Failed to get syllabus topics: {e}")
            return []

# Test function
def test_syllabus_manager():
    """Test the syllabus manager"""
    manager = SyllabusManager()
    
    # Test download and indexing
    pdf_path = manager.download_syllabus("Karnataka State Board", "6th", "Math")
    if pdf_path:
        success = manager.parse_and_index_syllabus(pdf_path)
        print(f"Indexing success: {success}")
        
        # Test querying
        results = manager.query_syllabus("fractions", "Karnataka State Board", "6th", "Math")
        print(f"Found {len(results)} results for 'fractions'")
        for result in results[:2]:
            print(f"Score: {result['score']:.3f}")
            print(f"Text: {result['text'][:200]}...")
            print()

if __name__ == "__main__":
    test_syllabus_manager()