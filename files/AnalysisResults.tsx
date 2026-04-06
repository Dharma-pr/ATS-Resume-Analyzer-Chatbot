import React from 'react';
import { BarChart3, CheckCircle, AlertCircle, TrendingUp } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface AnalysisData {
  match_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  semantic_gaps: Record<string, string[]>;
  feedback: string;
  recommendations: string[];
}

interface AnalysisResultsProps {
  data: AnalysisData;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-100';
    if (score >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  return (
    <div className="space-y-6">
      {/* Match Score */}
      <div className={`${getScoreBgColor(data.match_score)} p-6 rounded-lg`}>
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600">Overall Match Score</p>
            <p className={`text-4xl font-bold ${getScoreColor(data.match_score)}`}>
              {data.match_score}%
            </p>
          </div>
          <BarChart3 className={`w-16 h-16 ${getScoreColor(data.match_score)}`} />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Matched Keywords */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CheckCircle className="w-5 h-5 text-green-500" />
            Matched Keywords
          </h3>
          <div className="flex flex-wrap gap-2">
            {data.matched_keywords.map((keyword, index) => (
              <span
                key={index}
                className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>

        {/* Missing Keywords */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            Missing Keywords
          </h3>
          <div className="flex flex-wrap gap-2">
            {data.missing_keywords.slice(0, 10).map((keyword, index) => (
              <span
                key={index}
                className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
              >
                {keyword}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Semantic Gaps */}
      {Object.keys(data.semantic_gaps).length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Semantic Gaps
          </h3>
          <div className="space-y-3">
            {Object.entries(data.semantic_gaps).map(([gap, items]) => (
              <div key={gap}>
                <p className="font-medium text-gray-700 capitalize">{gap}</p>
                <ul className="list-disc list-inside text-gray-600 text-sm">
                  {items.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Feedback */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">AI Feedback</h3>
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{data.feedback}</ReactMarkdown>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
        <ol className="space-y-3">
          {data.recommendations.map((rec, index) => (
            <li key={index} className="flex gap-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <span className="text-gray-700">{rec}</span>
            </li>
          ))}
        </ol>
      </div>
    </div>
  );
};