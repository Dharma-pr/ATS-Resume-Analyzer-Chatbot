import os
from typing import List, Dict
import openai
from anthropic import Anthropic

class LLMHandler:
    """Handle LLM interactions for chatbot"""
    
    def __init__(self):
        self.llm_provider = os.getenv('LLM_PROVIDER', 'openai')
        self.model = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        
        if self.llm_provider == 'openai':
            openai.api_key = os.getenv('OPENAI_API_KEY')
        elif self.llm_provider == 'anthropic':
            self.anthropic_client = Anthropic()
    
    def generate_initial_feedback(self, analysis_data: Dict) -> str:
        """Generate initial feedback based on analysis"""
        prompt = self._build_feedback_prompt(analysis_data)
        return self._call_llm(prompt)
    
    def chat_response(self, chat_history: List[Dict], user_message: str, analysis_data: Dict) -> str:
        """Generate chatbot response"""
        system_prompt = self._build_system_prompt(analysis_data)
        
        # Format chat history
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        for msg in chat_history:
            messages.append({
                "role": msg['role'],
                "content": msg['content']
            })
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        return self._call_llm_chat(messages)
    
    def _build_system_prompt(self, analysis_data: Dict) -> str:
        """Build system prompt for chatbot"""
        matched = ", ".join(analysis_data.get('matched_keywords', [])[:5])
        missing = ", ".join(analysis_data.get('missing_keywords', [])[:5])
        score = analysis_data.get('match_score', 0)
        
        return f"""You are an expert HR consultant and career coach specializing in resume optimization and job application feedback.

Your role is to:
1. Explain why a resume may not have matched with a job description
2. Provide constructive, actionable feedback
3. Suggest specific improvements to the resume
4. Encourage and support the job seeker

Current Analysis Data:
- Match Score: {score}%
- Matched Keywords: {matched}
- Missing Keywords: {missing}

Always be:
- Positive and encouraging
- Specific with recommendations
- Data-driven based on the analysis
- Professional but friendly

When users ask questions, provide detailed explanations and next steps."""
    
    def _build_feedback_prompt(self, analysis_data: Dict) -> str:
        """Build prompt for initial feedback"""
        matched = ", ".join(analysis_data.get('matched_keywords', [])[:10])
        missing = ", ".join(analysis_data.get('missing_keywords', [])[:10])
        score = analysis_data.get('match_score', 0)
        semantic_gaps = analysis_data.get('semantic_gaps', {})
        
        return f"""Based on the following resume analysis for a job application:

Match Score: {score}%
Matched Keywords: {matched}
Missing Keywords: {missing}
Semantic Gaps: {semantic_gaps}

Please provide:
1. A brief summary of why this resume may not have been selected
2. The top 3 missing areas
3. 3-5 specific, actionable recommendations to improve the resume
4. An encouraging message about their candidacy

Format the response clearly with headings and bullet points."""
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API"""
        if self.llm_provider == 'openai':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful HR consultant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == 'anthropic':
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    
    def _call_llm_chat(self, messages: List[Dict]) -> str:
        """Call LLM for chat"""
        if self.llm_provider == 'openai':
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content
        
        elif self.llm_provider == 'anthropic':
            # Convert to Anthropic format
            user_messages = [m for m in messages if m['role'] == 'user']
            system_msg = next((m['content'] for m in messages if m['role'] == 'system'), "")
            
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                system=system_msg,
                messages=user_messages
            )
            return response.content[0].text