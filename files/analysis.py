from flask import Blueprint, request, jsonify
from app import db
from models.database import Resume, JobDescription, Analysis
from utils.keyword_matcher import KeywordMatcher
from utils.semantic_analyzer import SemanticAnalyzer
from utils.llm_handler import LLMHandler

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job description"""
    try:
        data = request.get_json()
        resume_id = data.get('resume_id')
        job_id = data.get('job_id')
        
        if not resume_id or not job_id:
            return jsonify({'error': 'Missing resume_id or job_id'}), 400
        
        # Fetch data
        resume = Resume.query.get(resume_id)
        job_desc = JobDescription.query.get(job_id)
        
        if not resume or not job_desc:
            return jsonify({'error': 'Resume or Job Description not found'}), 404
        
        # Keyword matching
        matcher = KeywordMatcher()
        resume_keywords = matcher.extract_keywords(resume.raw_text)
        jd_keywords = matcher.extract_keywords(job_desc.content)
        
        match_results = matcher.match_keywords(resume_keywords, jd_keywords)
        
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        semantic_gaps = analyzer.identify_semantic_gaps(resume.raw_text, job_desc.content)
        
        # Generate feedback using LLM
        llm_handler = LLMHandler()
        analysis_data = {
            'matched_keywords': match_results['matched_keywords'],
            'missing_keywords': match_results['missing_keywords'],
            'match_score': match_results['match_score'],
            'semantic_gaps': semantic_gaps
        }
        
        feedback = llm_handler.generate_initial_feedback(analysis_data)
        
        # Generate recommendations
        recommendations = _generate_recommendations(
            match_results['missing_keywords'],
            semantic_gaps
        )
        
        # Save analysis
        analysis = Analysis(
            resume_id=resume_id,
            job_id=job_id,
            match_score=match_results['match_score'],
            matched_keywords=match_results['matched_keywords'],
            missing_keywords=match_results['missing_keywords'],
            semantic_gaps=semantic_gaps,
            feedback=feedback,
            recommendations=recommendations
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'analysis_id': analysis.id,
            'match_score': match_results['match_score'],
            'matched_keywords': match_results['matched_keywords'],
            'missing_keywords': match_results['missing_keywords'],
            'semantic_gaps': semantic_gaps,
            'feedback': feedback,
            'recommendations': recommendations
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _generate_recommendations(missing_keywords, semantic_gaps):
    """Generate actionable recommendations"""
    recommendations = []
    
    if missing_keywords:
        if len(missing_keywords) > 0:
            recommendations.append(f"Add experience with: {', '.join(missing_keywords[:5])}")
    
    if 'skills' in semantic_gaps:
        recommendations.append(f"Highlight your proficiency in: {', '.join(semantic_gaps['skills'][:3])}")
    
    if 'education' in semantic_gaps:
        recommendations.append("Consider adding formal education or certifications mentioned in the job description")
    
    if 'certifications' in semantic_gaps:
        recommendations.append(f"Pursue certifications: {', '.join(semantic_gaps['certifications'][:3])}")
    
    recommendations.append("Quantify your achievements with metrics and numbers")
    recommendations.append("Use action verbs and industry-specific terminology")
    
    return recommendations[:5]