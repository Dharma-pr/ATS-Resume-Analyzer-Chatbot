from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from models.database import Resume, JobDescription
from utils.resume_parser import ResumeParser
import os

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        user_id = request.form.get('user_id', 'default_user')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join('uploads', filename)
        file.save(filepath)
        
        # Parse resume
        parser = ResumeParser()
        parsed_data = parser.parse_file(filepath)
        
        # Save to database
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=filepath,
            raw_text=parsed_data['raw_text'],
            parsed_data={
                'skills': parsed_data.get('skills', []),
                'experience': parsed_data.get('experience', []),
                'education': parsed_data.get('education', []),
                'certifications': parsed_data.get('certifications', [])
            }
        )
        
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'resume_id': resume.id,
            'parsed_data': resume.parsed_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@upload_bp.route('/job-description', methods=['POST'])
def upload_job_description():
    """Upload job description"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user')
        title = data.get('title', 'Untitled')
        content = data.get('content', '')
        
        if not content:
            return jsonify({'error': 'No job description provided'}), 400
        
        # Extract keywords
        from utils.keyword_matcher import KeywordMatcher
        matcher = KeywordMatcher()
        keywords = matcher.extract_keywords(content)
        
        # Save to database
        job_desc = JobDescription(
            user_id=user_id,
            title=title,
            content=content,
            keywords=keywords
        )
        
        db.session.add(job_desc)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'job_id': job_desc.id,
            'keywords': keywords
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500