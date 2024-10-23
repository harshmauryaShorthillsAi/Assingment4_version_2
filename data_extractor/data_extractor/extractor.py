from typing import Any, Dict, List, Union
import fitz
import pdfplumber
# from data_extractor.data_extractor.extractor import Extractor

from abc import ABC, abstractmethod

class Extractor(ABC):
    @abstractmethod
    def load(self, file_path):
        pass

    @abstractmethod
    def extract_text(self):
        pass
    
    @abstractmethod
    def extract_images(self):
        pass
    
    @abstractmethod
    def extract_urls(self):
        pass
    
    @abstractmethod
    def extract_tables(self):
        pass





class FileExtractor(Extractor):
    def __init__(self, loader, file_type: str):
        self.loader = loader
        self.file_type = file_type
        self.file = None
        self.file_path = None

    def load(self, file_path: str):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path

    def extract_text(self) -> str:
        """Extract text from the file, based on file type."""
        text = ""
        if self.file_type == "docx":
            doc = self.loader.load_file(self.file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            for table in doc.tables:
                for row in table.rows:
                    row_text = "\t".join(cell.text.strip() for cell in row.cells)
                    text += row_text + "\n"
        
        elif self.file_type == "pdf":
            reader = self.loader.load_file(self.file_path)
            for page in reader.pages:
                text += page.extract_text()
        
        elif self.file_type == "pptx":
            ppt = self.loader.load_file(self.file_path)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
                    if shape.has_table:
                        for row in shape.table.rows:
                            row_text = "\t".join(cell.text.strip() for cell in row.cells)
                            text += row_text + "\n"
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        return text

    def extract_images(self) -> List[Dict[str, Any]]:
        """Extract images from the file, based on file type."""
        images = []
        
        if self.file_type == "docx":
            doc = self.loader.load_file(self.file_path)
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    image_blob = rel.target_part.blob
                    image_ext = rel.target_part.content_type.split('/')[1]
                    if image_blob is not None:
                        images.append({
                            "image_data": image_blob,
                            "ext": image_ext
                        })
        
        elif self.file_type == "pdf":
            pdf_document = fitz.open(self.file_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                image_list = page.get_images(full=True)
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    images.append({
                        "image_data": base_image["image"],
                        "ext": base_image["ext"],
                        "page": page_num + 1,
                        "dimensions": (base_image["width"], base_image["height"])
                    })
            pdf_document.close()
        
        elif self.file_type == "pptx":
            ppt = self.loader.load_file(self.file_path)
            for slide_num, slide in enumerate(ppt.slides):
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # Picture type
                        images.append({
                            "image_data": shape.image.blob,
                            "ext": shape.image.ext,
                            "page": slide_num + 1
                        })
        
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        return images

    def extract_urls(self) -> List[Dict[str, Any]]:
        """Extract URLs from the file, based on file type."""
        extracted_links = []
        
        if self.file_type == "docx":
            for rel in self.file.part.rels.values():
                if "hyperlink" in rel.reltype:
                    hyperlink = rel.target_ref
                    linked_text = None
                    page_number = None
                    for para_index, para in enumerate(self.file.paragraphs, start=1):
                        for run in para.runs:
                            if hyperlink in run._element.xml:
                                linked_text = run.text
                                page_number = para_index
                                break
                        if linked_text:
                            break
                    extracted_links.append({
                        "linked_text": linked_text or "",
                        "url": hyperlink,
                        "page_number": page_number
                    })
        
        elif self.file_type == "pdf":
            for page_num, page in enumerate(self.file.pages, start=1):
                if '/Annots' in page:
                    annotations = page['/Annots']
                    for annot in annotations:
                        annot_obj = annot.get_object()
                        if '/A' in annot_obj and '/URI' in annot_obj['/A']:
                            link = annot_obj['/A']['/URI']
                            extracted_links.append({
                                "linked_text": link,
                                "url": link,
                                "page_number": page_num
                            })
        
        elif self.file_type == "pptx":
            for slide_num, slide in enumerate(self.file.slides, start=1):
                for shape in slide.shapes:
                    if hasattr(shape, "text_frame") and shape.text_frame is not None:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                if run.hyperlink and run.hyperlink.address:
                                    extracted_links.append({
                                        "linked_text": run.text,
                                        "url": run.hyperlink.address,
                                        "page_number": slide_num
                                    })
        
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        return extracted_links

    def extract_tables(self) -> List[List[str]]:
        """Extract tables from the file, based on file type."""
        tables = []
        
        if self.file_type == "docx":
            doc = self.loader.load_file(self.file_path)
            for table in doc.tables:
                tables.append([[cell.text.strip() for cell in row.cells] for row in table.rows])
        
        elif self.file_type == "pdf":
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    tables.extend(page.extract_tables())
        
        elif self.file_type == "pptx":
            ppt = self.loader.load_file(self.file_path)
            for slide in ppt.slides:
                for shape in slide.shapes:
                    if shape.has_table:
                        table_content = [[cell.text_frame.text.strip() if cell.text_frame else '' for cell in row.cells] for row in shape.table.rows]
                        tables.append(table_content)
        
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")
        
        return tables







