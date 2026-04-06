import pdfplumber
from docx import Document
import re
from typing import Dict, List

class ResumeParser:
    """Parse resume files (PDF, DOCX, TXT) and extract structured data"""
    
    def __init__(self):
        self.skills_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'mongodb',
            'aws', 'docker', 'kubernetes', 'git', 'agile', 'api', 'rest',
            'tensorflow', 'pytorch', 'machine learning', 'data science',
            'devops', 'ci/cd', 'linux', 'windows', 'azure', 'gcp'
        ]
        
        self.education_keywords = [
            'bachelor', 'master', 'phd', 'diploma', 'certification',
            'degree', 'b.tech', 'b.s.', 'm.tech', 'm.s.', 'b.a.', 'm.a.'
        ]
    
    def parse_file(self, file_path: str) -> Dict:
        """Main parsing method"""
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            raw_text = self._parse_pdf(file_path)
        elif file_extension == 'docx':
            raw_text = self._parse_docx(file_path)
        elif file_extension == 'txt':
            raw_text = self._parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        parsed_data = self._extract_sections(raw_text)
        parsed_data['raw_text'] = raw_text
        
        return parsed_data
    
    def _parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    
    def _parse_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_sections(self, text: str) -> Dict:
        """Extract resume sections"""
        text_lower = text.lower()
        
        skills = self._extract_skills(text_lower)
        experience = self._extract_experience(text)
        education = self._extract_education(text_lower)
        certifications = self._extract_certifications(text_lower)
        
        return {
            'skills': skills,
            'experience': experience,
            'education': education,
            'certifications': certifications
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills section"""
        skills_section = re.search(r'skills?\s*[:\-]?(.*?)(?=\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if skills_section:
            skills_text = skills_section.group(1)
            skills = re.findall(r'[\w\s\+\#\.]+', skills_text)
            skills = [s.strip() for s in skills if s.strip() and len(s.strip()) > 2]
            return list(set(skills))[:20]
        
        # Fallback: extract known keywords
        found_skills = [skill for skill in self.skills_keywords if skill in text]
        return found_skills
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract experience/work history"""
        exp_section = re.search(r'(?:work\s+)?experience\s*[:\-]?(.*?)(?=education|skills?|\Z)', text, re.DOTALL | re.IGNORECASE)
        if exp_section:
            exp_text = exp_section.group(1)
            jobs = re.split(r'\n(?=[A-Z])', exp_text)
            return [job.strip()[:200] for job in jobs if job.strip()]
        return []
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education section"""
        edu_section = re.search(r'education\s*[:\-]?(.*?)(?=skills?|experience|\Z)', text, re.DOTALL | re.IGNORECASE)
        if edu_section:
            edu_text = edu_section.group(1)
            educations = re.split(r'\n(?=[A-Z])', edu_text)
            return [edu.strip() for edu in educations if edu.strip()]
        return []
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        cert_section = re.search(r'(?:certification|certifications?)\s*[:\-]?(.*?)(?=\n\n|\Z)', text, re.DOTALL | re.IGNORECASE)
        if cert_section:
            cert_text = cert_section.group(1)
            certs = re.split(r'\n', cert_text)
            return [cert.strip() for cert in certs if cert.strip()]
        return []