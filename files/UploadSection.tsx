import React, { useState } from 'react';
import { uploadResume, uploadJobDescription } from '../services/api';
import { Upload, FileText } from 'lucide-react';

interface UploadSectionProps {
  onResumeUploaded: (resumeId: number) => void;
  onJobUploaded: (jobId: number) => void;
}

export const UploadSection: React.FC<UploadSectionProps> = ({ onResumeUploaded, onJobUploaded }) => {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState('');
  const [jobContent, setJobContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleResumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setResumeFile(e.target.files[0]);
    }
  };

  const handleResumeUpload = async () => {
    if (!resumeFile) {
      setError('Please select a resume file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await uploadResume(resumeFile);
      onResumeUploaded(response.data.resume_id);
      setResumeFile(null);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to upload resume');
    } finally {
      setLoading(false);
    }
  };

  const handleJobUpload = async () => {
    if (!jobTitle || !jobContent) {
      setError('Please fill in job title and description');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await uploadJobDescription(jobTitle, jobContent);
      onJobUploaded(response.data.job_id);
      setJobTitle('');
      setJobContent('');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to upload job description');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Resume Upload */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Upload Resume
          </h2>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleResumeChange}
                className="hidden"
                id="resume-input"
              />
              <label htmlFor="resume-input" className="cursor-pointer">
                <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400" />
                <p className="text-sm text-gray-600">
                  {resumeFile ? resumeFile.name : 'Click to upload or drag and drop'}
                </p>
                <p className="text-xs text-gray-500">PDF, DOCX, or TXT</p>
              </label>
            </div>
            <button
              onClick={handleResumeUpload}
              disabled={!resumeFile || loading}
              className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 text-white py-2 px-4 rounded"
            >
              {loading ? 'Uploading...' : 'Upload Resume'}
            </button>
          </div>
        </div>

        {/* Job Description Upload */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Paste Job Description
          </h2>
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Job Title"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:border-blue-500"
            />
            <textarea
              placeholder="Paste job description here..."
              value={jobContent}
              onChange={(e) => setJobContent(e.target.value)}
              rows={6}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:border-blue-500"
            />
            <button
              onClick={handleJobUpload}
              disabled={!jobTitle || !jobContent || loading}
              className="w-full bg-green-500 hover:bg-green-600 disabled:bg-gray-300 text-white py-2 px-4 rounded"
            >
              {loading ? 'Processing...' : 'Upload Job Description'}
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
    </div>
  );
};