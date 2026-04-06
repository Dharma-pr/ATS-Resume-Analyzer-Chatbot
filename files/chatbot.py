from flask import Blueprint, request, jsonify
from app import db
from models.database import Analysis, ChatMessage
from utils.llm_handler import LLMHandler

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/message', methods=['POST'])
def chat():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        user_message = data.get('message')
        
        if not analysis_id or not user_message:
            return jsonify({'error': 'Missing analysis_id or message'}), 400
        
        # Fetch analysis
        analysis = Analysis.query.get(analysis_id)
        if not analysis:
            return jsonify({'error': 'Analysis not found'}), 404
        
        # Get chat history
        chat_history = ChatMessage.query.filter_by(analysis_id=analysis_id).all()
        history_dicts = [
            {'role': msg.role, 'content': msg.content}
            for msg in chat_history
        ]
        
        # Prepare analysis data for context
        analysis_data = {
            'matched_keywords': analysis.matched_keywords,
            'missing_keywords': analysis.missing_keywords,
            'match_score': analysis.match_score,
            'semantic_gaps': analysis.semantic_gaps
        }
        
        # Generate response
        llm_handler = LLMHandler()
        response_text = llm_handler.chat_response(history_dicts, user_message, analysis_data)
        
        # Save messages to database
        user_msg = ChatMessage(
            analysis_id=analysis_id,
            role='user',
            content=user_message
        )
        
        assistant_msg = ChatMessage(
            analysis_id=analysis_id,
            role='assistant',
            content=response_text
        )
        
        db.session.add(user_msg)
        db.session.add(assistant_msg)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response_text,
            'message_id': assistant_msg.id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/history/<int:analysis_id>', methods=['GET'])
def get_chat_history(analysis_id):
    """Get chat history for an analysis"""
    try:
        messages = ChatMessage.query.filter_by(analysis_id=analysis_id).all()
        
        history = [
            {
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat()
            }
            for msg in messages
        ]
        
        return jsonify({
            'success': True,
            'history': history
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500