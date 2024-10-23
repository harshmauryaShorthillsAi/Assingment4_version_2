import docx
import os
from PyPDF2 import PdfReader
import pptx



from abc import ABC, abstractmethod
from typing import Any

class FileLoader(ABC):



    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """Validate the file format."""
        pass

    @abstractmethod
    def load_file(self, file_path: str) -> Any:
        """Load and return the file object."""
        pass

   

class UnifiedFileLoader(FileLoader):
    def validate_file(self, file_path: str) -> bool:
        """
        Validate the file type by checking its extension.
        """
        file_path = file_path.lower()
        if file_path.endswith('.docx'):
            return True
        elif file_path.endswith('.pdf'):
            return True
        elif file_path.endswith('.pptx') or file_path.endswith('.ppt'):
            return True
        return False

    def load_file(self, file_path: str):
        """
        Load the file based on its extension and return the appropriate object.
        """
        if not self.validate_file(file_path):
            raise ValueError("Unsupported or invalid file format. Use DOCX, PDF, or PPTX/PPT.")

        if file_path.endswith('.docx'):
            return self._load_docx(file_path)
        elif file_path.endswith('.pdf'):
            return self._load_pdf(file_path)
        elif file_path.endswith('.pptx') or file_path.endswith('.ppt'):
            return self._load_ppt(file_path)
    
    def _load_docx(self, file_path: str) -> docx.Document:
        """
        Load a DOCX file and return a Document object.
        """
        return docx.Document(file_path)

    def _load_pdf(self, file_path: str) -> PdfReader:
        """
        Load a PDF file and return a PdfReader object.
        """
        return PdfReader(file_path)

    def _load_ppt(self, file_path: str) -> pptx.Presentation:
        """
        Load a PPT/PPTX file and return a Presentation object.
        """
        return pptx.Presentation(file_path)
