from typing import Dict, List, Tuple
import re
from difflib import SequenceMatcher

class KeywordMatcher:
    """Match keywords between resume and job description"""
    
    def __init__(self):
        self.technical_keywords = [
            'python', 'java', 'javascript', 'typescript', 'react', 'vue', 'angular',
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring boot',
            'postgresql', 'mongodb', 'mysql', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'git', 'gitlab', 'github', 'bitbucket',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'rest api', 'graphql', 'grpc', 'soap',
            'ci/cd', 'devops', 'microservices', 'agile', 'scrum'
        ]
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        text_lower = text.lower()
        
        # Find technical keywords
        found_keywords = []
        for keyword in self.technical_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        # Extract custom keywords (words between 4-30 chars with special consideration)
        words = re.findall(r'\b[a-z]{4,30}\+?\b', text_lower)
        words = [w for w in words if w not in ['the', 'that', 'this', 'with', 'from']]
        
        found_keywords.extend(words)
        
        # Remove duplicates and return
        return list(set(found_keywords))
    
    def match_keywords(self, resume_keywords: List[str], jd_keywords: List[str]) -> Dict:
        """Match keywords and calculate match score"""
        resume_set = set(resume_keywords)
        jd_set = set(jd_keywords)
        
        matched = list(resume_set & jd_set)
        missing = list(jd_set - resume_set)
        extra = list(resume_set - jd_set)
        
        # Calculate match score (0-100)
        if len(jd_set) == 0:
            match_score = 0
        else:
            match_score = round((len(matched) / len(jd_set)) * 100, 2)
        
        return {
            'matched_keywords': matched,
            'missing_keywords': missing,
            'extra_keywords': extra,
            'match_score': match_score,
            'total_jd_keywords': len(jd_set),
            'matched_count': len(matched)
        }
    
    def find_similar_keywords(self, keyword: str, candidates: List[str], threshold: float = 0.7) -> List[Tuple[str, float]]:
        """Find similar keywords using sequence matching"""
        similarities = []
        
        for candidate in candidates:
            ratio = SequenceMatcher(None, keyword.lower(), candidate.lower()).ratio()
            if ratio >= threshold:
                similarities.append((candidate, ratio))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)
    
    def categorize_missing_keywords(self, missing: List[str]) -> Dict:
        """Categorize missing keywords"""
        categories = {
            'technical_skills': [],
            'soft_skills': [],
            'tools': [],
            'certifications': [],
            'other': []
        }
        
        soft_skills = ['leadership', 'communication', 'teamwork', 'management', 'collaboration', 'problem-solving']
        tools = ['jira', 'confluence', 'slack', 'docker', 'kubernetes', 'jenkins']
        certifications = ['aws', 'certification', 'certified', 'ccna', 'ckad']
        
        for keyword in missing:
            if any(tech in keyword.lower() for tech in ['python', 'java', 'javascript', 'sql', 'api']):
                categories['technical_skills'].append(keyword)
            elif any(soft in keyword.lower() for soft in soft_skills):
                categories['soft_skills'].append(keyword)
            elif any(tool in keyword.lower() for tool in tools):
                categories['tools'].append(keyword)
            elif any(cert in keyword.lower() for cert in certifications):
                categories['certifications'].append(keyword)
            else:
                categories['other'].append(keyword)
        
        return {k: v for k, v in categories.items() if v}