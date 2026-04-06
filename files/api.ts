import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadResume = async (file: File, userId: string = 'default_user') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  
  return apiClient.post('/upload/resume', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const uploadJobDescription = async (title: string, content: string, userId: string = 'default_user') => {
  return apiClient.post('/upload/job-description', {
    title,
    content,
    user_id: userId,
  });
};

export const analyzeResume = async (resumeId: number, jobId: number) => {
  return apiClient.post('/analysis/analyze', {
    resume_id: resumeId,
    job_id: jobId,
  });
};

export const sendChatMessage = async (analysisId: number, message: string) => {
  return apiClient.post('/chatbot/message', {
    analysis_id: analysisId,
    message,
  });
};

export const getChatHistory = async (analysisId: number) => {
  return apiClient.get(`/chatbot/history/${analysisId}`);
};

export const checkHealth = async () => {
  return apiClient.get('/health');
};