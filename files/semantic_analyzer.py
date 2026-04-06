import spacy
from typing import Dict, List, Tuple
import re

class SemanticAnalyzer:
    """Analyze semantic meaning of resume and JD content"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Downloading spacy model...")
            import os
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        self.skill_indicators = ['proficient', 'expert', 'experienced', 'skilled', 'knowledgeable']
        self.education_indicators = ['degree', 'diploma', 'certified', 'graduated']
    
    def categorize_content(self, text: str) -> Dict[str, List[str]]:
        """Categorize text into skills, education, experience, etc."""
        doc = self.nlp(text)
        
        categories = {
            'skills': [],
            'education': [],
            'experience': [],
            'soft_skills': [],
            'certifications': []
        }
        
        sentences = [sent.text for sent in doc.sents]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Detect education
            if any(edu in sentence_lower for edu in ['bachelor', 'master', 'phd', 'degree', 'graduated']):
                categories['education'].append(sentence.strip())
            
            # Detect certifications
            elif any(cert in sentence_lower for cert in ['certified', 'certification', 'certificate']):
                categories['certifications'].append(sentence.strip())
            
            # Detect technical skills
            elif any(skill in sentence_lower for skill in ['python', 'java', 'javascript', 'sql', 'api', 'cloud', 'database']):
                categories['skills'].append(sentence.strip())
            
            # Detect soft skills
            elif any(soft in sentence_lower for soft in ['leadership', 'communication', 'teamwork', 'management', 'collaboration']):
                categories['soft_skills'].append(sentence.strip())
            
            # Detect experience
            elif any(exp in sentence_lower for exp in ['developed', 'implemented', 'managed', 'led', 'worked on', 'responsible for']):
                categories['experience'].append(sentence.strip())
        
        return categories
    
    def extract_entities(self, text: str) -> Dict:
        """Extract named entities (ORG, PERSON, PRODUCT, etc.)"""
        doc = self.nlp(text)
        
        entities = {
            'organizations': [],
            'products': [],
            'technologies': [],
            'dates': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'ORG':
                entities['organizations'].append(ent.text)
            elif ent.label_ == 'PRODUCT':
                entities['products'].append(ent.text)
            elif ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
        
        return entities
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts"""
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        
        similarity = doc1.similarity(doc2)
        return round(similarity, 3)
    
    def identify_semantic_gaps(self, resume_text: str, jd_text: str) -> Dict:
        """Identify semantic gaps between resume and JD"""
        resume_cat = self.categorize_content(resume_text)
        jd_cat = self.categorize_content(jd_text)
        
        gaps = {}
        
        for category in jd_cat:
            jd_items = set(jd_cat[category])
            resume_items = set(resume_cat[category])
            
            missing = jd_items - resume_items
            if missing:
                gaps[category] = list(missing)[:5]
        
        return gaps