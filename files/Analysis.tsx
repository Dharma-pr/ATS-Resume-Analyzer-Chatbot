import React, { useState } from 'react';
import { analyzeResume } from '../services/api';
import { AnalysisResults } from '../components/AnalysisResults';
import { ChatBot } from '../components/ChatBot';
import { Loader } from 'lucide-react';

interface AnalysisPageProps {
  resumeId: number;
  jobId: number;
}

interface AnalysisData {
  match_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  semantic_gaps: Record<string, string[]>;
  feedback: string;
  recommendations: string[];
}

export const AnalysisPage: React.FC<AnalysisPageProps> = ({ resumeId, jobId }) => {
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [analysisId, setAnalysisId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await analyzeResume(resumeId, jobId);
      setAnalysis({
        match_score: response.data.match_score,
        matched_keywords: response.data.matched_keywords,
        missing_keywords: response.data.missing_keywords,
        semantic_gaps: response.data.semantic_gaps,
        feedback: response.data.feedback,
        recommendations: response.data.recommendations,
      });
      setAnalysisId(response.data.analysis_id);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to analyze resume');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="w-full bg-purple-500 hover:bg-purple-600 disabled:bg-gray-300 text-white py-3 px-4 rounded-lg font-semibold flex items-center justify-center gap-2"
      >
        {loading && <Loader className="w-5 h-5 animate-spin" />}
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      {analysis && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <AnalysisResults data={analysis} />
          </div>
          <div className="lg:col-span-1">
            {analysisId && <ChatBot analysisId={analysisId} />}
          </div>
        </div>
      )}
    </div>
  );
};